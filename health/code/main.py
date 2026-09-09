from typing import List, Dict, Any, Tuple, Set
from pathlib import Path
from itertools import product
import os
import json
import random
from datetime import datetime, timedelta

import nutritional_facts

from nutrition_calculation import (
    bmr,
    lean_body_mass,
    tdee_calc,
    tdee_output,
    input_conversion,
    activity_factor,
)
from weekly_program import user_program
from exercises import EXERCISES
from lifting_calculations.weight_lifting_program import evaluate_selected_program
from lifting_calculations.program_matrix import attach_weekly_prescriptions, normalize_training_goal


def get_training_day_offsets(freq: int) -> List[int]:
    """
    Monday is offset 0. Returns which weekdays you train for a given frequency.
    5 -> Mon..Fri
    4 -> Mon, Tue, Thu, Fri
    3 -> Mon, Wed, Fri
    2 -> Tue, Thu
    """
    if freq == 5:
        return [0, 1, 2, 3, 4]
    if freq == 4:
        return [0, 1, 3, 4]
    if freq == 3:
        return [0, 2, 4]
    if freq == 2:
        return [1, 3]

    raise ValueError("lifting_frequency_input must be one of {2,3,4,5}")


def infer_num_weeks(selected_program: List[List[Dict[str, Any]]]) -> int:
    """
    Finds the first exercise with 'weeks' and returns len(weeks).
    Assumes you've already called attach_weekly_prescriptions(...).
    """
    for day in selected_program:
        for ex in day:
            weeks = ex.get("weeks")
            if weeks:
                return len(weeks)

    raise RuntimeError("No 'weeks' found on any exercise. Did you call attach_weekly_prescriptions()?")


def build_maxes_list(selected_program: List[List[Dict[str, Any]]]) -> List[Tuple[str, int]]:
    """
    Returns a de-duplicated list of (exercise name, 1RM) for the selected program.
    Uses the first occurrence order across days.
    """
    seen: Set[str] = set()
    out: List[Tuple[str, int]] = []

    for day in selected_program:
        for ex in day:
            name = ex.get("name", ex.get("key", "<unknown>"))

            if name in seen:
                continue

            one_rm = ex.get("one_rm")

            if isinstance(one_rm, (int, float)):
                out.append((name, int(one_rm)))
                seen.add(name)

    return out


def build_inputs_text_last_week(selected_program: List[List[Dict[str, Any]]]) -> str:
    """
    Produce a plain-text summary for the LAST attached week:
    - Day by day
    - Each exercise on one line
    - Shows 1RM and the last week's target as:
      - Exercise | 1RM: X | try: Y reps @ Z lbs first
    """
    lines: List[str] = []

    num_weeks = None

    for day in selected_program:
        for ex in day:
            weeks = ex.get("weeks")
            if weeks:
                num_weeks = len(weeks)
                break

        if num_weeks is not None:
            break

    if not num_weeks or num_weeks < 1:
        raise RuntimeError("Expected at least 1 week attached to exercises. Check attach_weekly_prescriptions().")

    week_index = num_weeks - 1
    week_label = week_index + 1

    lines.append(f"=== Week {week_label} Inputs Snapshot ===")
    lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    for day_idx, day in enumerate(selected_program, start=1):
        lines.append(f"Day {day_idx}")

        for ex in day:
            name = ex.get("name", ex.get("key", "<unknown>"))
            one_rm = ex.get("one_rm", "N/A")
            weeks = ex.get("weeks", [])

            if week_index < len(weeks):
                w = weeks[week_index]
                reps = w.get("reps", "N/A")
                weight = w.get("weight", "N/A")
                pct = w.get("pct_1rm", None)
                pct_text = f"{round(pct * 100)}% 1RM" if isinstance(pct, (int, float)) else "N/A"

                lines.append(f"- {name} | 1RM: {one_rm} | try: {reps} reps @ {weight} lbs ({pct_text}) first")
            else:
                lines.append(f"- {name} | 1RM: {one_rm} | try: (no data)")

        lines.append("")

    return "\n".join(lines)


def _darken_hex(hex_color: str, factor: float = 0.75) -> str:
    """
    Darken a hex color by multiplying RGB channels by factor.
    """
    hex_color = hex_color.strip().lstrip("#")

    if len(hex_color) != 6:
        return "#3B3A30"

    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))

    return f"#{r:02X}{g:02X}{b:02X}"


