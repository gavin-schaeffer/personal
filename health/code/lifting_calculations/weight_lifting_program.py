from typing import List, Dict, Any, Tuple, Set
from constants import one_rm_conversion_key, round_to

# If you already define this elsewhere, you can remove or merge it.
BASE_KEY_ALIASES: Dict[str, str] = {
    # Example fixes you mentioned (adjust to your data)
    # "incline_bench_main": "incline_bench",
    # "pull_down_main": "pull_down",
}

def round_to_nearest(x: float, nearest: int) -> int:
    return int(round(x / nearest) * nearest)

def convert_to_onerpm(lifting_weight: float, reps: int) -> int:
    """
    Convert weight × reps to estimated 1RM.
    Assumes one_rm_conversion_key maps reps -> fraction of 1RM (e.g., 6 -> 0.85).
    Falls back to Epley if reps not in the key.
    """
    if reps in one_rm_conversion_key:
        pct = float(one_rm_conversion_key[reps])
        if pct <= 0:
            raise ValueError(f"Conversion key for reps={reps} must be > 0.")
        est = lifting_weight / pct
    else:
        epley = lifting_weight * (1 + reps / 30.0)
        brzycki = lifting_weight * 36.0 / (37.0 - reps)
        lombardi = lifting_weight * (reps ** 0.10)
        est = (epley + brzycki + lombardi ) / 3
    return round_to_nearest(est, round_to)

# Prompt helpers
# -----------------------------
def prompt_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number (e.g., 225).")

def prompt_weight_reps(name: str) -> Tuple[int, int]:
    """Prompt user for weight and reps for an exercise."""
    print(f"\n{name}")
    w = prompt_int("  Weight lifted: ")
    r = prompt_int("  Reps completed: ")
    return w, r

# ---------- Core logic ----------
def evaluate_selected_program(
    selected_program: List[List[Dict[str, Any]]],
    exercises_catalog: Dict[str, Dict[str, Any]],
) -> Tuple[List[List[Dict[str, Any]]], Dict[str, int]]:
    """
    Evaluate ONLY the exercises used in the selected_program
    (list of day-lists of exercise dicts taken from exercises_catalog).

    - Prompts once for each unique ask_input exercise in the selection (weight+reps).
    - Computes 1RM for inputs, resolves derived/mirror values across the selection.
    - Attaches ex['one_rm'] to each exercise dict (mutates in-place).
    - Returns (selected_program, values_map), where values_map = {exercise_key: one_rm}.

    NOTE: Because you're using EXERCISES[...] directly to build the lists,
    each dict here is the same object as in EXERCISES, so mutation will reflect globally.
    """

    # Build a reverse index from object id -> key so we can recover keys from the dicts
    reverse_index: Dict[int, str] = {id(v): k for k, v in exercises_catalog.items()}

    # Collect unique keys used in the selected program
    used_keys: Set[str] = set()
    for day in selected_program:
        for ex in day:
            k = reverse_index.get(id(ex))
            if not k:
                raise KeyError("Exercise in program is not a known object from EXERCISES.")
            # Attach the key to the dict for convenience (optional)
            ex.setdefault("key", k)
            used_keys.add(k)

    # Prompt for inputs ONLY for used keys that ask_input=True
    values: Dict[str, int] = {}
    prompted: Set[str] = set()

    print("\nEnter your most recent top set (weight × reps) for each prompted exercise.")
    for day in selected_program:
        for ex in day:
            k = ex["key"]
            if k in prompted:
                continue
            if ex.get("ask_input") and k in used_keys:
                w, r = prompt_weight_reps(ex["name"])
                values[k] = convert_to_onerpm(w, r)
                prompted.add(k)

    # Resolve mirrors / derived values across ONLY the used set
    remaining = True
    passes, max_passes = 0, 12

    while remaining and passes < max_passes:
        remaining = False
        passes += 1

        for day in selected_program:
            for ex in day:
                k = ex["key"]
                if k in values:
                    ex["one_rm"] = values[k]
                    continue

                # mirror
                if "mirror" in ex:
                    src = ex["mirror"]
                    src = BASE_KEY_ALIASES.get(src, src)
                    if src in values:
                        values[k] = int(values[src])
                        ex["one_rm"] = values[k]
                        continue
                    else:
                        # Only keep trying if the source is within the used set or aliases to one that is
                        if src in used_keys:
                            remaining = True
                        continue

                # derived (base * factor)
                base = ex.get("base")
                fac = ex.get("factor")
                if base is not None and fac is not None:
                    base = BASE_KEY_ALIASES.get(base, base)
                    if base in values:
                        values[k] = round_to_nearest(values[base] * float(fac), round_to)
                        ex["one_rm"] = values[k]
                        continue
                    else:
                        if base in used_keys:
                            remaining = True
                        continue

                # If neither ask_input, mirror nor base-factor, and it's in selection, we can't resolve yet
                if not ex.get("ask_input"):
                    remaining = True

    # Final attachment (ensure every ex in the selection got a 1RM)
    unresolved = []
    for day in selected_program:
        for ex in day:
            k = ex["key"]
            if k in values:
                ex["one_rm"] = values[k]
            else:
                unresolved.append(ex.get("name", k))

    if unresolved:
        raise RuntimeError(
            "Unresolved exercises in selected program (missing inputs or base/mirror not resolvable): "
            + ", ".join(unresolved)
        )

    return selected_program, values