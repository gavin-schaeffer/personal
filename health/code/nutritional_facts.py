from itertools import product


def convert_macro(macro, meal_frequency):
    return macro / meal_frequency


def meal_table(kcal, proteins, carbs, fat, fiber, meal_frequency):
    header = [["Food", "Serving (g)", "Kcal", "Protein (g)", "Carbs (g)", "Fat (g)", "Fiber (g)"]]

    macro_plan = [kcal, proteins, carbs, fat, fiber]

    meal_macro_plan = []
    for macro in macro_plan:
        meal_macro_plan.append(convert_macro(macro, meal_frequency))

    return header, meal_macro_plan

MACRO_KEYS = ["kcal", "protein_g", "carbs_g", "fat_g", "fiber_g"]


def get_food_by_description(description):
    """
    Finds a food by its exact description.
    Searches through all food categories.
    """
    for category, food_list in foods.items():
        for food in food_list:
            if food["description"] == description:
                return food

    raise ValueError(f"Food not found: {description}")


def scale_food(food, grams):
    """
    Scales a food's nutrition facts to a specific gram amount.
    """
    scale = grams / food["serving_size_g"]

    return {
        "description": food["description"],
        "grams": round(grams, 1),
        "kcal": round(food["kcal"] * scale, 1),
        "protein_g": round(food["protein_g"] * scale, 1),
        "carbs_g": round(food["carbs_g"] * scale, 1),
        "fat_g": round(food["fat_g"] * scale, 1),
        "fiber_g": round(food["fiber_g"] * scale, 1),
    }


def total_meal(meal):
    """
    Totals the macros for a list of scaled foods.
    """
    totals = {
        "kcal": 0,
        "protein_g": 0,
        "carbs_g": 0,
        "fat_g": 0,
        "fiber_g": 0,
    }

    for item in meal:
        for key in totals:
            totals[key] += item[key]

    return {key: round(value, 1) for key, value in totals.items()}


def macro_difference(totals, targets):
    """
    Shows how far the meal is from the target macros.
    Positive means over target.
    Negative means under target.
    """
    return {
        key: round(totals[key] - targets[key], 1)
        for key in targets
    }


def meal_score(totals, targets, weights=None):
    """
    Scores how close a meal is to the target macros.
    Lower score is better.

    You can weight some macros more heavily than others.
    """
    if weights is None:
        weights = {
            "protein_g": 10,
            "fiber_g": 8,
            "carbs_g": 6,
            "kcal": 4,
            "fat_g": 2,
        }

    score = 0

    for key in targets:
        difference = totals[key] - targets[key]
        score += weights.get(key, 1) * abs(difference)

    return score


def build_meal(
    selected_food_descriptions,
    targets,
    min_grams=0,
    max_grams=300,
    step=25,
):
    """
    Tries different gram amounts for each selected food and returns
    the combination that best matches the target macros.

    selected_food_descriptions: list of food description strings
    targets: dictionary of target macros for the meal
    min_grams: minimum grams per food
    max_grams: maximum grams per food
    step: search step size in grams
    """

    selected_foods = [
        get_food_by_description(description)
        for description in selected_food_descriptions
    ]

    gram_options = range(min_grams, max_grams + step, step)

    best_meal = None
    best_totals = None
    best_difference = None
    best_score = float("inf")

    for gram_combo in product(gram_options, repeat=len(selected_foods)):
        meal = []

        for food, grams in zip(selected_foods, gram_combo):
            if grams > 0:
                meal.append(scale_food(food, grams))

        totals = total_meal(meal)

        score = meal_score(totals, targets)

        if score < best_score:
            best_score = score
            best_meal = meal
            best_totals = totals
            best_difference = macro_difference(totals, targets)

    return {
        "meal": best_meal,
        "totals": best_totals,
        "targets": targets,
        "difference": best_difference,
        "score": round(best_score, 1),
    }