def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert a hex color to RGB.
    """
    hex_color = hex_color.strip().lstrip("#")

    if len(hex_color) != 6:
        return (59, 58, 48)

    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB values to a hex color.
    """
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))

    return f"#{r:02X}{g:02X}{b:02X}"


def _relative_luminance(hex_color: str) -> float:
    """
    Calculates perceived brightness so text can stay readable.
    """
    r, g, b = _hex_to_rgb(hex_color)

    def channel(c: int) -> float:
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    return (
        0.2126 * channel(r)
        + 0.7152 * channel(g)
        + 0.0722 * channel(b)
    )


def _text_color_for_bg(hex_color: str) -> str:
    """
    Pick white or dark text depending on background color.
    """
    return "#FFFFFF" if _relative_luminance(hex_color) < 0.42 else "#2B2118"


def _blend_with_white(hex_color: str, amount: float = 0.35) -> str:
    """
    Softens a color by blending it with white.
    amount closer to 1 means lighter.
    """
    r, g, b = _hex_to_rgb(hex_color)

    r = r + (255 - r) * amount
    g = g + (255 - g) * amount
    b = b + (255 - b) * amount

    return _rgb_to_hex(r, g, b)


def _random_base_hex() -> str:
    """
    Generate a random base color.
    """
    return _rgb_to_hex(
        random.randint(40, 215),
        random.randint(40, 215),
        random.randint(40, 215),
    )


def _random_soft_hex() -> str:
    """
    Generate a readable soft color for backgrounds.
    """
    return _blend_with_white(_random_base_hex(), amount=random.uniform(0.35, 0.65))


def generate_random_color_scheme(count: int = 12) -> Dict[str, Any]:
    """
    Random page-wide color scheme.
    Keeps all program content the same and only changes colors.
    """
    page_bg = _blend_with_white(_random_base_hex(), amount=0.78)

    primary_bg = _darken_hex(_random_base_hex(), factor=random.uniform(0.45, 0.70))
    secondary_bg = _darken_hex(_random_base_hex(), factor=random.uniform(0.45, 0.70))
    accent_bg = _darken_hex(_random_base_hex(), factor=random.uniform(0.50, 0.75))

    week_colors = [_random_soft_hex() for _ in range(count)]

    return {
        "page_bg": page_bg,
        "body_text": "#2B2118",
        "primary_bg": primary_bg,
        "primary_text": _text_color_for_bg(primary_bg),
        "secondary_bg": secondary_bg,
        "secondary_text": _text_color_for_bg(secondary_bg),
        "accent_bg": accent_bg,
        "accent_text": _text_color_for_bg(accent_bg),
        "week_colors": week_colors,
    }


def html_escape(text: str) -> str:
    """
    Minimal HTML escaping for injecting into textarea safely.
    """
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


MEAL_TEMPLATES = [
    {
        "name": "Chicken Rice Bowl",
        "foods": [
            "Chicken breast, boneless skinless, raw",
            "White rice, dry",
            "Black beans, cooked",
            "Broccoli, raw",
            "Olive oil",
        ],
        "gram_ranges": {
            "Chicken breast, boneless skinless, raw": (100, 350),
            "White rice, dry": (40, 175),
            "Black beans, cooked": (0, 250),
            "Broccoli, raw": (50, 300),
            "Olive oil": (0, 35),
        },
    },
    {
        "name": "Turkey Oats Yogurt Meal",
        "foods": [
            "Extra lean ground turkey, 99%, raw",
            "Oats, dry",
            "Fage Total 0% Greek yogurt",
            "Blueberries, raw",
            "Chia seeds",
        ],
        "gram_ranges": {
            "Extra lean ground turkey, 99%, raw": (100, 350),
            "Oats, dry": (30, 150),
            "Fage Total 0% Greek yogurt": (100, 350),
            "Blueberries, raw": (0, 200),
            "Chia seeds": (0, 40),
        },
    },
    {
        "name": "Beef Potato Plate",
        "foods": [
            "Ground beef, 96% lean, raw",
            "White potato, raw",
            "Green peas, raw",
            "Avocado, raw",
            "Olive oil",
        ],
        "gram_ranges": {
            "Ground beef, 96% lean, raw": (100, 350),
            "White potato, raw": (150, 600),
            "Green peas, raw": (50, 250),
            "Avocado, raw": (0, 150),
            "Olive oil": (0, 25),
        },
    },
    {
        "name": "Pork Pasta Meal",
        "foods": [
            "Pork tenderloin, raw",
            "Pasta, dry",
            "Red sauce, no sugar added",
            "Mushrooms, white, raw",
            "Olive oil",
        ],
        "gram_ranges": {
            "Pork tenderloin, raw": (100, 350),
            "Pasta, dry": (40, 175),
            "Red sauce, no sugar added": (100, 250),
            "Mushrooms, white, raw": (50, 250),
            "Olive oil": (0, 30),
        },
    },
]


