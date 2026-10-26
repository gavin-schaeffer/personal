from exercises import EXERCISES

E = EXERCISES

program = {
    "hypertrophy": {
        "advanced": {
            2: [
                [
                    E["back_squat"],
                    E["flat_press"],
                    E["pull_down"],
                    E["hamstring_curl"],
                    E["lateral_raises"],
                    E["calf_raises"],
                ],
                [
                    E["rdl"],
                    E["leg_press"],
                    E["incline_press"],
                    E["incline_bench_support_back_row"],
                    E["barbell_curl"],
                    E["tricep_pushdowns"],
                ],
            ],
            3: [
                [
                    E["back_squat"],
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["rdl"],
                    E["incline_press"],
                    E["pull_down"],
                    E["lateral_raises"],
                    E["barbell_curl"],
                ],
                [
                    E["leg_press"],
                    E["split_squat"],
                    E["flat_press"],
                    E["seated_cable_row"],
                    E["tricep_pushdowns"],
                    E["rear_delts"],
                ],
            ],
            4: [
                [
                    E["back_squat"],
                    E["rdl"],
                    E["leg_extension"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["pull_down"],
                    E["incline_bench_support_back_row"],
                    E["lateral_raises"],
                    E["tricep_pushdowns"],
                ],
                [
                    E["leg_press"],
                    E["split_squat"],
                    E["leg_extension"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["incline_press"],
                    E["shoulder_press"],
                    E["machine_row"],
                    E["rear_delts"],
                    E["barbell_curl"],
                ],
            ],
            5: [
                [
                    E["back_squat"],
                    E["rdl"],
                    E["leg_extension"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["pull_down"],
                    E["incline_bench_support_back_row"],
                    E["lateral_raises"],
                ],
                [
                    E["leg_press"],
                    E["split_squat"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["incline_press"],
                    E["shoulder_press"],
                    E["lateral_raises"],
                    E["tricep_pushdowns"],
                ],
                [
                    E["machine_row"],
                    E["pull_down"],
                    E["rear_delts"],
                    E["barbell_curl"],
                    E["pullovers"],
                ],
            ],
        },

        "easy": {
            2: [
                [
                    E["split_squat"],
                    E["flat_press"],
                    E["pull_down"],
                    E["hamstring_curl"],
                    E["lateral_raises"],
                    E["calf_raises"],
                ],
                [
                    E["rdl"],
                    E["leg_press"],
                    E["incline_press"],
                    E["seated_cable_row"],
                    E["barbell_curl"],
                    E["tricep_pushdowns"],
                ],
            ],
            3: [
                [
                    E["split_squat"],
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["leg_press"],
                    E["incline_press"],
                    E["pull_down"],
                    E["lateral_raises"],
                    E["barbell_curl"],
                ],
                [
                    E["rdl"],
                    E["goblet_squat"],
                    E["flat_press"],
                    E["seated_cable_row"],
                    E["tricep_pushdowns"],
                    E["rear_delts"],
                ],
            ],
            4: [
                [
                    E["split_squat"],
                    E["rdl"],
                    E["leg_extension"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["pull_down"],
                    E["incline_bench_support_back_row"],
                    E["lateral_raises"],
                    E["tricep_pushdowns"],
                ],
                [
                    E["leg_press"],
                    E["goblet_squat"],
                    E["leg_extension"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["incline_press"],
                    E["shoulder_press"],
                    E["machine_row"],
                    E["rear_delts"],
                    E["barbell_curl"],
                ],
            ],
            5: [
                [
                    E["split_squat"],
                    E["rdl"],
                    E["leg_extension"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["pull_down"],
                    E["incline_bench_support_back_row"],
                    E["lateral_raises"],
                ],
                [
                    E["leg_press"],
                    E["goblet_squat"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["incline_press"],
                    E["shoulder_press"],
                    E["lateral_raises"],
                    E["tricep_pushdowns"],
                ],
                [
                    E["machine_row"],
                    E["pull_down"],
                    E["rear_delts"],
                    E["barbell_curl"],
                    E["pullovers"],
                ],
            ],
        },
    },

    "strength": {
        "advanced": {
            2: [
                [
                    E["back_squat"],
                    E["flat_press"],
                    E["pull_down"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["deadlift"],
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["split_squat"],
                    E["close_grip_press"],
                ],
            ],
            3: [
                [
                    E["back_squat"],
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["hamstring_curl"],
                ],
                [
                    E["deadlift"],
                    E["shoulder_press"],
                    E["pull_down"],
                    E["split_squat"],
                ],
                [
                    E["flat_press"],
                    E["back_squat"],
                    E["machine_row"],
                    E["close_grip_press"],
                    E["barbell_curl"],
                ],
            ],
            4: [
                [
                    E["back_squat"],
                    E["rdl"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["shoulder_press"],
                    E["close_grip_press"],
                ],
                [
                    E["deadlift"],
                    E["leg_press"],
                    E["leg_extension"],
                    E["hamstring_curl"],
                ],
                [
                    E["flat_press"],
                    E["pull_down"],
                    E["machine_row"],
                    E["barbell_curl"],
                ],
            ],
            5: [
                [
                    E["back_squat"],
                    E["rdl"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["close_grip_press"],
                ],
                [
                    E["deadlift"],
                    E["pull_down"],
                    E["rear_delts"],
                    E["barbell_curl"],
                ],
                [
                    E["back_squat"],
                    E["leg_press"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["shoulder_press"],
                    E["machine_row"],
                    E["lateral_raises"],
                ],
            ],
        },

        "easy": {
            2: [
                [
                    E["split_squat"],
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["rdl"],
                    E["flat_press"],
                    E["leg_press"],
                    E["pull_down"],
                    E["close_grip_press"],
                ],
            ],
            3: [
                [
                    E["split_squat"],
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["hamstring_curl"],
                ],
                [
                    E["rdl"],
                    E["shoulder_press"],
                    E["pull_down"],
                    E["goblet_squat"],
                ],
                [
                    E["flat_press"],
                    E["leg_press"],
                    E["machine_row"],
                    E["close_grip_press"],
                    E["barbell_curl"],
                ],
            ],
            4: [
                [
                    E["split_squat"],
                    E["rdl"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["shoulder_press"],
                    E["close_grip_press"],
                ],
                [
                    E["leg_press"],
                    E["goblet_squat"],
                    E["leg_extension"],
                    E["hamstring_curl"],
                ],
                [
                    E["flat_press"],
                    E["pull_down"],
                    E["machine_row"],
                    E["barbell_curl"],
                ],
            ],
            5: [
                [
                    E["split_squat"],
                    E["rdl"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["close_grip_press"],
                ],
                [
                    E["leg_press"],
                    E["pull_down"],
                    E["rear_delts"],
                    E["barbell_curl"],
                ],
                [
                    E["split_squat"],
                    E["goblet_squat"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["shoulder_press"],
                    E["machine_row"],
                    E["lateral_raises"],
                ],
            ],
        },
    },

    "balanced": {
        "advanced": {
            2: [
                [
                    E["back_squat"],
                    E["flat_press"],
                    E["pull_down"],
                    E["hamstring_curl"],
                    E["lateral_raises"],
                    E["calf_raises"],
                ],
                [
                    E["rdl"],
                    E["incline_press"],
                    E["split_squat"],
                    E["incline_bench_support_back_row"],
                    E["barbell_curl"],
                    E["tricep_pushdowns"],
                ],
            ],
            3: [
                [
                    E["back_squat"],
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["rdl"],
                    E["shoulder_press"],
                    E["pull_down"],
                    E["split_squat"],
                    E["barbell_curl"],
                ],
                [
                    E["flat_press"],
                    E["leg_press"],
                    E["machine_row"],
                    E["lateral_raises"],
                    E["tricep_pushdowns"],
                ],
            ],
            4: [
                [
                    E["back_squat"],
                    E["rdl"],
                    E["leg_extension"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["pull_down"],
                    E["incline_bench_support_back_row"],
                    E["lateral_raises"],
                    E["tricep_pushdowns"],
                ],
                [
                    E["leg_press"],
                    E["split_squat"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["incline_press"],
                    E["machine_row"],
                    E["shoulder_press"],
                    E["rear_delts"],
                    E["barbell_curl"],
                ],
            ],
            5: [
                [
                    E["back_squat"],
                    E["rdl"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["pull_down"],
                    E["incline_bench_support_back_row"],
                    E["lateral_raises"],
                ],
                [
                    E["leg_press"],
                    E["split_squat"],
                    E["leg_extension"],
                    E["calf_raises"],
                ],
                [
                    E["incline_press"],
                    E["shoulder_press"],
                    E["lateral_raises"],
                    E["tricep_pushdowns"],
                ],
                [
                    E["machine_row"],
                    E["pull_down"],
                    E["rear_delts"],
                    E["barbell_curl"],
                    E["pullovers"],
                ],
            ],
        },

        "easy": {
            2: [
                [
                    E["split_squat"],
                    E["flat_press"],
                    E["pull_down"],
                    E["hamstring_curl"],
                    E["lateral_raises"],
                    E["calf_raises"],
                ],
                [
                    E["rdl"],
                    E["incline_press"],
                    E["leg_press"],
                    E["incline_bench_support_back_row"],
                    E["barbell_curl"],
                    E["tricep_pushdowns"],
                ],
            ],
            3: [
                [
                    E["split_squat"],
                    E["flat_press"],
                    E["incline_bench_support_back_row"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["rdl"],
                    E["shoulder_press"],
                    E["pull_down"],
                    E["goblet_squat"],
                    E["barbell_curl"],
                ],
                [
                    E["flat_press"],
                    E["leg_press"],
                    E["machine_row"],
                    E["lateral_raises"],
                    E["tricep_pushdowns"],
                ],
            ],
            4: [
                [
                    E["split_squat"],
                    E["rdl"],
                    E["leg_extension"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["pull_down"],
                    E["incline_bench_support_back_row"],
                    E["lateral_raises"],
                    E["tricep_pushdowns"],
                ],
                [
                    E["leg_press"],
                    E["goblet_squat"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["incline_press"],
                    E["machine_row"],
                    E["shoulder_press"],
                    E["rear_delts"],
                    E["barbell_curl"],
                ],
            ],
            5: [
                [
                    E["split_squat"],
                    E["rdl"],
                    E["hamstring_curl"],
                    E["calf_raises"],
                ],
                [
                    E["flat_press"],
                    E["pull_down"],
                    E["incline_bench_support_back_row"],
                    E["lateral_raises"],
                ],
                [
                    E["leg_press"],
                    E["goblet_squat"],
                    E["leg_extension"],
                    E["calf_raises"],
                ],
                [
                    E["incline_press"],
                    E["shoulder_press"],
                    E["lateral_raises"],
                    E["tricep_pushdowns"],
                ],
                [
                    E["machine_row"],
                    E["pull_down"],
                    E["rear_delts"],
                    E["barbell_curl"],
                    E["pullovers"],
                ],
            ],
        },
    },
}


def normalize_program_goal(goal_input):
    goal_input = (goal_input or "hypertrophy").lower().strip()

    if goal_input in ["h", "hypertrophy", "muscle", "build muscle", "bodybuilding"]:
        return "hypertrophy"

    if goal_input in ["s", "strength", "build strength", "power"]:
        return "strength"

    if goal_input in ["b", "balance", "balanced", "hybrid"]:
        return "balanced"

    raise ValueError("training goal must be one of: H/hypertrophy, S/strength, or B/balanced")


def normalize_rank(rank_input):
    rank_input = (rank_input or "").lower().strip()

    if rank_input in ["a", "advanced"]:
        return "advanced"

    if rank_input in ["e", "easy"]:
        return "easy"

    raise ValueError("rank_input must be one of: E/easy, A/advanced")


def user_program(rank_input, lifting_frequency_input, training_goal_input="hypertrophy"):
    goal_key = normalize_program_goal(training_goal_input)
    rank_key = normalize_rank(rank_input)

    if lifting_frequency_input not in program[goal_key][rank_key]:
        raise ValueError("lifting_frequency_input must be one of: 2, 3, 4, 5")

    return program[goal_key][rank_key][lifting_frequency_input]
