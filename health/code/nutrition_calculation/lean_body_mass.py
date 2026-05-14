def lean_body_mass_calculation_kg (weight, body_fat, height, gender,training_age):
    #calc LBM with fat percentage
    fat_mass = weight * (body_fat/100)
    bf_LBM = weight - fat_mass
    #calculating base lean body mass
    if gender in ("M", "m"):
        boer_formular = 0.407 * weight + 0.267 * height - 19.2
        james_formula = 1.10 * weight - 128 * ((weight/height)**2)
        hume_formula = 0.32810 * weight + 0.33929 * height - 29.5336
        base_lbm = (boer_formular + james_formula + hume_formula)/ 3
    elif gender in ("F","f","Oth","oth"):
        boer_formular = 0.252 * weight + 0.473 * height - 48.3
        james_formula = 1.07 * weight - 148 * ((weight/height)**2)
        hume_formula = 0.29569 * weight + 0.41813 * height - 43.2933
        base_lbm = (boer_formular + james_formula + hume_formula)/ 3
    #factor in body fat
    base_lbm = (base_lbm + bf_LBM)/2

    #calculating training age effect
    t_max = 4 #in kg
    t = 3 #years
    training_effect = t_max * (1 - (2.718281828**(-training_age/t)))

    return base_lbm + training_effect

def lean_body_mass_calculation_lb():
    return lean_body_mass_calculation_kg ()/0.45359237