def meal_score_by_priority(totals: Dict[str, float], targets: Dict[str, float]) -> float:
    """
    Lower score is better.

    Priority order:
    1. Protein
    2. Fiber
    3. Carbs
    4. Calories
    5. Fat
    """
    weights = {
        "protein_g": 10,
        "fiber_g": 8,
        "carbs_g": 6,
        "kcal": 4,
        "fat_g": 2,
    }

    score = 0.0

    for key, weight in weights.items():
        score += abs(totals[key] - targets[key]) * weight

    return score


def build_meal_with_custom_ranges(
    selected_food_descriptions: List[str],
    targets: Dict[str, float],
    gram_ranges: Dict[str, Tuple[int, int]],
    step: int = 5,
) -> Dict[str, Any]:
    """
    Builds a meal from selected foods using realistic gram ranges.
    """
    selected_foods = [
        nutritional_facts.get_food_by_description(description)
        for description in selected_food_descriptions
    ]

    all_gram_options = []

    for food in selected_foods:
        low, high = gram_ranges.get(food["description"], (0, 300))
        all_gram_options.append(range(low, high + step, step))

    best_meal = None
    best_totals = None
    best_difference = None
    best_score = float("inf")

    for gram_combo in product(*all_gram_options):
        meal = []

        for food, grams in zip(selected_foods, gram_combo):
            if grams > 0:
                meal.append(nutritional_facts.scale_food(food, grams))

        totals = nutritional_facts.total_meal(meal)
        score = meal_score_by_priority(totals, targets)

        if score < best_score:
            best_score = score
            best_meal = meal
            best_totals = totals
            best_difference = nutritional_facts.macro_difference(totals, targets)

    return {
        "meal": best_meal,
        "totals": best_totals,
        "targets": targets,
        "difference": best_difference,
        "score": round(best_score, 1),
    }


def build_meal_portion_ideas(meal_targets: Dict[str, float]) -> List[Dict[str, Any]]:
    """
    Builds meal portion ideas from preset meal templates.
    Best matching meals are returned first.
    """
    meal_ideas = []

    for template in MEAL_TEMPLATES:
        result = build_meal_with_custom_ranges(
            selected_food_descriptions=template["foods"],
            targets=meal_targets,
            gram_ranges=template["gram_ranges"],
            step=5,
        )

        meal_ideas.append({
            "name": template["name"],
            "result": result,
        })

    meal_ideas.sort(key=lambda item: item["result"]["score"])

    return meal_ideas


