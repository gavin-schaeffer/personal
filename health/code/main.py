from typing import List, Dict, Any, Tuple, Set
import os
import json
import random
from datetime import datetime, timedelta

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
    for day in selected_program:
        for ex in day:
            weeks = ex.get("weeks")
            if weeks:
                return len(weeks)

    raise RuntimeError("No 'weeks' found on any exercise. Did you call attach_weekly_prescriptions()?")


def build_maxes_list(selected_program: List[List[Dict[str, Any]]]) -> List[Tuple[str, int]]:
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
    hex_color = hex_color.strip().lstrip("#")

    if len(hex_color) != 6:
        return (59, 58, 48)

    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
    )


def _rgb_to_hex(r: int, g: int, b: int) -> str:
    r = max(0, min(255, int(r)))
    g = max(0, min(255, int(g)))
    b = max(0, min(255, int(b)))

    return f"#{r:02X}{g:02X}{b:02X}"


def _relative_luminance(hex_color: str) -> float:
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
    return "#FFFFFF" if _relative_luminance(hex_color) < 0.42 else "#2B2118"


def _blend_with_white(hex_color: str, amount: float = 0.35) -> str:
    r, g, b = _hex_to_rgb(hex_color)

    r = r + (255 - r) * amount
    g = g + (255 - g) * amount
    b = b + (255 - b) * amount

    return _rgb_to_hex(r, g, b)


def _random_base_hex() -> str:
    return _rgb_to_hex(
        random.randint(40, 215),
        random.randint(40, 215),
        random.randint(40, 215),
    )


def _random_soft_hex() -> str:
    return _blend_with_white(_random_base_hex(), amount=random.uniform(0.35, 0.65))


def generate_random_color_scheme(count: int = 12) -> Dict[str, Any]:
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
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def build_nutrition_goals_html(
    header,
    goal_label_matrix,
    kcal,
    proteins,
    carbs,
    fat,
    fiber,
) -> str:
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
            <div class="table-scroll">
              <table>
                <tr>
"""

    for col in header:
        html += f"                  <th>{col}</th>\n"

    html += """
                </tr>
                <tr>
