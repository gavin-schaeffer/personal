# lifting_calculations/program_matrix.py

from typing import Dict, Any, List, Tuple

from constants import (
    round_to,
    PROGRAM_PRESCRIPTIONS,
    ROLE_TO_PRESCRIPTION,
)


def round_to_nearest(x: float, nearest: int) -> int:
    return int(round(x / nearest) * nearest)


def normalize_training_goal(training_goal: str) -> str:
    if not training_goal:
        return "hypertrophy"

    goal = training_goal.strip().lower().replace("-", "_").replace(" ", "_")

    if goal in {
        "h",
        "hypertrophy",
        "muscle",
        "muscle_building",
        "build_muscle",
        "build_muscle",
        "bodybuilding",
    }:
        return "hypertrophy"

    if goal in {
        "s",
        "strength",
        "strength_training",
        "strength_building",
        "build_strength",
        "powerlifting",
        "power",
    }:
        return "strength"

    if goal in {
        "b",
        "balance",
        "balanced",
        "hybrid",
        "strength_and_size",
        "size_and_strength",
    }:
        return "balanced"

    raise ValueError(
        "training_goal must be one of: "
        "H/hypertrophy, S/strength, or B/balanced"
    )


def normalize_role(role: str) -> str:
    """
    Converts exercise roles into PROGRAM_PRESCRIPTIONS roles.

    EXERCISES roles:
    - main
    - auxiliary
    - isolation

    PROGRAM_PRESCRIPTIONS roles:
    - main
    - main_aux
    - aux
    """

    if not role:
        return "aux"

    role_clean = role.strip().lower().replace("-", "_").replace(" ", "_")

    if role_clean in ROLE_TO_PRESCRIPTION:
        return ROLE_TO_PRESCRIPTION[role_clean]

    if role_clean in {"main"}:
        return "main"

    if role_clean in {"main_aux", "main__aux", "auxiliary", "compound_aux"}:
        return "main_aux"

    if role_clean in {"aux", "isolation", "isolated", "accessory"}:
        return "aux"

    return "aux"


def get_role_profile(
    role: str,
    training_goal: str = "hypertrophy",
) -> Tuple[List[int], List[int], Dict[int, float]]:
    """
    Dynamically selects the correct sets/reps/%1RM profile.

    Example:
    training_goal = "strength"
    role = "main"

    Returns:
    PROGRAM_PRESCRIPTIONS["strength"]["main"]
    """

    goal_key = normalize_training_goal(training_goal)
    role_key = normalize_role(role)

    try:
        profile = PROGRAM_PRESCRIPTIONS[goal_key][role_key]
    except KeyError as e:
        raise KeyError(
            f"No prescription found for goal='{goal_key}', role='{role}', "
            f"normalized_role='{role_key}'. Check PROGRAM_PRESCRIPTIONS."
        ) from e

    return profile["sets"], profile["reps"], profile["rep_to_pct_1rm"]


def attach_weekly_prescriptions(
    selected_program: List[List[Dict[str, Any]]],
    default_round_to: int = None,
    training_goal: str = "hypertrophy",
) -> List[List[Dict[str, Any]]]:
    """
    Adds week-by-week prescriptions to each exercise.

    This is the important dynamic logic:

    PROGRAM_PRESCRIPTIONS[training_goal][role]

    So if the user chooses:
    - Hypertrophy -> uses PROGRAM_PRESCRIPTIONS["hypertrophy"]
    - Strength -> uses PROGRAM_PRESCRIPTIONS["strength"]
    - Balanced -> uses PROGRAM_PRESCRIPTIONS["balanced"]
    """

    rt = round_to if default_round_to is None else default_round_to
    goal_key = normalize_training_goal(training_goal)

    for day in selected_program:
        for ex in day:
            exercise_name = ex.get("name", ex.get("key", "<unknown>"))

            one_rm = ex.get("one_rm")

            if not isinstance(one_rm, (int, float)):
                raise ValueError(
                    f"Exercise '{exercise_name}' is missing a numeric 'one_rm'. "
                    f"Make sure evaluate_selected_program() runs before "
                    f"attach_weekly_prescriptions()."
                )

            role_key = normalize_role(ex.get("role", ""))

            sets_list, reps_list, pct_map = get_role_profile(
                role=ex.get("role", ""),
                training_goal=goal_key,
            )

            if len(sets_list) != len(reps_list):
                raise ValueError(
                    f"Sets and reps length mismatch for exercise '{exercise_name}' "
                    f"with role '{ex.get('role')}' under goal '{goal_key}'."
                )

            weeks: List[Dict[str, Any]] = []

            for week_number, (sets_i, reps_i) in enumerate(
                zip(sets_list, reps_list),
                start=1,
            ):
                if reps_i not in pct_map:
                    raise KeyError(
                        f"No %1RM mapping for reps={reps_i} in exercise "
                        f"'{exercise_name}', role='{ex.get('role')}', "
                        f"goal='{goal_key}'. Update constants.py rep_to_pct_1rm."
                    )

                pct = pct_map[reps_i]
                weight = round_to_nearest(one_rm * pct, rt)

                weeks.append(
                    {
                        "week": week_number,
                        "sets": sets_i,
                        "reps": reps_i,
                        "pct_1rm": pct,
                        "weight": weight,
                    }
                )

            ex["training_goal"] = goal_key
            ex["prescription_role"] = role_key
            ex["weeks"] = weeks

    return selected_program