def build_meal_ideas_html(meal_ideas: List[Dict[str, Any]]) -> str:
    """
    Builds the HTML table for meal portion ideas.
    """
    html = """
        <details class="week-collapsible" open>
          <summary class="week-summary" style="background-color:#6B4F2A;">
            Meal Portion Ideas
          </summary>

          <div class="week-section" style="--week-bg:#D5BA96; --week-border:#6B4F2A; background-color:var(--week-bg); border:8px solid var(--week-border);">
"""

    for idea in meal_ideas:
        name = idea["name"]
        result = idea["result"]
        meal = result["meal"]
        totals = result["totals"]
        targets = result["targets"]
        difference = result["difference"]

        html += f"""
            <div class="day-card">
              <div class="day-title">{name}</div>

              <table>
                <tr>
                  <th>Food</th>
                  <th>Serving (g)</th>
                  <th>Kcal</th>
                  <th>Protein (g)</th>
                  <th>Carbs (g)</th>
                  <th>Fat (g)</th>
                  <th>Fiber (g)</th>
                </tr>
"""

        for item in meal:
            html += f"""
                <tr>
                  <td>{item["description"]}</td>
                  <td>{item["grams"]}</td>
                  <td>{item["kcal"]}</td>
                  <td>{item["protein_g"]}</td>
                  <td>{item["carbs_g"]}</td>
                  <td>{item["fat_g"]}</td>
                  <td>{item["fiber_g"]}</td>
                </tr>
"""

        html += f"""
              </table>

              <table>
                <tr>
                  <th></th>
                  <th>Kcal</th>
                  <th>Protein (g)</th>
                  <th>Carbs (g)</th>
                  <th>Fat (g)</th>
                  <th>Fiber (g)</th>
                </tr>
                <tr>
                  <td>Targets</td>
                  <td>{round(targets["kcal"], 1)}</td>
                  <td>{round(targets["protein_g"], 1)}</td>
                  <td>{round(targets["carbs_g"], 1)}</td>
                  <td>{round(targets["fat_g"], 1)}</td>
                  <td>{round(targets["fiber_g"], 1)}</td>
                </tr>
                <tr>
                  <td>Totals</td>
                  <td>{round(totals["kcal"], 1)}</td>
                  <td>{round(totals["protein_g"], 1)}</td>
                  <td>{round(totals["carbs_g"], 1)}</td>
                  <td>{round(totals["fat_g"], 1)}</td>
                  <td>{round(totals["fiber_g"], 1)}</td>
                </tr>
                <tr>
                  <td>Difference</td>
                  <td>{round(difference["kcal"], 1)}</td>
                  <td>{round(difference["protein_g"], 1)}</td>
                  <td>{round(difference["carbs_g"], 1)}</td>
                  <td>{round(difference["fat_g"], 1)}</td>
                  <td>{round(difference["fiber_g"], 1)}</td>
                </tr>
              </table>
            </div>
"""

    html += """
          </div>
        </details>
"""

    return html


def build_nutrition_goals_html(
    header,
    goal_label_matrix,
    kcal,
    proteins,
    carbs,
    fat,
    fiber,
) -> str:
    """
    Builds the Nutrition Goals section with calories and macros only.
    """
    html = """
  <section id="nutrition-goals">
    <details class="collapsible">
      <summary class="summary-header">Nutrition Guide</summary>
      <div class="collapse-body">

        <details class="week-collapsible" open>
          <summary class="week-summary" style="background-color:#3B3A30;">
            Calories and Macros
          </summary>

          <div class="week-section" style="--week-bg:#D9D2B6; --week-border:#3B3A30; background-color:var(--week-bg); border:8px solid var(--week-border);">
            <table>
              <tr>
"""

    for col in header:
        html += f"                <th>{col}</th>\n"

    html += """
              </tr>
              <tr>
"""

    for cell in goal_label_matrix:
        html += f"                <td>{cell}</td>\n"

    html += """
              </tr>
            </table>

            <table>
              <tr>
                <th>Calories</th>
                <th>Protein</th>
                <th>Carbs</th>
                <th>Fat</th>
                <th>Fiber</th>
              </tr>
              <tr>
"""

    for cell in [kcal, proteins, carbs, fat, fiber]:
        if isinstance(cell, (int, float)):
            html += f"                <td>{round(cell, 1)}</td>\n"
        else:
            html += f"                <td>{cell}</td>\n"

    html += """
              </tr>
            </table>
          </div>
        </details>

      </div>
    </details>
  </section>
"""

    return html

