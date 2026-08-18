from exercises import EXERCISES

# Helper alias for code cleanliness
E = EXERCISES

program = {
    # =========================================================================
    # ADVANCED: High neural intensity, compound focus, optimized volume/freq
    # =========================================================================
    "advanced": {
        2: [
            # Lower (Quad/Hamstring balanced)
            [E["back_squat"], E["split_squat"], E["leg_curl"], E["calf_raises"]],
            # Upper (Push/Pull balanced)
            [E["flat_bench"], E["pull_down"], E["shoulder_press"], E["barbell_curl"]],
        ],
        3: [
            # Lower A (Quad Emphasis)
            [E["back_squat"], E["split_squat"], E["leg_extension"], E["calf_raises"]],
            # Upper A (Push/Pull)
            [E["flat_bench"], E["pull_down"], E["shoulder_press"], E["lateral_raises"]],
            # Lower B (Posterior Chain Emphasis)
            [E["rdl"], E["split_squat"], E["leg_curl"], E["calf_raises"]],
        ],
        4: [
            # Lower A (Squat focus)
            [E["back_squat"], E["split_squat"], E["leg_extension"], E["calf_raises"]],
            # Upper A (Horizontal Push/Vertical Pull)
            [E["flat_bench"], E["pull_down"], E["shoulder_press"], E["tricep_pushdowns"]],
            # Lower B (Hinge/Posterior focus)
            [E["deadlift"], E["split_squat"], E["leg_curl"], E["calf_raises"]],
            # Upper B (Vertical Push/Horizontal Pull)
            [E["incline_bench"], E["machine_row"], E["rear_delts"], E["barbell_curl"]],
        ],
        5: [
            # Day 1: Lower Quad Heavy
            [E["back_squat"], E["split_squat"], E["leg_extension"], E["calf_raises"]],
            # Day 2: Push Focus
            [E["flat_bench"], E["shoulder_press"], E["lateral_raises"], E["tricep_pushdowns"]],
            # Day 3: Pull Focus
            [E["deadlift"], E["pull_down"], E["seated_cable_row"], E["barbell_curl"]],
            # Day 4: Lower Posterior Heavy
            [E["rdl"], E["split_squat"], E["leg_curl"], E["calf_raises"]],
            # Day 5: Upper Auxiliary/Hypertrophy
            [E["incline_bench"], E["seated_cable_row"], E["lateral_raises"], E["skull_crushers"], E["barbell_curl"]],
        ],
    },

    # =========================================================================
    # EASY: Lower technical difficulty, stable machine focus, lower fatigue
    # =========================================================================
    "easy": {
        2: [
            [E["split_squat"], E["leg_extension"], E["leg_curl"], E["calf_raises"]],
            [E["flat_bench"], E["pull_down"], E["shoulder_press"], E["lateral_raises"]],
        ],
        3: [
            [E["split_squat"], E["leg_extension"], E["leg_curl"], E["calf_raises"]],
            [E["flat_bench"], E["pull_down"], E["shoulder_press"], E["tricep_pushdowns"]],
            [E["rdl"], E["split_squat"], E["leg_curl"], E["calf_raises"]],
        ],
        4: [
            [E["split_squat"], E["leg_extension"], E["leg_curl"], E["calf_raises"]],
            [E["flat_bench"], E["shoulder_press"], E["lateral_raises"], E["tricep_pushdowns"]],
            [E["rdl"], E["split_squat"], E["leg_curl"], E["calf_raises"]],
            [E["pull_down"], E["incline_bench_support_back_row"], E["rear_delts"], E["barbell_curl"]],
        ],
        5: [
            [E["back_squat"], E["leg_extension"], E["leg_curl"], E["calf_raises"]],
            [E["flat_bench"], E["shoulder_press"], E["lateral_raises"], E["tricep_pushdowns"]],
            [E["seated_cable_row"], E["pull_down"], E["incline_bench_support_back_row"], E["barbell_curl"]],
            [E["split_squat"], E["rdl"], E["leg_curl"], E["calf_raises"]],
            [E["incline_bench"], E["seated_cable_row"], E["lateral_raises"], E["tricep_pushdowns"], E["barbell_curl"]],
        ],
    },

    # =========================================================================
    # INJURED: Pelvic-floor friendly, spine-sparing, minimal intra-abdominal pressure
    # =========================================================================
    "injured": {
        2: [
            [E["split_squat"], E["leg_extension"], E["leg_curl"], E["calf_raises"]],
            [E["flat_bench"], E["pull_down"], E["shoulder_press"], E["lateral_raises"]],
        ],
        3: [
            [E["split_squat"], E["leg_extension"], E["leg_curl"], E["calf_raises"]],
            [E["flat_bench"], E["pull_down"], E["shoulder_press"], E["lateral_raises"]],
            [E["split_squat"], E["leg_curl"], E["leg_extension"], E["calf_raises"]],
        ],
        4: [
            [E["split_squat"], E["leg_extension"], E["leg_curl"], E["calf_raises"]],
            [E["flat_bench"], E["shoulder_press"], E["lateral_raises"], E["tricep_pushdowns"]],
            [E["split_squat"], E["leg_curl"], E["leg_extension"], E["calf_raises"]],
            [E["pull_down"], E["incline_bench_support_back_row"], E["rear_delts"], E["barbell_curl"]],
        ],
        5: [
            [E["split_squat"], E["leg_extension"], E["leg_curl"], E["calf_raises"]],
            [E["flat_bench"], E["shoulder_press"], E["lateral_raises"], E["tricep_pushdowns"]],
            [E["pull_down"], E["incline_bench_support_back_row"], E["rear_delts"], E["barbell_curl"]],
            [E["split_squat"], E["leg_curl"], E["leg_extension"], E["calf_raises"]],
            [E["incline_bench"], E["pullovers"], E["lateral_raises"], E["tricep_pushdowns"]],
        ],
    },
}


def user_program(rank_input, lifting_frequency_input):
    rank_input = rank_input.lower().strip()

    if rank_input in ["a", "advanced"]:
        selected_program = program["advanced"][lifting_frequency_input]

    elif rank_input in ["e", "easy"]:
        selected_program = program["easy"][lifting_frequency_input]

    elif rank_input in ["i", "injured"]:
        selected_program = program["injured"][lifting_frequency_input]

    else:
        raise ValueError("rank_input must be one of: E/easy, A/advanced, I/injured")

    return selected_program