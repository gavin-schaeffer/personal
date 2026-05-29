program = {
    "Lose Agressive": {
        "tdee_percentage": 0.20,
        "carb_percentage": 0.40,
    },

    "Lose Moderate": {
        "tdee_percentage": 0.10,
        "carb_percentage": 0.45,
    },

    "Maintain": {
        "tdee_percentage": 0,
        "carb_percentage": 0.50,
    },
    
    "Gain Moderate": {
        "tdee_percentage": -0.075,
        "carb_percentage": 0.52,
    },

    "Gain Agressive": {
        "tdee_percentage": -0.15,
        "carb_percentage": 0.55,
    },
    
}

def calculate_adjusted_cal_plan(tdee, tdee_percentage):
    kcal = tdee - (tdee * tdee_percentage)
    return kcal

def calculate_macros(kcal,lean_body_mass, carb_percentage):
    protein_nutrients = lean_body_mass * 2.2 #protein in grams
    protein_calories = protein_nutrients * 4 # protein in kcal
    
    carb_calories = kcal * carb_percentage #carbs in kcal
    carb_nutrients = carb_calories / 4 #carbs in grams
    
    fat_calories = kcal - (protein_calories + carb_calories) #fat in kcal
    fat_nutrients = fat_calories / 9 #fats in grams

    fiber_nutrients = kcal * 0.014
    return protein_nutrients,  carb_nutrients, fat_nutrients, fiber_nutrients

def user_nutrition_plan(nutrition_goal, nutrition_goal_level):
    nutrition_goal = nutrition_goal.lower().strip()
    nutrition_goal_level = nutrition_goal_level.lower().strip()

    if nutrition_goal in ["l", "lose"]:
        if nutrition_goal_level in ["a", "agressive"]:
            tdee_percentage = program["Lose Agressive"]["tdee_percentage"]
            carb_percentage = program["Lose Agressive"]["carb_percentage"]
            goal_type_label = program["Lose Agressive"]
        elif nutrition_goal_level in ["m", "moderate"]:
            tdee_percentage = program["Lose Moderate"]["tdee_percentage"]
            carb_percentage = program["Lose Moderate"]["carb_percentage"]
            goal_type_label = program["Lose Moderate"]
    elif nutrition_goal in ["g", "gain"]:
        if nutrition_goal_level in ["a", "agressive"]:
            tdee_percentage = program["Gain Agressive"]["tdee_percentage"]
            carb_percentage = program["Gain Agressive"]["carb_percentage"]
            goal_type_label = program["Gain Agressive"]
        elif nutrition_goal_level in ["m", "moderate"]:
            tdee_percentage = program["Gain Moderate"]["tdee_percentage"]
            carb_percentage = program["Gain Moderate"]["carb_percentage"]
            goal_type_label = program["Gain Moderate"]
    elif nutrition_goal in ["m", "maintain"]:
        tdee_percentage = program["Maintain"]["tdee_percentage"]
        carb_percentage = program["Maintain"]["carb_percentage"]
        goal_type_label = program["Maintain"]

    else:
        raise ValueError("nutrition_goal must be lose, gain, or maintain or L, G, M &  nutrition_goal_level must be Agressive, Moderate or A, M")

    return tdee_percentage, carb_percentage, goal_type_label

def nutrition_table( tdee, lean_body_mass, goal_type_label, tdee_percentage, carb_percentage ):
    header = [["Goal Type", "Kcal", "Protein (g)", "Carbs (g)", "Fat (g)", "Fiber (g)"]]
    goal_label_matrix = goal_type_label
    kcal = calculate_adjusted_cal_plan(tdee, tdee_percentage)
    proteins, carbs, fat, fiber = calculate_macros(kcal, lean_body_mass, carb_percentage)

    return header, goal_label_matrix, kcal, proteins, carbs, fat, fiber