def main():
    now = datetime.now()
    today = now.date()

    days_ahead = (0 - today.weekday() + 7) % 7
    next_monday = today + timedelta(days=days_ahead)

    # -------------------- Inputs --------------------
    name_input = str(input("Name: "))
    gender = str(input("Gender (M or F or Oth): "))
    age = int(input("Age: "))
    weight_input = int(input("Weight (lb): "))
    height_input = input("Height (ft,in): ")
    body_fat_input = float(
        input("Approximate body fat percentage (just integers, no sign): "))
    sleep_score_input = float(
        input("Approximate hours of Sleep per night? (ex. 7.5): "))
    lifting_frequency_input = int(
        input("How many days a week do you lift weights? "))
    training_age_input = int(
        input("How long have you been strength training in years? "))
    cardio_frequency_input = int(
        input("How many days a week do you do cardio? "))
    daily_step_activity_input = int(
        input("How many steps do you get approximately every day? "))
    job_type_input = str(
        input(
            "What type of Job do you have? Sedentary (desk job), Moderate(retail), Active (Contruction). "
        ))
    rank_input = input("Easy, Advanced, or Injured (E, A, or I): ").lower()
    lifting_goal_input = input(
        "Lifting goal? Hypertrophy or Strength (H or S): ").lower()
    training_goal = normalize_training_goal(lifting_goal_input)
    training_goal_label = training_goal.title()
    nutrition_goal = input("lose, gain, or maintain? (L, G, or M): ").lower()
    nutrition_goal_level = input(
        "Goal rank? Agressive, or Moderate (A or M): ").lower()
    # meal_frequency_input = int(input("How many meals per day do you want? "))

    # if meal_frequency_input <= 0:
    #     raise ValueError("Meal frequency must be greater than 0.")

    # ================== Nutrition Info =========================
    weight = input_conversion.weight_kg_conversions(weight_input)
    height = input_conversion.height_cm_conversions(height_input)

    lean_body_mass_kg = lean_body_mass.lean_body_mass_calculation_kg(
        weight,
        body_fat_input,
        height,
        gender,
        training_age_input,
    )

    calc_bmr = bmr.calculate_bmr(
        gender,
        age,
        weight,
        height,
        lean_body_mass_kg,
    )

    activity = activity_factor.calculate_activity_factor(
        daily_step_activity_input,
        job_type_input,
        sleep_score_input,
        body_fat_input,
        lifting_frequency_input,
        cardio_frequency_input,
    )

    tdee = tdee_calc.calculate_tdee(calc_bmr, activity)

    tdee_percentage, carb_percentage, goal_type_label = tdee_output.user_nutrition_plan(
        nutrition_goal,
        nutrition_goal_level,
    )

    header, goal_label_matrix, kcal, proteins, carbs, fat, fiber = tdee_output.nutrition_table(
        tdee,
        lean_body_mass_kg,
        goal_type_label,
        tdee_percentage,
        carb_percentage,
    )

    # ================== Lifting program =========================
    selected = user_program(rank_input, lifting_frequency_input, training_goal)
    evaluated_program, one_rms = evaluate_selected_program(selected, EXERCISES)
    full_program = attach_weekly_prescriptions(evaluated_program,
                                               training_goal=training_goal)
    initial_inputs_text = build_inputs_text_last_week(full_program)

    num_weeks = infer_num_weeks(full_program)
    day_offsets = get_training_day_offsets(lifting_frequency_input)

    if len(full_program) != len(day_offsets):
        raise RuntimeError(
            f"The selected program has {len(full_program)} days but training frequency "
            f"({lifting_frequency_input}) maps to {len(day_offsets)} calendar days."
        )

    last_day_offset = day_offsets[-1]
    end_date = next_monday + timedelta(weeks=num_weeks - 1,
                                       days=last_day_offset)

    maxes_list = build_maxes_list(full_program)

    # -------------------- Build HTML --------------------
    color_scheme = generate_random_color_scheme(count=max(num_weeks, 12))
    week_colors = color_scheme["week_colors"]

    initial_inputs_text_for_textarea = html_escape(initial_inputs_text)
    session_default_text_js = json.dumps(initial_inputs_text)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <title>The Program to Get Jacked</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Roboto+Slab:wght@400;700&display=swap" rel="stylesheet">
  <style>
    body {{
      font-family: 'Roboto Slab', serif;
      margin: 20px;
      line-height: 1.8;
      font-size: 16px;
      color: {color_scheme["body_text"]};
      background-color: {color_scheme["page_bg"]};
    }}

    h1, h2, h3 {{
      font-family: 'Oswald', sans-serif;
      font-weight: 700;
      text-align: center;
      color: {color_scheme["primary_bg"]};
      text-transform: uppercase;
    }}

    h1 {{
      font-size: 28px;
      margin-bottom: 20px;
    }}

    table {{
      border-collapse: collapse;
      width: 100%;
      margin-bottom: 20px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
      background: white;
    }}

    th {{
      background-color: {color_scheme["secondary_bg"]};
      color: {color_scheme["secondary_text"]};
      font-size: 16px;
      font-family: 'Oswald', sans-serif;
      font-weight: bold;
      padding: 12px;
    }}

    td {{
      border: 1px solid #ccc;
      padding: 8px;
      text-align: center;
      font-family: 'Roboto Slab', serif;
      font-size: 15px;
      background: white;
    }}

    .week-section {{
      padding: 14px;
      margin: 0;
      border-radius: 10px;
      border: 8px solid var(--week-border);
      background-color: var(--week-bg);
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.18);
    }}

    .day-card {{
      background: rgba(255, 255, 255, 0.82);
      border-radius: 10px;
      border: 6px solid {color_scheme["primary_bg"]};
      margin: 14px 0;
      overflow: hidden;
    }}

    .day-title {{
      font-family: 'Oswald', sans-serif;
      font-size: 18px;
      padding: 10px 12px;
      background: {color_scheme["primary_bg"]};
      color: {color_scheme["primary_text"]};
      text-align: left;
      letter-spacing: 0.5px;
    }}

    .day-card table {{
      box-shadow: none;
      margin: 0 0 20px 0;
      border-collapse: collapse;
      width: 100%;
      background: white;
    }}

    details {{
      border-radius: 10px;
      margin: 12px 0 18px;
      background: #fff;
      box-shadow: 0 6px 14px rgba(0,0,0,0.10);
      overflow: hidden;
    }}

    summary::-webkit-details-marker {{ display: none; }}
    summary {{ user-select: none; }}

    .summary-header {{
      display: flex;
      align-items: center;
      justify-content: center;
      text-align: center;
      list-style: none;
      cursor: pointer;
      padding: 12px 14px;
      margin: 0;
      background-color: {color_scheme["accent_bg"]};
      color: {color_scheme["accent_text"]};
      font-family: 'Oswald', sans-serif;
      font-size: 20px;
      text-transform: uppercase;
      border: none;
    }}

    .week-summary {{
      display: flex;
      align-items: center;
      cursor: pointer;
      padding: 10px 12px;
      font-family: 'Oswald', sans-serif;
      font-size: 18px;
      color: #fff;
      text-transform: uppercase;
      border: none;
      list-style: none;
    }}

    .collapse-body {{ padding: 12px 12px 16px 12px; }}
  </style>
