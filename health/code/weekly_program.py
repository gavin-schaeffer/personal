from exercises import EXERCISES

E = EXERCISES

program = {
    "hypertrophy": {
        "advanced": {
            2: [
                [E["back_squat"], E["rdl"], E["flat_press"], E["pull_down"], E["lateral_raises"], E["calf_raises"]],
                [E["leg_press"], E["split_squat"], E["incline_press"], E["machine_row"], E["hamstring_curl"], E["barbell_curl"], E["tricep_pushdowns"]],
            ],
            3: [
                [E["back_squat"], E["leg_press"], E["rdl"], E["leg_extension"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["shoulder_press"], E["seated_cable_row"], E["lateral_raises"], E["tricep_pushdowns"]],
                [E["incline_press"], E["machine_row"], E["split_squat"], E["hip_thrust"], E["rear_delts"], E["barbell_curl"]],
            ],
            4: [
                [E["back_squat"], E["leg_press"], E["split_squat"], E["leg_extension"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["shoulder_press"], E["seated_cable_row"], E["tricep_pushdowns"]],
                [E["rdl"], E["hip_thrust"], E["hamstring_curl"], E["leg_extension"], E["calf_raises"]],
                [E["incline_press"], E["machine_row"], E["pullovers"], E["lateral_raises"], E["rear_delts"], E["barbell_curl"]],
            ],
            5: [
                [E["back_squat"], E["leg_press"], E["split_squat"], E["leg_extension"], E["calf_raises"]],
                [E["flat_press"], E["shoulder_press"], E["lateral_raises"], E["tricep_pushdowns"], E["skull_crushers"]],
                [E["pull_down"], E["machine_row"], E["seated_cable_row"], E["rear_delts"], E["barbell_curl"]],
                [E["rdl"], E["hip_thrust"], E["hamstring_curl"], E["leg_extension"], E["calf_raises"]],
                [E["incline_press"], E["incline_bench_support_back_row"], E["pullovers"], E["lateral_raises"], E["close_grip_press"]],
            ],
        },

        "easy": {
            2: [
                [E["leg_press"], E["goblet_squat"], E["leg_extension"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["shoulder_press"], E["machine_row"], E["lateral_raises"], E["tricep_pushdowns"]],
            ],
            3: [
                [E["leg_press"], E["split_squat"], E["leg_extension"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["shoulder_press"], E["machine_row"], E["lateral_raises"]],
                [E["hip_thrust"], E["goblet_squat"], E["hamstring_curl"], E["incline_press"], E["seated_cable_row"], E["barbell_curl"]],
            ],
            4: [
                [E["leg_press"], E["split_squat"], E["leg_extension"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["shoulder_press"], E["tricep_pushdowns"]],
                [E["hip_thrust"], E["goblet_squat"], E["hamstring_curl"], E["calf_raises"]],
                [E["incline_press"], E["machine_row"], E["rear_delts"], E["barbell_curl"]],
            ],
            5: [
                [E["leg_press"], E["split_squat"], E["leg_extension"], E["calf_raises"]],
                [E["flat_press"], E["shoulder_press"], E["lateral_raises"], E["tricep_pushdowns"]],
                [E["pull_down"], E["machine_row"], E["rear_delts"], E["barbell_curl"]],
                [E["hip_thrust"], E["goblet_squat"], E["hamstring_curl"], E["calf_raises"]],
                [E["incline_press"], E["seated_cable_row"], E["pullovers"], E["lateral_raises"], E["skull_crushers"]],
            ],
        },

        "injured": {
            2: [
                [E["leg_press"], E["split_squat"], E["leg_extension"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["incline_bench_support_back_row"], E["lateral_raises"], E["rear_delts"]],
            ],
            3: [
                [E["split_squat"], E["leg_extension"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["incline_bench_support_back_row"], E["lateral_raises"]],
                [E["leg_press"], E["goblet_squat"], E["hip_thrust"], E["pullovers"], E["tricep_pushdowns"]],
            ],
            4: [
                [E["split_squat"], E["leg_extension"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["lateral_raises"], E["tricep_pushdowns"]],
                [E["leg_press"], E["goblet_squat"], E["hip_thrust"], E["calf_raises"]],
                [E["incline_bench_support_back_row"], E["pullovers"], E["rear_delts"], E["barbell_curl"]],
            ],
            5: [
                [E["split_squat"], E["leg_extension"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["lateral_raises"], E["tricep_pushdowns"]],
                [E["incline_bench_support_back_row"], E["pullovers"], E["rear_delts"], E["barbell_curl"]],
                [E["leg_press"], E["goblet_squat"], E["hip_thrust"], E["calf_raises"]],
                [E["incline_press"], E["machine_row"], E["lateral_raises"], E["skull_crushers"]],
            ],
        },
    },

    "strength": {
        "advanced": {
            2: [
                [E["back_squat"], E["flat_press"], E["barbell_back_row"], E["rdl"], E["close_grip_press"]],
                [E["deadlift"], E["shoulder_press"], E["pull_down"], E["leg_press"], E["barbell_curl"]],
            ],
            3: [
                [E["back_squat"], E["flat_press"], E["barbell_back_row"], E["hamstring_curl"]],
                [E["deadlift"], E["shoulder_press"], E["pull_down"], E["split_squat"]],
                [E["leg_press"], E["incline_press"], E["machine_row"], E["rdl"], E["tricep_pushdowns"]],
            ],
            4: [
                [E["back_squat"], E["leg_press"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["barbell_back_row"], E["shoulder_press"], E["tricep_pushdowns"]],
                [E["deadlift"], E["rdl"], E["split_squat"], E["leg_extension"]],
                [E["incline_press"], E["pull_down"], E["machine_row"], E["barbell_curl"]],
            ],
            5: [
                [E["back_squat"], E["leg_press"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["barbell_back_row"], E["close_grip_press"], E["tricep_pushdowns"]],
                [E["deadlift"], E["rdl"], E["pull_down"], E["barbell_curl"]],
                [E["leg_press"], E["split_squat"], E["leg_extension"], E["calf_raises"]],
                [E["shoulder_press"], E["incline_press"], E["machine_row"], E["rear_delts"]],
            ],
        },

        "easy": {
            2: [
                [E["leg_press"], E["flat_press"], E["pull_down"], E["hamstring_curl"], E["tricep_pushdowns"]],
                [E["split_squat"], E["shoulder_press"], E["machine_row"], E["leg_extension"], E["barbell_curl"]],
            ],
            3: [
                [E["leg_press"], E["split_squat"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["shoulder_press"], E["machine_row"]],
                [E["hip_thrust"], E["incline_press"], E["seated_cable_row"], E["leg_extension"], E["tricep_pushdowns"]],
            ],
            4: [
                [E["leg_press"], E["split_squat"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["shoulder_press"], E["tricep_pushdowns"]],
                [E["hip_thrust"], E["goblet_squat"], E["leg_extension"], E["calf_raises"]],
                [E["incline_press"], E["machine_row"], E["rear_delts"], E["barbell_curl"]],
            ],
            5: [
                [E["leg_press"], E["split_squat"], E["hamstring_curl"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["tricep_pushdowns"]],
                [E["machine_row"], E["shoulder_press"], E["rear_delts"], E["barbell_curl"]],
                [E["hip_thrust"], E["goblet_squat"], E["leg_extension"], E["calf_raises"]],
                [E["incline_press"], E["seated_cable_row"], E["lateral_raises"], E["skull_crushers"]],
            ],
        },

        "injured": {
            2: [
                [E["leg_press"], E["split_squat"], E["leg_extension"], E["hamstring_curl"]],
                [E["flat_press"], E["pull_down"], E["incline_bench_support_back_row"], E["lateral_raises"]],
            ],
            3: [
                [E["leg_press"], E["split_squat"], E["leg_extension"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["incline_bench_support_back_row"], E["tricep_pushdowns"]],
                [E["hip_thrust"], E["goblet_squat"], E["hamstring_curl"], E["barbell_curl"]],
            ],
            4: [
                [E["leg_press"], E["split_squat"], E["leg_extension"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["lateral_raises"], E["tricep_pushdowns"]],
                [E["hip_thrust"], E["goblet_squat"], E["hamstring_curl"], E["calf_raises"]],
                [E["incline_bench_support_back_row"], E["pullovers"], E["rear_delts"], E["barbell_curl"]],
            ],
            5: [
                [E["leg_press"], E["split_squat"], E["leg_extension"], E["calf_raises"]],
                [E["flat_press"], E["pull_down"], E["tricep_pushdowns"]],
                [E["incline_bench_support_back_row"], E["pullovers"], E["rear_delts"], E["barbell_curl"]],
                [E["hip_thrust"], E["goblet_squat"], E["hamstring_curl"], E["calf_raises"]],
                [E["incline_press"], E["machine_row"], E["lateral_raises"], E["skull_crushers"]],
            ],
        },
    },
}


def normalize_program_goal(goal_input):
    goal_input = (goal_input or "hypertrophy").lower().strip()

    if goal_input in ["h", "hypertrophy", "muscle", "build muscle"]:
        return "hypertrophy"

    if goal_input in ["s", "strength", "build strength"]:
        return "strength"

    raise ValueError("training goal must be one of: H/hypertrophy or S/strength")


def normalize_rank(rank_input):
    rank_input = rank_input.lower().strip()

    if rank_input in ["a", "advanced"]:
        return "advanced"

    if rank_input in ["e", "easy"]:
        return "easy"

    if rank_input in ["i", "injured"]:
        return "injured"

    raise ValueError("rank_input must be one of: E/easy, A/advanced, I/injured")


def user_program(rank_input, lifting_frequency_input, training_goal_input="hypertrophy"):
    goal_key = normalize_program_goal(training_goal_input)
    rank_key = normalize_rank(rank_input)

    if lifting_frequency_input not in program[goal_key][rank_key]:
        raise ValueError("lifting_frequency_input must be one of: 2, 3, 4, 5")

    return program[goal_key][rank_key][lifting_frequency_input]