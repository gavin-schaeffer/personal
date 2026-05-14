def calculate_bmr (gender_input, age_input, weight, height, lean_body_mass_kg):
        #Calculating BMR via mifflin_st_jeor method
    if gender_input in ("M", "m"):
        mifflin_st_jeor = (10 * weight) + (6.25 * height)-(5 * age_input) + 5
    elif gender_input in ("F","f","Oth","oth"):
        mifflin_st_jeor = (10 * weight) + (6.25 * height)-(5 * age_input) + -161
    #print(mifflin_st_jeor)
    
    #calculating BMR via Harris Benedict equation
    if gender_input in ("M", "m"):
         harris_benedict = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age_input)
    elif gender_input in ("F","f","Oth","oth"):
         harris_benedict = 447.596 + (9.247 * weight) + (3.098 * height) - (4.330 * age_input)
    #print(harris_benedict)
    
    #calcuating BMR via Katch-mcardle formula
    katch_mcardle = 370 + (21.6 * lean_body_mass_kg)
    #print(katch_mcardle)

    #calcuating BMR via cunningham formula
    cunningham = 500 + (22 * lean_body_mass_kg)
    #print(cunningham)

    #calculating BMR via Owen equation
    if gender_input in ("M", "m"):
         owen = 879 + (10.2 * weight)
    elif gender_input in ("F","f","Oth","oth"):
         owen = 795 + (7.18 * weight)
    #print(owen)
    
    #Average BMR of the three methods
    return int(mifflin_st_jeor + harris_benedict + katch_mcardle + cunningham + owen)/5