</head>

<body>
  <h1>The "Getting Jacked" Program</h1>

  <div style="display:flex; gap:10px; justify-content:center; margin: 8px 0 16px;">
    <button id="expandAllBtn" type="button">Expand all</button>
    <button id="collapseAllBtn" type="button">Collapse all</button>
  </div>

  <script>
    document.addEventListener('DOMContentLoaded', () => {{
      const expandAllBtn = document.getElementById('expandAllBtn');
      const collapseAllBtn = document.getElementById('collapseAllBtn');

      expandAllBtn.addEventListener('click', () => {{
        document.querySelectorAll('details').forEach(d => d.open = true);
      }});

      collapseAllBtn.addEventListener('click', () => {{
        document.querySelectorAll('details').forEach(d => d.open = false);
      }});
    }});
  </script>

  <section id="lifting-program">
    <details class="collapsible">
      <summary class="summary-header">Lifting Program</summary>
      <div class="collapse-body">
"""

    # Weeks
    for week_index in range(num_weeks):
        week_start = next_monday + timedelta(weeks=week_index)
        week_end = week_start + timedelta(days=6)

        week_bg = week_colors[week_index % len(week_colors)]
        week_border = _darken_hex(week_bg, factor=0.58)
        week_text = _text_color_for_bg(week_border)

        html_content += f"""
        <details class="week-collapsible">
          <summary class="week-summary" style="background-color:{week_border}; color:{week_text};">
            Week {week_index + 1}: {week_start.strftime('%m-%d-%y')} to {week_end.strftime('%m-%d-%y')}
          </summary>

          <div class="week-section" style="--week-bg: {week_bg}; --week-border: {week_border}; background-color: var(--week-bg); border: 8px solid var(--week-border);">