"""

    for cell in goal_label_matrix:
        html += f"                  <td>{cell}</td>\n"

    html += """
                </tr>
              </table>
            </div>

            <div class="table-scroll">
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
            html += f"                  <td>{round(cell, 1)}</td>\n"
        else:
            html += f"                  <td>{cell}</td>\n"

    html += """
                </tr>
              </table>
            </div>
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

    name_input = str(input("Name: "))
    gender = str(input("Gender (M or F or Oth): "))
    age = int(input("Age: "))
    weight_input = int(input("Weight (lb): "))
    height_input = input("Height (ft,in): ")
    body_fat_input = float(input("Approximate body fat percentage (just integers, no sign): "))
    sleep_score_input = float(input("Approximate hours of Sleep per night? (ex. 7.5): "))
    lifting_frequency_input = int(input("How many days a week do you lift weights? "))
    training_age_input = int(input("How long have you been strength training in years? "))
    cardio_frequency_input = int(input("How many days a week do you do cardio? "))
    daily_step_activity_input = int(input("How many steps do you get approximately every day? "))
    job_type_input = str(input("What type of Job do you have? Sedentary (desk job), Moderate(retail), Active (Construction). "))
    rank_input = input("Easy, Advanced, or Injured (E, A, or I): ").lower()
    lifting_goal_input = input("Lifting goal? Hypertrophy or Strength (H or S): ").lower()
    training_goal = normalize_training_goal(lifting_goal_input)
    training_goal_label = training_goal.title()
    nutrition_goal = input("lose, gain, or maintain? (L, G, or M): ").lower()
    nutrition_goal_level = input("Goal rank? Aggressive, or Moderate (A or M): ").lower()

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

    selected = user_program(rank_input, lifting_frequency_input, training_goal)
    evaluated_program, one_rms = evaluate_selected_program(selected, EXERCISES)

    full_program = attach_weekly_prescriptions(
        evaluated_program,
        training_goal=training_goal,
    )

    initial_inputs_text = build_inputs_text_last_week(full_program)

    num_weeks = infer_num_weeks(full_program)
    day_offsets = get_training_day_offsets(lifting_frequency_input)

    if len(full_program) != len(day_offsets):
        raise RuntimeError(
            f"The selected program has {len(full_program)} days but training frequency "
            f"({lifting_frequency_input}) maps to {len(day_offsets)} calendar days."
        )

    last_day_offset = day_offsets[-1]
    end_date = next_monday + timedelta(weeks=num_weeks - 1, days=last_day_offset)

    maxes_list = build_maxes_list(full_program)

    color_scheme = generate_random_color_scheme(count=max(num_weeks, 12))
    week_colors = color_scheme["week_colors"]

    initial_inputs_text_for_textarea = html_escape(initial_inputs_text)
    session_default_text_js = json.dumps(initial_inputs_text)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <title>{training_goal_label} Program</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@400;700&family=Roboto+Slab:wght@400;700&display=swap" rel="stylesheet">
  <style>
    * {{
      box-sizing: border-box;
    }}

    html {{
      width: 100%;
      overflow-x: hidden;
    }}

    body {{
      width: 100%;
      margin: 0;
      padding: 16px;
      line-height: 1.8;
      font-size: 16px;
      color: {color_scheme["body_text"]};
      background-color: {color_scheme["page_bg"]};
      font-family: 'Roboto Slab', serif;
      overflow-x: hidden;
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
      margin: 18px 0 20px;
      line-height: 1.15;
    }}

    button {{
      font: inherit;
      cursor: pointer;
    }}

    table {{
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
      background: white;
    }}

    th {{
      padding: 9px 5px;
      background-color: {color_scheme["secondary_bg"]};
      color: {color_scheme["secondary_text"]};
      font-family: 'Oswald', sans-serif;
      font-size: 13px;
      font-weight: bold;
      line-height: 1.15;
      text-align: center;
      white-space: normal;
      overflow-wrap: anywhere;
    }}

    td {{
      border: 1px solid #ccc;
      padding: 8px 5px;
      background: white;
      font-family: 'Roboto Slab', serif;
      font-size: 13px;
      line-height: 1.25;
      text-align: center;
      white-space: normal;
      overflow-wrap: anywhere;
    }}

    .page-shell {{
      width: 100%;
      max-width: 980px;
      margin: 0 auto;
    }}

    .button-row {{
      display: flex;
      gap: 10px;
      justify-content: center;
      flex-wrap: wrap;
      margin: 8px 0 16px;
    }}

    .table-scroll {{
      width: 100%;
      max-width: 100%;
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
    }}

    .table-scroll table {{
      margin: 0;
    }}

    .lift-table {{
      min-width: 315px;
    }}

    .lift-table th:nth-child(1),
    .lift-table td:nth-child(1) {{
      width: 38%;
      text-align: left;
    }}

    .lift-table th:nth-child(2),
    .lift-table td:nth-child(2) {{
      width: 17%;
    }}

    .lift-table th:nth-child(3),
    .lift-table td:nth-child(3) {{
      width: 12%;
    }}

    .lift-table th:nth-child(4),
    .lift-table td:nth-child(4) {{
      width: 12%;
    }}

    .lift-table th:nth-child(5),
    .lift-table td:nth-child(5) {{
      width: 21%;
    }}

    .week-section {{
      padding: 12px;
      margin: 0;
      border-radius: 10px;
      border: 8px solid var(--week-border);
      background-color: var(--week-bg);
      box-shadow: 0 6px 14px rgba(0, 0, 0, 0.18);
      overflow: hidden;
    }}

    .day-card {{
      width: 100%;
      max-width: 100%;
      margin: 14px 0;
      border: 6px solid {color_scheme["primary_bg"]};
      border-radius: 10px;
      background: rgba(255, 255, 255, 0.82);
      overflow: hidden;
    }}

    .day-title {{
      width: 100%;
      padding: 10px 12px;
      background: {color_scheme["primary_bg"]};
      color: {color_scheme["primary_text"]};
      font-family: 'Oswald', sans-serif;
      font-size: 18px;
      line-height: 1.2;
      text-align: left;
      letter-spacing: 0.5px;
      white-space: normal;
      overflow-wrap: anywhere;
    }}

    details {{
      width: 100%;
      max-width: 100%;
      border-radius: 10px;
      margin: 12px 0 18px;
      background: #fff;
      box-shadow: 0 6px 14px rgba(0,0,0,0.10);
      overflow: hidden;
    }}

    summary::-webkit-details-marker {{
      display: none;
    }}

    summary {{
      user-select: none;
    }}

    .summary-header {{
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 12px 14px;
      margin: 0;
      border: none;
      background-color: {color_scheme["accent_bg"]};
      color: {color_scheme["accent_text"]};
      font-family: 'Oswald', sans-serif;
      font-size: 20px;
      line-height: 1.2;
      text-align: center;
      text-transform: uppercase;
      list-style: none;
      cursor: pointer;
    }}

    .week-summary {{
      display: flex;
      align-items: center;
      padding: 10px 12px;
      border: none;
      color: #fff;
      font-family: 'Oswald', sans-serif;
      font-size: 18px;
      line-height: 1.2;
      text-transform: uppercase;
      list-style: none;
      cursor: pointer;
      white-space: normal;
      overflow-wrap: anywhere;
    }}

    .collapse-body {{
      padding: 12px;
      overflow-x: hidden;
    }}

    textarea {{
      width: 100%;
      max-width: 100%;
      box-sizing: border-box;
    }}

    @media (max-width: 760px) {{
      body {{
        padding: 8px;
        font-size: 14px;
      }}

      h1 {{
        font-size: 24px;
      }}

      .collapse-body {{
        padding: 8px;
      }}

      .week-section {{
        padding: 8px;
        border-width: 5px;
      }}

      .day-card {{
        border-width: 4px;
      }}

      .day-title {{
        padding: 8px 10px;
        font-size: 16px;
      }}

      .summary-header {{
        font-size: 18px;
      }}

      .week-summary {{
        font-size: 16px;
      }}

      th {{
        padding: 7px 4px;
        font-size: 12px;
      }}

      td {{
        padding: 7px 4px;
        font-size: 12px;
      }}

      .lift-table {{
        min-width: 300px;
      }}
    }}
  </style>
</head>

<body>
  <div class="page-shell">
    <h1>The "{training_goal_label}" Program</h1>

    <div class="button-row">
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

            <div class="week-section" style="--week-bg: {week_bg}; --week-border: {week_border};">
"""

        for day_index, day in enumerate(full_program):
            day_date = week_start + timedelta(days=day_offsets[day_index])

            html_content += f"""
              <div class="day-card">
                <div class="day-title">Day {day_index + 1}: {day_date.strftime('%A, %m-%d-%y')}</div>
                <div class="table-scroll">
                  <table class="lift-table">
                    <tr>
                      <th>Exercise</th>
                      <th>Weight</th>
                      <th>Sets</th>
                      <th>Reps</th>
                      <th>% 1RM</th>
                    </tr>
"""

            for ex in day:
                name = ex.get("name", ex.get("key", "<unknown>"))

                try:
                    week_block = ex["weeks"][week_index]
                    weight_val = week_block["weight"]
                    sets_val = week_block["sets"]
                    reps_val = week_block["reps"]
                    pct_val = week_block["pct_1rm"]
                    pct_display = f"{round(pct_val * 100)}%"
                except (KeyError, IndexError):
                    weight_val = sets_val = reps_val = pct_display = "-"

                html_content += f"""
                    <tr>
                      <td>{name}</td>
                      <td>{weight_val}</td>
                      <td>{sets_val}</td>
                      <td>{reps_val}</td>
                      <td>{pct_display}</td>
                    </tr>
"""

            html_content += """
                  </table>
                </div>
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
              <textarea id="liftInputBox" style="height:260px;font-family:monospace;font-size:14px;white-space:pre;">{initial_inputs_text_for_textarea}</textarea>

              <div style="margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;">
                <button onclick="saveLocal()">Save to browser</button>
                <button onclick="loadLocal()">Load from browser</button>
                <button onclick="resetDefaults()">Reset to this plan</button>
              </div>

              <p style="font-size:12px;color:#555;margin-top:8px;">
                - Save to browser stores your text in this browser using localStorage.<br>
                - Load from browser restores what you saved previously.
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
          <div class="table-scroll">
            <table>
              <tr>
                <th>Exercise</th>
                <th>1 Rep Max</th>
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
  </div>
</body>
</html>
"""

    output_path = "/home/u302264/personal/health/programs"
    os.makedirs(output_path, exist_ok=True)

    output_file = f"{name_input}_health_program_{next_monday.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}.html"
    full_file_path = os.path.join(output_path, output_file)

    with open(full_file_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"Program saved to {full_file_path}")


if __name__ == "__main__":
    main()