def build_meal_with_custom_ranges(
    selected_food_descriptions,
    targets,
    gram_ranges=None,
    step=5,
):
    """
    Builds a meal using custom gram ranges per food.

    This is better than build_meal() because foods like olive oil
    should not search the same gram range as chicken or rice.
    """

    if gram_ranges is None:
        gram_ranges = {}

    selected_foods = [
        get_food_by_description(description)
        for description in selected_food_descriptions
    ]

    all_gram_options = []

    for food in selected_foods:
        low, high = gram_ranges.get(food["description"], (0, 300))
        all_gram_options.append(range(low, high + step, step))

    best_meal = None
    best_totals = None
    best_difference = None
    best_score = float("inf")

    for gram_combo in product(*all_gram_options):
        meal = []

        for food, grams in zip(selected_foods, gram_combo):
            if grams > 0:
                meal.append(scale_food(food, grams))

        totals = total_meal(meal)
        score = meal_score(totals, targets)

        if score < best_score:
            best_score = score
            best_meal = meal
            best_totals = totals
            best_difference = macro_difference(totals, targets)

    return {
        "meal": best_meal,
        "totals": best_totals,
        "targets": targets,
        "difference": best_difference,
        "score": round(best_score, 1),
    }

def print_meal_result(result):
    """
    Nicely prints the meal builder result.
    """
    print("Meal:")
    for item in result["meal"]:
        print(
            f"- {item['description']}: {item['grams']}g | "
            f"{item['kcal']} kcal, "
            f"{item['protein_g']}g protein, "
            f"{item['carbs_g']}g carbs, "
            f"{item['fat_g']}g fat, "
            f"{item['fiber_g']}g fiber"
        )

    print("\nTotals:")
    print(result["totals"])

    print("\nTargets:")
    print(result["targets"])

    print("\nDifference:")
    print(result["difference"])

