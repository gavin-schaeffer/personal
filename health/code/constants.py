
round_to = 5

PROGRAM_PRESCRIPTIONS = {
    "hypertrophy": {
        "main": {
            "sets": [3, 3, 4, 2, 4, 4, 3, 2],
            "reps": [12, 10, 8, 15, 10, 8, 6, 12],
            "rep_to_pct_1rm": {
                6: 0.77,
                8: 0.72,
                10: 0.67,
                12: 0.62,
                15: 0.54,
            },
        },
        "main_aux": {
            "sets": [3, 3, 3, 2, 3, 4, 3, 2],
            "reps": [12, 10, 10, 15, 10, 8, 8, 12],
            "rep_to_pct_1rm": {
                8: 0.70,
                10: 0.65,
                12: 0.60,
                15: 0.52,
            },
        },
        "aux": {
            "sets": [2, 3, 3, 1, 3, 3, 2, 2],
            "reps": [15, 15, 12, 15, 12, 10, 10, 15],
            "rep_to_pct_1rm": {
                10: 0.60,
                12: 0.56,
                15: 0.48,
            },
        },
    },

    "strength": {
        "main": {
            "sets": [3, 4, 4, 2, 4, 5, 4, 2],
            "reps": [5, 4, 3, 5, 4, 3, 2, 3],
            "rep_to_pct_1rm": {
                2: 0.88,
                3: 0.84,
                4: 0.80,
                5: 0.76,
            },
        },
        "main_aux": {
            "sets": [3, 3, 4, 2, 3, 4, 3, 2],
            "reps": [8, 6, 6, 10, 6, 5, 5, 8],
            "rep_to_pct_1rm": {
                5: 0.78,
                6: 0.74,
                8: 0.68,
                10: 0.60,
            },
        },
        "aux": {
            "sets": [2, 2, 2, 1, 2, 3, 2, 1],
            "reps": [15, 12, 10, 15, 12, 10, 10, 15],
            "rep_to_pct_1rm": {
                10: 0.60,
                12: 0.55,
                15: 0.47,
            },
        },
    },

    "balanced": {
        "main": {
            "sets": [3, 4, 4, 2, 4, 4, 3, 2],
            "reps": [8, 6, 5, 10, 6, 5, 4, 6],
            "rep_to_pct_1rm": {
                4: 0.82,
                5: 0.78,
                6: 0.75,
                8: 0.70,
                10: 0.62,
            },
        },
        "main_aux": {
            "sets": [3, 3, 3, 2, 3, 3, 3, 2],
            "reps": [12, 10, 8, 12, 10, 8, 6, 10],
            "rep_to_pct_1rm": {
                6: 0.74,
                8: 0.69,
                10: 0.64,
                12: 0.58,
            },
        },
        "aux": {
            "sets": [2, 3, 3, 1, 3, 3, 2, 2],
            "reps": [15, 12, 12, 15, 12, 10, 10, 15],
            "rep_to_pct_1rm": {
                10: 0.59,
                12: 0.55,
                15: 0.48,
            },
        },
    },
}


ROLE_TO_PRESCRIPTION = {
    "main": "main",
    "auxiliary": "main_aux",
    "isolation": "aux",
}


REST_INTERVALS_SECONDS = {
    "main": 180,
    "main_aux": 120,
    "aux": 75,
}


TARGET_RIR_BY_GOAL = {
    "hypertrophy": {
        "main": [3, 2, 1, 4, 2, 1, 1, 3],
        "main_aux": [3, 2, 2, 4, 2, 1, 1, 3],
        "aux": [2, 2, 1, 4, 1, 1, 0, 3],
    },
    "strength": {
        "main": [3, 3, 2, 5, 2, 1, 1, 3],
        "main_aux": [3, 2, 2, 4, 2, 1, 1, 3],
        "aux": [3, 2, 2, 4, 2, 1, 1, 3],
    },
    "balanced": {
        "main": [3, 2, 2, 4, 2, 1, 1, 3],
        "main_aux": [3, 2, 2, 4, 2, 1, 1, 3],
        "aux": [2, 2, 1, 4, 1, 1, 1, 3],
    },
}


def get_program_prescription(training_goal: str, exercise_role: str):
    training_goal = (training_goal or "hypertrophy").lower().strip()
    exercise_role = (exercise_role or "aux").lower().strip()

    role_key = ROLE_TO_PRESCRIPTION.get(exercise_role, exercise_role)

    if training_goal not in PROGRAM_PRESCRIPTIONS:
        raise ValueError(
            f"training_goal must be one of: {list(PROGRAM_PRESCRIPTIONS.keys())}"
        )

    if role_key not in PROGRAM_PRESCRIPTIONS[training_goal]:
        raise ValueError(
            f"role_key must be one of: {list(PROGRAM_PRESCRIPTIONS[training_goal].keys())}"
        )

    return PROGRAM_PRESCRIPTIONS[training_goal][role_key]


one_rm_conversion_key = {
    1: 1.00,
    2: 0.97,
    3: 0.94,
    4: 0.92,
    5: 0.89,
    6: 0.86,
    7: 0.83,
    8: 0.81,
    9: 0.78,
    10: 0.75,
    11: 0.73,
    12: 0.71,
}