"""

        for day_index, day in enumerate(full_program):
            day_date = week_start + timedelta(days=day_offsets[day_index])

            html_content += f"""
            <div class="day-card">
              <div class="day-title">Day {day_index + 1}: {day_date.strftime('%A, %m-%d-%y')}</div>
              <table>
                <tr>
                  <th>Exercise</th>
                  <th>Weight (lbs)</th>
                  <th>% 1RM</th>
                  <th>Sets</th>
                  <th>Reps</th>
                </tr>
"""

            for ex in day:
                name = ex.get("name", ex.get("key", "<unknown>"))

                try:
                    week_block = ex["weeks"][week_index]
                    weight_val = week_block["weight"]
                    pct_val = week_block["pct_1rm"]
                    pct_display = f"{round(pct_val * 100)}%"
                    sets_val = week_block["sets"]
                    reps_val = week_block["reps"]
                except (KeyError, IndexError):
                    weight_val = pct_display = sets_val = reps_val = "—"

                html_content += f"""
                <tr>
                  <td>{name}</td>
                  <td>{weight_val}</td>
                  <td>{pct_display}</td>
                  <td>{sets_val}</td>
                  <td>{reps_val}</td>
                </tr>
"""

            html_content += """
              </table>
            </div>
"""

        html_content += """
          </div>
        </details>
"""

    html_content += f"""
      </div>
    </details>
  </section>

  <section id="user-lift-inputs">
    <details class="collapsible">
      <summary class="summary-header">Your Lift Inputs (Editable)</summary>
      <div class="collapse-body">
        <div class="day-card">
          <div class="day-title">Edit / Save Your Inputs</div>
          <div style="padding:12px;">
            <textarea id="liftInputBox" style="width:100%;height:260px;font-family:monospace;font-size:14px;white-space:pre;">{initial_inputs_text_for_textarea}</textarea>

            <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">
              <button onclick="saveLocal()">Save to browser</button>
              <button onclick="loadLocal()">Load from browser</button>
              <button onclick="resetDefaults()">Reset to this plan</button>
            </div>

            <p style="font-size:12px;color:#555;margin-top:8px;">
              • “Save to browser” stores your text in this browser (localStorage).<br>
              • “Load from browser” restores what you saved previously.
            </p>
          </div>
        </div>

        <script>
          const sessionDefaultText = {session_default_text_js};

          document.addEventListener('DOMContentLoaded', () => {{
            const box = document.getElementById('liftInputBox');
            const saved = localStorage.getItem('liftInputs');

            if (saved && saved.trim().length > 0) {{
              box.value = saved;
            }} else {{
              box.value = sessionDefaultText;
            }}
          }});

          function saveLocal() {{
            const box = document.getElementById('liftInputBox');
            localStorage.setItem('liftInputs', box.value);
            alert('Saved to this browser.');
          }}

          function loadLocal() {{
            const saved = localStorage.getItem('liftInputs');

            if (saved) {{
              document.getElementById('liftInputBox').value = saved;
            }} else {{
              alert('No browser-saved inputs found.');
            }}
          }}

          function resetDefaults() {{
            document.getElementById('liftInputBox').value = sessionDefaultText;
          }}
        </script>
      </div>
    </details>
  </section>

  <section id="progress-report">
    <details class="collapsible">
      <summary class="summary-header">Progress Report</summary>
      <div class="collapse-body">
        <table>
          <tr>
            <th>Exercise</th>
            <th>1 Rep Max (lbs)</th>
          </tr>
"""

    for exercise, max_weight in maxes_list:
        html_content += f"""
          <tr>
            <td>{exercise}</td>
            <td>{max_weight}</td>
          </tr>
"""


    html_content += """
        </table>
      </div>
    </details>
  </section>
"""

    html_content += build_nutrition_goals_html(
        header=header,
        goal_label_matrix=goal_label_matrix,
        kcal=kcal,
        proteins=proteins,
        carbs=carbs,
        fat=fat,
        fiber=fiber,
    )

    html_content += """
</body>
</html>
"""

# Write file
    output_path = "/home/u302264/personal/health/programs"
    os.makedirs(output_path, exist_ok=True)

    output_file = f"{name_input}_health_program_{next_monday.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.html"
    full_file_path = os.path.join(output_path, output_file)

    with open(full_file_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"Program saved to {full_file_path}")


if __name__ == "__main__":
    main()