protein = [
    {
        "description": "Chicken thighs, boneless skinless, raw",
        "serving_size_g": 113,
        "protein_g": 19,
        "carbs_g": 0,
        "fat_g": 9,
        "fiber_g": 0,
        "kcal": 158,
    },
    {
        "description": "Chicken breast, boneless skinless, raw",
        "serving_size_g": 113,
        "protein_g": 25,
        "carbs_g": 0,
        "fat_g": 2,
        "fiber_g": 0,
        "kcal": 120,
    },
    {
        "description": "Beef sirloin roast, raw",
        "serving_size_g": 113,
        "protein_g": 24,
        "carbs_g": 0,
        "fat_g": 6,
        "fiber_g": 0,
        "kcal": 150,
    },
    {
        "description": "Ground beef, 96% lean, raw",
        "serving_size_g": 113,
        "protein_g": 24,
        "carbs_g": 0,
        "fat_g": 4,
        "fiber_g": 0,
        "kcal": 140,
    },
    {
        "description": "Ground beef, 90% lean, raw",
        "serving_size_g": 113,
        "protein_g": 22,
        "carbs_g": 0,
        "fat_g": 11,
        "fiber_g": 0,
        "kcal": 200,
    },
    {
        "description": "Beef ribeye steak, raw",
        "serving_size_g": 113,
        "protein_g": 21,
        "carbs_g": 0,
        "fat_g": 17,
        "fiber_g": 0,
        "kcal": 240,
    },
    {
        "description": "Eye of round steak, raw",
        "serving_size_g": 113,
        "protein_g": 25,
        "carbs_g": 0,
        "fat_g": 4,
        "fiber_g": 0,
        "kcal": 140,
    },
    {
        "description": "Pork loin, raw",
        "serving_size_g": 113,
        "protein_g": 24,
        "carbs_g": 0,
        "fat_g": 4,
        "fiber_g": 0,
        "kcal": 135,
    },
    {
        "description": "Pork shoulder, raw",
        "serving_size_g": 113,
        "protein_g": 20,
        "carbs_g": 0,
        "fat_g": 18,
        "fiber_g": 0,
        "kcal": 250,
    },
    {
        "description": "Beef skirt steak, raw",
        "serving_size_g": 113,
        "protein_g": 22,
        "carbs_g": 0,
        "fat_g": 12,
        "fiber_g": 0,
        "kcal": 200,
    },
    {
        "description": "Turkey breast, raw",
        "serving_size_g": 113,
        "protein_g": 26,
        "carbs_g": 0,
        "fat_g": 1,
        "fiber_g": 0,
        "kcal": 120,
    },
    {
        "description": "Turkey thighs, raw",
        "serving_size_g": 113,
        "protein_g": 22,
        "carbs_g": 0,
        "fat_g": 8,
        "fiber_g": 0,
        "kcal": 165,
    },
    {
        "description": "Pork tenderloin, raw",
        "serving_size_g": 113,
        "protein_g": 24,
        "carbs_g": 0,
        "fat_g": 3,
        "fiber_g": 0,
        "kcal": 125,
    },
    {
        "description": "Pork chop, lean, raw",
        "serving_size_g": 113,
        "protein_g": 24,
        "carbs_g": 0,
        "fat_g": 5,
        "fiber_g": 0,
        "kcal": 145,
    },
    {
        "description": "Top round steak, raw",
        "serving_size_g": 113,
        "protein_g": 25,
        "carbs_g": 0,
        "fat_g": 5,
        "fiber_g": 0,
        "kcal": 150,
    },
    {
        "description": "Bottom round steak, raw",
        "serving_size_g": 113,
        "protein_g": 24,
        "carbs_g": 0,
        "fat_g": 6,
        "fiber_g": 0,
        "kcal": 160,
    },
    {
        "description": "Beef tenderloin, raw",
        "serving_size_g": 113,
        "protein_g": 23,
        "carbs_g": 0,
        "fat_g": 9,
        "fiber_g": 0,
        "kcal": 180,
    },
    {
        "description": "Lean ground turkey, 93%, raw",
        "serving_size_g": 113,
        "protein_g": 22,
        "carbs_g": 0,
        "fat_g": 8,
        "fiber_g": 0,
        "kcal": 170,
    },
    {
        "description": "Extra lean ground turkey, 99%, raw",
        "serving_size_g": 113,
        "protein_g": 26,
        "carbs_g": 0,
        "fat_g": 1,
        "fiber_g": 0,
        "kcal": 120,
    },
    {
        "description": "Chicken tenderloins, raw",
        "serving_size_g": 113,
        "protein_g": 25,
        "carbs_g": 0,
        "fat_g": 1,
        "fiber_g": 0,
        "kcal": 110,
    },
    {
        "description": "Egg, large",
        "serving_size_g": 50,
        "protein_g": 6,
        "carbs_g": 0,
        "fat_g": 5,
        "fiber_g": 0,
        "kcal": 72,
    },
    {
        "description": "Fage Total 0% Greek yogurt",
        "serving_size_g": 170,
        "protein_g": 18,
        "carbs_g": 5,
        "fat_g": 0,
        "fiber_g": 0,
        "kcal": 90,
    },
    {
        "description": "Fage Total 2% Greek yogurt",
        "serving_size_g": 170,
        "protein_g": 17,
        "carbs_g": 5,
        "fat_g": 4,
        "fiber_g": 0,
        "kcal": 120,
    },
    {
        "description": "Mozzarella cheese",
        "serving_size_g": 28,
        "protein_g": 6,
        "carbs_g": 1,
        "fat_g": 6,
        "fiber_g": 0,
        "kcal": 85,
    },
]


