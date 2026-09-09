from typing import Dict, Any, List, Tuple
import sys
from constants import (
    round_to,
    main_sets,
    main_reps,
    main_rep_to_pct_1rm,
    main_aux_sets,
    main_aux_reps,
    main_aux_rep_to_pct_1rm,
    aux_sets,
    aux_reps,
    aux_rep_to_pct_1rm,
)
from constants import round_to, PROGRAM_PRESCRIPTIONS

def round_to_nearest(x: float, nearest: int) -> int:
    return int(round(x / nearest) * nearest)


def normalize_role(role: str) -> str:
    """
    Normalize role values like 'main aux' and 'main_aux' to a single key: 'main_aux'.
    """
    if not role:
        return "aux"  # safe default
    r = role.strip().lower().replace("-", "_").replace(" ", "_")
    if r in {"main_aux", "main__aux", "auxiliary"}:
        return "main_aux"
    if r == "main":
        return "main"
    if r in {"aux", "isolation"}:
        return "aux"
    # everything else treated as aux
    return "aux"
def normalize_training_goal(training_goal: str) -> str:
    if not training_goal:
        return "hypertrophy"

    goal = training_goal.strip().lower().replace("-", "_").replace(" ", "_")

    if goal in {"h", "hypertrophy", "muscle", "muscle_building", "build_muscle", "bodybuilding"}:
        return "hypertrophy"

    if goal in {"s", "strength", "strength_training", "strength_building", "build_strength", "powerlifting"}:
        return "strength"

    raise ValueError("training_goal must be one of: H/hypertrophy or S/strength")

def get_role_profile(role: str, training_goal: str = "hypertrophy") -> Tuple[List[int], List[int], Dict[int, float]]:
    role_key = normalize_role(role)
    goal_key = normalize_training_goal(training_goal)

    profile = PROGRAM_PRESCRIPTIONS[goal_key][role_key]

    return profile["sets"], profile["reps"], profile["rep_to_pct_1rm"]
def attach_weekly_prescriptions(
    selected_program: List[List[Dict[str, Any]]],
    default_round_to: int = None,
    training_goal: str = "hypertrophy",
) -> List[List[Dict[str, Any]]]:
    rt = round_to if default_round_to is None else default_round_to
    goal_key = normalize_training_goal(training_goal)

    for day in selected_program:
        for ex in day:
            one_rm = ex.get("one_rm")
            if one_rm is None:
                raise ValueError(f"Exercise '{ex.get('name', ex.get('key', '<unknown>'))}' is missing 'one_rm'.")

            sets_list, reps_list, pct_map = get_role_profile(ex.get("role", ""), goal_key)

            if len(sets_list) != len(reps_list):
                raise ValueError(f"Sets and reps length mismatch for role '{ex.get('role')}'.")

            weeks: List[Dict[str, Any]] = []

            for i, (sets_i, reps_i) in enumerate(zip(sets_list, reps_list), start=1):
                if reps_i not in pct_map:
                    raise KeyError(
                        f"No %1RM mapping for reps={reps_i} in role '{ex.get('role')}'. "
                        f"Update constants rep_to_pct_1rm."
                    )

                pct = pct_map[reps_i]
                weight = round_to_nearest(one_rm * pct, rt)

                weeks.append({
                    "week": i,
                    "sets": sets_i,
                    "reps": reps_i,
                    "pct_1rm": pct,
                    "weight": weight,
                })

            ex["training_goal"] = goal_key
            ex["weeks"] = weeks

    return selected_program