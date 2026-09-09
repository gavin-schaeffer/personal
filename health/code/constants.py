round_to = 5

PROGRAM_PRESCRIPTIONS = {
    "hypertrophy": {
        "main": {
            "sets": [3, 4, 4, 4, 4, 4, 3, 3],
            "reps": [12, 12, 10, 10, 8, 8, 10, 8],
            "rep_to_pct_1rm": {
                6: 0.80,
                8: 0.76,
                10: 0.72,
                12: 0.68,
            },
        },
        "main_aux": {
            "sets": [3, 3, 4, 4, 4, 3, 3, 3],
            "reps": [15, 12, 12, 10, 10, 10, 12, 10],
            "rep_to_pct_1rm": {
                8: 0.72,
                10: 0.68,
                12: 0.64,
                15: 0.58,
            },
        },
        "aux": {
            "sets": [2, 3, 3, 3, 3, 3, 2, 2],
            "reps": [15, 15, 12, 12, 12, 10, 15, 12],
            "rep_to_pct_1rm": {
                10: 0.64,
                12: 0.60,
                15: 0.56,
            },
        },
    },
    "strength": {
        "main": {
            "sets": [4, 4, 5, 5, 4, 5, 3, 3],
            "reps": [5, 5, 4, 4, 3, 3, 2, 2],
            "rep_to_pct_1rm": {
                2: 0.92,
                3: 0.89,
                4: 0.86,
                5: 0.83,
            },
        },
        "main_aux": {
            "sets": [3, 4, 4, 4, 3, 4, 3, 3],
            "reps": [8, 6, 6, 5, 5, 4, 4, 3],
            "rep_to_pct_1rm": {
                3: 0.82,
                4: 0.80,
                5: 0.77,
                6: 0.74,
                8: 0.68,
            },
        },
        "aux": {
            "sets": [2, 3, 3, 3, 2, 3, 2, 2],
            "reps": [12, 10, 10, 8, 10, 8, 8, 6],
            "rep_to_pct_1rm": {
                6: 0.70,
                8: 0.66,
                10: 0.62,
                12: 0.58,
            },
        },
    },
}

# Backwards-compatible defaults
main_sets = PROGRAM_PRESCRIPTIONS["hypertrophy"]["main"]["sets"]
main_reps = PROGRAM_PRESCRIPTIONS["hypertrophy"]["main"]["reps"]
main_rep_to_pct_1rm = PROGRAM_PRESCRIPTIONS["hypertrophy"]["main"]["rep_to_pct_1rm"]

main_aux_sets = PROGRAM_PRESCRIPTIONS["hypertrophy"]["main_aux"]["sets"]
main_aux_reps = PROGRAM_PRESCRIPTIONS["hypertrophy"]["main_aux"]["reps"]
main_aux_rep_to_pct_1rm = PROGRAM_PRESCRIPTIONS["hypertrophy"]["main_aux"]["rep_to_pct_1rm"]

aux_sets = PROGRAM_PRESCRIPTIONS["hypertrophy"]["aux"]["sets"]
aux_reps = PROGRAM_PRESCRIPTIONS["hypertrophy"]["aux"]["reps"]
aux_rep_to_pct_1rm = PROGRAM_PRESCRIPTIONS["hypertrophy"]["aux"]["rep_to_pct_1rm"]

one_rm_conversion_key = {
    1: 1.00,
    2: 0.95,
    3: 0.93,
    4: 0.90,
    5: 0.875,
    6: 0.85,
    7: 0.825,
    8: 0.80,
    9: 0.775,
    10: 0.75,
    11: 0.725,
    12: 0.70,
}