carbs = [
    {
        "description": "Sweet potato, raw",
        "serving_size_g": 100,
        "protein_g": 2,
        "carbs_g": 20,
        "fat_g": 0,
        "fiber_g": 3,
        "kcal": 86,
    },
    {
        "description": "White potato, raw",
        "serving_size_g": 100,
        "protein_g": 2,
        "carbs_g": 17,
        "fat_g": 0,
        "fiber_g": 2,
        "kcal": 77,
    },
    {
        "description": "White rice, dry",
        "serving_size_g": 45,
        "protein_g": 3,
        "carbs_g": 36,
        "fat_g": 0,
        "fiber_g": 1,
        "kcal": 160,
    },
    {
        "description": "Pasta, dry",
        "serving_size_g": 56,
        "protein_g": 7,
        "carbs_g": 42,
        "fat_g": 1,
        "fiber_g": 2,
        "kcal": 200,
    },
    {
        "description": "Plain bagel",
        "serving_size_g": 105,
        "protein_g": 11,
        "carbs_g": 55,
        "fat_g": 1,
        "fiber_g": 2,
        "kcal": 277,
    },
    {
        "description": "Honey",
        "serving_size_g": 10,
        "protein_g": 0,
        "carbs_g": 8,
        "fat_g": 0,
        "fiber_g": 0,
        "kcal": 30,
    },
    {
        "description": "Dates, Medjool",
        "serving_size_g": 24,
        "protein_g": 0,
        "carbs_g": 18,
        "fat_g": 0,
        "fiber_g": 2,
        "kcal": 66,
    },
    {
        "description": "Cocoa powder, unsweetened",
        "serving_size_g": 5,
        "protein_g": 1,
        "carbs_g": 3,
        "fat_g": 1,
        "fiber_g": 2,
        "kcal": 12,
    },
    {
        "description": "Black beans, cooked",
        "serving_size_g": 100,
        "protein_g": 9,
        "carbs_g": 24,
        "fat_g": 1,
        "fiber_g": 9,
        "kcal": 132,
    },
    {
        "description": "Lentils, cooked",
        "serving_size_g": 100,
        "protein_g": 9,
        "carbs_g": 20,
        "fat_g": 0,
        "fiber_g": 8,
        "kcal": 116,
    },
    {
        "description": "Chickpeas, cooked",
        "serving_size_g": 100,
        "protein_g": 9,
        "carbs_g": 27,
        "fat_g": 3,
        "fiber_g": 8,
        "kcal": 164,
    },
    {
        "description": "Oats, dry",
        "serving_size_g": 40,
        "protein_g": 5,
        "carbs_g": 27,
        "fat_g": 3,
        "fiber_g": 4,
        "kcal": 150,
    },
    {
        "description": "Chia seeds",
        "serving_size_g": 28,
        "protein_g": 5,
        "carbs_g": 12,
        "fat_g": 9,
        "fiber_g": 10,
        "kcal": 138,
    },
    {
        "description": "Ground flaxseed",
        "serving_size_g": 14,
        "protein_g": 3,
        "carbs_g": 4,
        "fat_g": 6,
        "fiber_g": 4,
        "kcal": 75,
    },
]


vegetables = [
    {
        "description": "Broccoli, raw",
        "serving_size_g": 100,
        "protein_g": 3,
        "carbs_g": 7,
        "fat_g": 0,
        "fiber_g": 3,
        "kcal": 34,
    },
    {
        "description": "Tomato, raw",
        "serving_size_g": 123,
        "protein_g": 1,
        "carbs_g": 5,
        "fat_g": 0,
        "fiber_g": 2,
        "kcal": 22,
    },
    {
        "description": "Zucchini, raw",
        "serving_size_g": 100,
        "protein_g": 1,
        "carbs_g": 3,
        "fat_g": 0,
        "fiber_g": 1,
        "kcal": 17,
    },
    {
        "description": "Jalapeño pepper, raw",
        "serving_size_g": 14,
        "protein_g": 0,
        "carbs_g": 1,
        "fat_g": 0,
        "fiber_g": 0,
        "kcal": 4,
    },
    {
        "description": "Bell pepper, raw",
        "serving_size_g": 164,
        "protein_g": 2,
        "carbs_g": 10,
        "fat_g": 0,
        "fiber_g": 3,
        "kcal": 43,
    },
    {
        "description": "Mushrooms, white, raw",
        "serving_size_g": 100,
        "protein_g": 3,
        "carbs_g": 3,
        "fat_g": 0,
        "fiber_g": 1,
        "kcal": 22,
    },
    {
        "description": "Eggplant, raw",
        "serving_size_g": 100,
        "protein_g": 1,
        "carbs_g": 6,
        "fat_g": 0,
        "fiber_g": 3,
        "kcal": 25,
    },
    {
        "description": "Red sauce, no sugar added",
        "serving_size_g": 125,
        "protein_g": 2,
        "carbs_g": 10,
        "fat_g": 1,
        "fiber_g": 3,
        "kcal": 60,
    },
    {
        "description": "Green peas, raw",
        "serving_size_g": 100,
        "protein_g": 5,
        "carbs_g": 14,
        "fat_g": 0,
        "fiber_g": 5,
        "kcal": 81,
    },
    {
        "description": "Artichoke hearts",
        "serving_size_g": 100,
        "protein_g": 3,
        "carbs_g": 11,
        "fat_g": 0,
        "fiber_g": 5,
        "kcal": 47,
    },
    {
        "description": "Cabbage, raw",
        "serving_size_g": 100,
        "protein_g": 1,
        "carbs_g": 6,
        "fat_g": 0,
        "fiber_g": 3,
        "kcal": 25,
    },
]


