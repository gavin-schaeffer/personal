from typing import Dict, Any, List, Tuple
import sys
from constants import (
    round_to,
    main_sets, main_reps, main_rep_to_pct_1rm,
    main_aux_sets, main_aux_reps, main_aux_rep_to_pct_1rm,
    aux_sets, aux_reps, aux_rep_to_pct_1rm,
)

def round_to_nearest(x: float, nearest: int) -> int:
    return int(round(x / nearest) * nearest)

def normalize_role(role: str) -> str:
    """
    Normalize role values like 'main aux' and 'main_aux' to a single key: 'main_aux'.
    """
    if not role:
        return "aux"  # safe default
    r = role.strip().lower().replace("-", "_").replace(" ", "_")
    if r in {"main_aux", "main__aux"}:
        return "main_aux"
    if r == "main":
        return "main"
    # everything else treated as aux
    return "aux"

def get_role_profile(role: str) -> Tuple[List[int], List[int], Dict[int, float]]:
    """
    Return (sets_list, reps_list, rep_to_pct_map) for the given role.
    """
    r = normalize_role(role)
    if r == "main":
        return main_sets, main_reps, main_rep_to_pct_1rm
    elif r == "main_aux":
        return main_aux_sets, main_aux_reps, main_aux_rep_to_pct_1rm
    else:
        return aux_sets, aux_reps, aux_rep_to_pct_1rm

def attach_weekly_prescriptions(
    selected_program: List[List[Dict[str, Any]]],
    default_round_to: int = None,
) -> List[List[Dict[str, Any]]]:
    """
    Mutates each exercise dict in `selected_program` to add:
      ex['weeks'] = [
        {'sets': int, 'reps': int, 'pct_1rm': float, 'weight': int},  # week 1
        ...
      ]
    Uses role-specific sets/reps and %1RM maps from constants.
    Returns the same structure for convenience.

    EXPECTS each exercise dict to already have 'one_rm' resolved.
    """
    rt = round_to if default_round_to is None else default_round_to

    for day in selected_program:
        for ex in day:
            one_rm = ex.get("one_rm")
            if one_rm is None:
                # If not computed yet, you should run your evaluate_selected_program first
                raise ValueError(f"Exercise '{ex.get('name', ex.get('key', '<unknown>'))}' is missing 'one_rm'.")

            sets_list, reps_list, pct_map = get_role_profile(ex.get("role", ""))

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
            ex["weeks"] = weeks  # attach plan per week

    return selected_program
