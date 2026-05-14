def calculate_adjusted_cal_plan(tdee):
    percentages = [0.22 , 0.125 , 0, -0.07, -0.18]
    tdee_matrix = []
    for percent in percentages:
        kcal = tdee - (tdee * percent)
        tdee_matrix.append(kcal)
    return tdee_matrix

def calculate_macros(kcal,lean_body_mass):
    protein_nutrients = lean_body_mass * 2.8 #protein in grams
    protein_calories = protein_nutrients * 4 # protein in kcal
    carb_calories = kcal * 0.5 #carbs in kcal
    carb_nutrients = carb_calories / 4 #carbs in grams
    fat_calories = kcal - (protein_calories + carb_calories) #fat in kcal
    fat_nutrients = fat_calories / 9 #fats in grams
    return kcal, protein_nutrients,  carb_nutrients, fat_nutrients

def matrix_goal_plan(tdee, lean_body_mass):
    user_matrix = [["Goal Type", "Kcal", "Protein (g)", "Carbs (g)", "Fat (g)"]]
    goal_label_matrix = [["Lose Agressive", "Lose Moderate", "Maintain", "Gain Moderate", "Gain Agressive"]]

    for i, kcal in enumerate(calculate_adjusted_cal_plan(tdee)):
        kcal, proteins, carbs, fat = calculate_macros(kcal,lean_body_mass)
        user_matrix.append([goal_label_matrix[0][i], round(kcal,0), round(proteins, 0), round(carbs, 0), round(fat, 0)])
    return user_matrix
