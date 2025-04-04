def trapezoidal(x, a, b, c, d):
    if a < x < b:
        return (x - a) / (b - a)
    elif b <= x <= c:
        return 1
    elif c < x < d:
        return (d - x) / (d - c)
    else:
        return 0


def triangular(x, a, b, c):
    if a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    else:
        return 0


def get_membership(x, fuzzy_set):
    return trapezoidal(x, *fuzzy_set) if len(fuzzy_set) == 4 else triangular(x, *fuzzy_set)


FUZZY_SETS = {
    "LOW": [0.0, 0.0, 0.1, 0.3],
    "MLL": [0.1, 0.3, 0.5],
    "MED": [0.3, 0.5, 0.7],
    "MLH": [0.5, 0.7, 0.9],
    "HIGH": [0.7, 0.9, 1.0, 1.0]
}

RULES = {
    1: ["LOW", "LOW", "MED"],
    2: ["LOW", "MLL", "MLH"],
    3: ["LOW", "MED", "MLH"],
    4: ["LOW", "MLH", "HIGH"],
    5: ["LOW", "HIGH", "HIGH"],

    6: ["MLL", "LOW", "MLL"],
    7: ["MLL", "MLL", "MED"],
    8: ["MLL", "MED", "MLH"],
    9: ["MLL", "MLH", "MLH"],
    10: ["MLL", "HIGH", "HIGH"],

    11: ["MED", "LOW", "MLL"],
    12: ["MED", "MLL", "MLL"],
    13: ["MED", "MED", "MED"],
    14: ["MED", "MLH", "MLH"],
    15: ["MED", "HIGH", "MLH"],

    16: ["MLH", "LOW", "LOW"],
    17: ["MLH", "MLL", "MLL"],
    18: ["MLH", "MED", "MLL"],
    19: ["MLH", "MLH", "MED"],
    20: ["MLH", "HIGH", "MLH"],

    21: ["HIGH", "LOW", "LOW"],
    22: ["HIGH", "MLL", "LOW"],
    23: ["HIGH", "MED", "MLL"],
    24: ["HIGH", "MLH", "MLL"],
    25: ["HIGH", "HIGH", "MED"],
}

ACCURACY = 0.45
TIME = 0.57


def fuzzify(value, sets):
    return {k: get_membership(value, v) for k, v in sets.items()}


accuracy_fuzzy = fuzzify(ACCURACY, FUZZY_SETS)
time_fuzzy = fuzzify(TIME, FUZZY_SETS)


def apply_rules(accuracy_fuzzy, time_fuzzy):
    return {
        i: (min(accuracy_fuzzy[s], time_fuzzy[a]), o)
        for i, (s, a, o) in RULES.items()
        if min(accuracy_fuzzy[s], time_fuzzy[a]) > 0
    }


rule_strengths = apply_rules(accuracy_fuzzy, time_fuzzy)


def calculate_areas(rule_strengths):
    areas, weighted_areas = {}, {}
    for i, (strength, out) in rule_strengths.items():
        set_vals = FUZZY_SETS[out]
        center = set_vals[1] if len(set_vals) == 3 else (set_vals[1] + set_vals[2]) / 2
        if len(set_vals) == 4:
            base1 = set_vals[3] - set_vals[0]
            base2 = set_vals[2] - set_vals[1]
            area = strength * (base1 + base2) / 2
        else:
            base = set_vals[2] - set_vals[0]
            area = strength * base / 2
        areas[i] = area
        weighted_areas[i] = area * center
    return areas, weighted_areas


def defuzzify(areas, weighted_areas):
    total_area = sum(areas.values())
    return sum(weighted_areas.values()) / total_area if total_area > 0 else 0


areas, weighted_areas = calculate_areas(rule_strengths)
difficulty = defuzzify(areas, weighted_areas)

print(f"\n\nInputs:\n\tAccuracy = {ACCURACY}\n\tAnswer Time = {TIME}\n")
print(f"Output:\n\tDifficulty = {difficulty:.2f}\n\n")

print("Accuracy Fuzzy Values")
print(f"Crisp Value of Accuracy: {ACCURACY}")
print("Fuzzy Set\tMembership Value")
for k, v in accuracy_fuzzy.items():
    print(f"{k}\t\t{v:.2f}")
print("\n")

print("Answer Time Fuzzy Values")
print(f"Crisp Value of Answer Time: {TIME}")
print("Fuzzy Set\tMembership Value")
for k, v in time_fuzzy.items():
    print(f"{k}\t\t{v:.2f}")
print("\n")

print("Rule Strengths (only non-zero)")
print("Rule No.\tFuzzy Set\tStrength")
for k, (strength, fuzzy_set) in rule_strengths.items():
    print(f"{k}\t\t{fuzzy_set}\t\t{strength:.2f}")
print("\n")

print("Area Values")
print("Rule No.\tArea Value")
for k, v in areas.items():
    print(f"{k}\t\t{v:.2f}")
print("\n")

print("Weighted Areas Values")
print("Rule No.\tWeighted Value")
for k, v in weighted_areas.items():
    print(f"{k}\t\t{v:.2f}")
print("\n")

print(f"Defuzzified Crisp Value of Difficulty is {difficulty:.2f}\n")
