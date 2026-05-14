def weight_kg_conversions(weight_input):
    return weight_input * 0.45359237

def height_cm_conversions(height_input):
    height_ft, height_in = map(int, height_input.split(","))
    height = height_ft + (height_in/12)
    height_m = height * 0.3048
    return height_m * 100