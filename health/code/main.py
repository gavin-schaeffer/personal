from typing import List, Dict, Any, Tuple, Set
from pathlib import Path
import os
import json
from datetime import datetime, timedelta

from nutrition_calculation import bmr, lean_body_mass, tdee_calc, tdee_output, input_conversion, activity_factor
from weekly_program import user_program
from exercises import EXERCISES
from lifting_calculations.weight_lifting_program import evaluate_selected_program
from lifting_calculations.program_matrix import attach_weekly_prescriptions


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
    Assumes you've already called attach_weekly_prescriptions(...)
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

    Assumes each exercise has a 'weeks' list attached.
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
                lines.append(f"- {name} | 1RM: {one_rm} | try: {reps} reps @ {weight} lbs first")
            else:
                lines.append(f"- {name} | 1RM: {one_rm} | try: (no data)")

        lines.append("")

    return "\n".join(lines)

def _darken_hex(hex_color: str, factor: float = 0.75) -> str:
    """
    Darken a hex color by multiplying RGB channels by factor (0..1).
    factor=0.75 makes it 25% darker.
    """
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) != 6:
        return "#3B3A30"  # fallback
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))
    return f"#{r:02X}{g:02X}{b:02X}"


def html_escape(text: str) -> str:
    """Minimal HTML escaping for injecting into textarea safely."""
    return (
        text.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
    )


def main():
    # Current date and time
    now = datetime.now()
    today = now.date()

    # Calculate the next Monday
    days_ahead = (0 - today.weekday() + 7) % 7
    next_monday = today + timedelta(days=days_ahead)

    # -------------------- Inputs --------------------
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
    job_type_input = str(input("What type of Job do you have? Sedentary (desk job), Moderate(retail), Active (Contruction). "))
    rank_input = input("Easy, Advanced, or Injured (E, A, or I): ").lower()
    
    #================== Nutrition Info =========================
    weight = input_conversion.weight_kg_conversions(weight_input)
    height = input_conversion.height_cm_conversions(height_input)
    lean_body_mass_kg = lean_body_mass.lean_body_mass_calculation_kg(
        weight, body_fat_input, height, gender, training_age_input
    )
    calc_bmr = bmr.calculate_bmr(gender, age, weight, height, lean_body_mass_kg)
    activity = activity_factor.calculate_activity_factor(
        daily_step_activity_input, job_type_input, sleep_score_input,
        body_fat_input, lifting_frequency_input, cardio_frequency_input
    )
    tdee = tdee_calc.calculate_tdee(calc_bmr, activity)
    nutrition_maxtrix = tdee_output.matrix_goal_plan(tdee, lean_body_mass_kg)

    #================== Lifting program =========================
    selected = user_program(rank_input, lifting_frequency_input)
    evaluated_program, one_rms = evaluate_selected_program(selected, EXERCISES)
    full_program = attach_weekly_prescriptions(evaluated_program)
    initial_inputs_text = build_inputs_text_last_week(full_program)

    num_weeks = infer_num_weeks(full_program)
    day_offsets = get_training_day_offsets(lifting_frequency_input)

    if len(full_program) != len(day_offsets):
        raise RuntimeError(
            f"The selected program has {len(full_program)} days but training frequency ({lifting_frequency_input}) "
            f"maps to {len(day_offsets)} calendar days."
        )

    last_day_offset = day_offsets[-1]
    end_date = next_monday + timedelta(weeks=num_weeks - 1, days=last_day_offset)

    maxes_list = build_maxes_list(full_program)

    # -------------------- Build HTML (REAL TAGS, NOT ESCAPED) --------------------
    week_colors = [
        "#D5BA96",
        "#D9D2B6",
        "#CAB48B",
        "#A89B7C",
        "#C1B095",
        "#BCA77F",
    ]

    # Safe injection for textarea & JS
    initial_inputs_text_for_textarea = html_escape(initial_inputs_text)
    session_default_text_js = json.dumps(initial_inputs_text)  # safe JS string

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
      color: #2B2118;
    }}

    h1, h2, h3 {{
      font-family: 'Oswald', sans-serif;
      font-weight: 700;
      text-align: center;
      color: #3B3A30;
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
      background-color: #3E4E2F;
      color: white;
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
      border: 6px solid #3B3A30;
      margin: 14px 0;
      overflow: hidden;
    }}

    .day-title {{
      font-family: 'Oswald', sans-serif;
      font-size: 18px;
      padding: 10px 12px;
      background: #3B3A30;
      color: white;
      text-align: left;
      letter-spacing: 0.5px;
    }}

    .day-card table {{
      box-shadow: none;
      margin: 0;
      border-collapse: collapse;
      width: 100%;
      background: white; /* fixed */
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
      background-color: #D5BA96;
      color: #fff;
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
        week_border = _darken_hex(week_bg, factor=0.72)

        html_content += f"""
        <details class="week-collapsible">
          <summary class="week-summary" style="background-color:{week_border};">
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
                  <th>Sets</th>
                  <th>Reps</th>
                </tr>
"""

            for ex in day:
                name = ex.get("name", ex.get("key", "<unknown>"))
                try:
                    week_block = ex["weeks"][week_index]
                    weight_val = week_block["weight"]
                    sets_val = week_block["sets"]
                    reps_val = week_block["reps"]
                except (KeyError, IndexError):
                    weight_val = sets_val = reps_val = "—"

                html_content += f"""
                <tr>
                  <td>{name}</td>
                  <td>{weight_val}</td>
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

  <section id="nutrition-goals">
    <details class="collapsible">
      <summary class="summary-header">Nutrition Goals</summary>
      <div class="collapse-body">
        <table>
          <tr>
"""

    for header in nutrition_maxtrix[0]:
        html_content += f"<th>{header}</th>"

    html_content += "</tr>"

    for row in nutrition_maxtrix[1:]:
        html_content += "<tr>"
        for cell in row:
            html_content += f"<td>{cell}</td>"
        html_content += "</tr>"

    html_content += """
        </table>
      </div>
    </details>
  </section>

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