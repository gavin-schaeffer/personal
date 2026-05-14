round_to = 5

# ------- sets & reps: hypertrophy-first block with heavier week-8 test --------

main_sets      = [3, 4, 4, 3, 4, 4, 3, 2]
main_aux_sets  = [3, 3, 4, 3, 4, 3, 3, 2]
aux_sets       = [2, 3, 3, 2, 3, 3, 2, 2]

main_reps      = [10, 10, 8, 8, 8, 6, 6, 4]
main_aux_reps  = [12, 12, 10, 10, 10, 8, 8, 6]
aux_reps       = [15, 15, 12, 12, 12, 10, 10, 10]



# --- MAIN: heaviest / highest-skill / strength emphasis (multi-set friendly; not true RM %) ---
# Anchored near NSCA rep-max values, slightly reduced to allow multiple sets with quality. [1](https://www.nsca.com/contentassets/61d813865e264c6e852cadfe247eae52/nsca_training_load_chart.pdf)[2](https://tourniquets.org/wp-content/uploads/PDFs/ACSM-Progression-models-in-resistance-training-for-healthy-adults-2009.pdf)
main_rep_to_pct_1rm = {
    3: 0.93,
    4: 0.87,
    5: 0.85,
    6: 0.82,
    # hypertrophy zone
    7: 0.79,
    8: 0.76,
    9: 0.74,
    10: 0.72,
    11: 0.70,
    12: 0.68
}


# --- AUX: accessories / isolation / low systemic fatigue (hypertrophy; joint-friendly) ---
# Generally lighter again; great place for higher reps with short rest. [2](https://tourniquets.org/wp-content/uploads/PDFs/ACSM-Progression-models-in-resistance-training-for-healthy-adults-2009.pdf)
main_aux_rep_to_pct_1rm = {
    5: 0.87,
    6: 0.78,
    7: 0.76,
    8: 0.74,
    9: 0.72,
    10: 0.70,
    11: 0.68,
    12: 0.66
}


# --- If you’re estimating 1RM from a weight x reps set (rep-max style conversion) ---
# Matches standard rep-max relationships (NSCA-style). [1](https://www.nsca.com/contentassets/61d813865e264c6e852cadfe247eae52/nsca_training_load_chart.pdf)
aux_rep_to_pct_1rm = {
    3: 0.82,
    4: 0.79,
    5: 0.76,
    6: 0.74,
    7: 0.72,
    8: 0.80,
    9: 0.68,
    10: 0.66,
    11: 0.64,
    12: 0.62,
    13: 0.60,
    14: 0.58,
    15: 0.56
}


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
    12: 0.70    
}