fruits = [
    {
        "description": "Avocado, raw",
        "serving_size_g": 100,
        "protein_g": 2,
        "carbs_g": 9,
        "fat_g": 15,
        "fiber_g": 7,
        "kcal": 160,
    },
    {
        "description": "Strawberries, raw",
        "serving_size_g": 100,
        "protein_g": 1,
        "carbs_g": 8,
        "fat_g": 0,
        "fiber_g": 2,
        "kcal": 32,
    },
    {
        "description": "Apple, raw, medium",
        "serving_size_g": 182,
        "protein_g": 0,
        "carbs_g": 25,
        "fat_g": 0,
        "fiber_g": 4,
        "kcal": 95,
    },
    {
        "description": "Kiwi, raw",
        "serving_size_g": 69,
        "protein_g": 1,
        "carbs_g": 10,
        "fat_g": 0,
        "fiber_g": 2,
        "kcal": 42,
    },
    {
        "description": "Banana, raw, medium",
        "serving_size_g": 118,
        "protein_g": 1,
        "carbs_g": 27,
        "fat_g": 0,
        "fiber_g": 3,
        "kcal": 105,
    },
    {
        "description": "Blueberries, raw",
        "serving_size_g": 100,
        "protein_g": 1,
        "carbs_g": 14,
        "fat_g": 0,
        "fiber_g": 2,
        "kcal": 57,
    },
    {
        "description": "Raspberries, raw",
        "serving_size_g": 100,
        "protein_g": 1,
        "carbs_g": 12,
        "fat_g": 1,
        "fiber_g": 7,
        "kcal": 52,
    },
    {
        "description": "Blackberries, raw",
        "serving_size_g": 100,
        "protein_g": 1,
        "carbs_g": 10,
        "fat_g": 0,
        "fiber_g": 5,
        "kcal": 43,
    },
    {
        "description": "Pear, raw, medium",
        "serving_size_g": 178,
        "protein_g": 1,
        "carbs_g": 27,
        "fat_g": 0,
        "fiber_g": 6,
        "kcal": 101,
    },
    {
        "description": "Orange, raw, medium",
        "serving_size_g": 131,
        "protein_g": 1,
        "carbs_g": 15,
        "fat_g": 0,
        "fiber_g": 3,
        "kcal": 62,
    },
]


fats = [
    {
        "description": "Olive oil",
        "serving_size_g": 6.8,
        "protein_g": 0,
        "carbs_g": 0,
        "fat_g": 7,
        "fiber_g": 0,
        "kcal": 60,
    },
    {
        "description": "Coconut oil",
        "serving_size_g": 14,
        "protein_g": 0,
        "carbs_g": 0,
        "fat_g": 14,
        "fiber_g": 0,
        "kcal": 120,
    },
    {
        "description": "Cream cheese",
        "serving_size_g": 14.5,
        "protein_g": 1,
        "carbs_g": 1,
        "fat_g": 5,
        "fiber_g": 0,
        "kcal": 51,
    },
]


foods = {
    "protein": protein,
    "carbs": carbs,
    "vegetables": vegetables,
    "fruits": fruits,
    "fats": fats,
}