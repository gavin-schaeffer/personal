def calculate_activity_factor(step_activity_input, job_type_input, sleep_score_input, body_fat_input,lifting_frequency_input, cardio_frequency_input):
    base = 1.2 #sedentary factor 
    #formula for adjusting the activity factor by the numbers of steps user takes on average
    if step_activity_input <= 5000:
        steps_adjust = 0
    elif 5000 < step_activity_input <= 7500:
        steps_adjust = 0.05
    elif 7500 < step_activity_input <= 10000:
        steps_adjust = 0.1
    elif step_activity_input > 10000:
        steps_adjust = 0.15

    #formula for adjusting the activity factor by the type of job the user has
    if job_type_input in ("Sedentary", "sedentary"):
         job_adjust = 0
    elif job_type_input in ("Moderate","moderate"):
         job_adjust = 0.05
    elif job_type_input in ("Active","active"):
         job_adjust = 0.1

    #formula for adjusting the activity factor by how much sleep the user gets on average
    if sleep_score_input <= 5:
        sleep_adjust = -0.03
    elif 5 < sleep_score_input <= 7:
        sleep_adjust = -0.015
    elif sleep_score_input > 7:
        sleep_adjust = 0
    
    #formula factoring in body fat percentage
    if body_fat_input <= 0.12:
        fm_adjust = +0.010
    elif body_fat_input <= 0.20:
        fm_adjust = 0.000
    elif body_fat_input <= 0.30:
        fm_adjust = -0.015
    elif body_fat_input <= 0.40:
        fm_adjust = -0.030
    else:
        fm_adjust = -0.050


    return base + (lifting_frequency_input * 0.02) + (cardio_frequency_input * 0.015) + steps_adjust + job_adjust + sleep_adjust + fm_adjust
