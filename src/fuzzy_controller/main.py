# Membership Functions
def triangular(x, a, b, c):
    if a < x < b:
        return (x - a) / (b - a)
    if b <= x < c:
        return (c - x) / (c - b)
    return 0


def trapezoidal(x, a, b, c, d):
    if a < x < b:
        return (x - a) / (b - a)
    if b <= x <= c:
        return 1
    if c < x < d:
        return (d - x) / (d - c)
    return 0


def get_membership(x, fuzzy_set):
    return trapezoidal(x, *fuzzy_set) if len(fuzzy_set) == 4 else triangular(x, *fuzzy_set)


# Fuzzy Sets and Rules
FUZZY_SETS = {
    "NL": [0, 0, 31, 61], "NM": [31, 61, 95], "NS": [61, 95, 127], "ZE": [95, 127, 159],
    "PS": [127, 159, 191], "PM": [159, 191, 223], "PL": [191, 223, 255, 255]
}

RULES = {
    1: ["NL", "ZE", "PL"], 2: ["ZE", "NL", "PL"], 3: ["NM", "ZE", "PM"], 4: ["NS", "PS", "PS"],
    5: ["PS", "NS", "NS"], 6: ["PL", "ZE", "NL"], 7: ["ZE", "NS", "PS"], 8: ["ZE", "NM", "PM"]
}

# Inputs
SPEED_DIFF = 100
ACCELERATION = 70


# Step 1: Fuzzification
def fuzzify(value, sets):
    return {k: get_membership(value, v) for k, v in sets.items()}


speed_fuzzy = fuzzify(SPEED_DIFF, FUZZY_SETS)
print("Speed Fuzzy Values:\n", speed_fuzzy, "\n")

accel_fuzzy = fuzzify(ACCELERATION, FUZZY_SETS)
print("Acceleration Fuzzy Values:\n", accel_fuzzy, "\n")


# Step 2: Apply Rules
# s = speed, a = acceleration, o = output
def apply_rules(speed_fuzzy, accel_fuzzy):
    return {i: (min(speed_fuzzy[s], accel_fuzzy[a]), o) for i, (s, a, o) in RULES.items() if
            min(speed_fuzzy[s], accel_fuzzy[a]) > 0}


rule_strengths = apply_rules(speed_fuzzy, accel_fuzzy)
print("Rule Strengths:\n", rule_strengths, "\n")


# Step 3: Calculate Areas
def calculate_areas(rule_strengths):
    areas, weighted_areas = {}, {}
    for i, (strength, out) in rule_strengths.items():
        set_vals = FUZZY_SETS[out]
        center = set_vals[1] if len(set_vals) == 3 else (set_vals[1] + set_vals[2]) / 2
        # Corrected area calculation
        if len(set_vals) == 4:  # Trapezoid
            base1 = set_vals[3] - set_vals[0]  # Full base
            base2 = set_vals[2] - set_vals[1]  # Top base
            area = strength * (base1 + base2) / 2
        else:  # Triangle
            base = set_vals[2] - set_vals[0]
            area = strength * base / 2
        areas[i] = area
        weighted_areas[i] = area * center
    return areas, weighted_areas


# Step 4: Defuzzify
def defuzzify(areas, weighted_areas):
    total_area = sum(areas.values())
    return sum(weighted_areas.values()) / total_area if total_area > 0 else 0


# Execute and Print
areas, weighted_areas = calculate_areas(rule_strengths)
throttle = defuzzify(areas, weighted_areas)

print(f"Throttle Output: {throttle:.2f}")
print("Speed Fuzzy:", {k: f"{v:.2f}" for k, v in speed_fuzzy.items() if v > 0})
print("Accel Fuzzy:", {k: f"{v:.2f}" for k, v in accel_fuzzy.items() if v > 0})
print("Rules:", {k: (f"{v[0]:.2f}", v[1]) for k, v in rule_strengths.items()})
print("Areas:", {k: f"{v:.2f}" for k, v in areas.items()})
print("Weighted Areas:", {k: f"{v:.2f}" for k, v in weighted_areas.items()})
