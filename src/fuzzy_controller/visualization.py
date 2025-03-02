import matplotlib.pyplot as plt

# Fuzzy Functions and Set Definitions
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
accel_fuzzy = fuzzify(ACCELERATION, FUZZY_SETS)


# Step 2: Apply Rules
def apply_rules(speed_fuzzy, accel_fuzzy):
    return {i: (min(speed_fuzzy[s], accel_fuzzy[a]), o) for i, (s, a, o) in RULES.items() if
            min(speed_fuzzy[s], accel_fuzzy[a]) > 0}


rule_strengths = apply_rules(speed_fuzzy, accel_fuzzy)


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


# Visualization Function to Plot Inputs, Membership Functions, and Outputs
def plot_graph(throttle, output_set):
    # Plot Membership Functions for Inputs
    fig, axs = plt.subplots(2, 1, figsize=(10, 8))

    for label, fuzzy_set in FUZZY_SETS.items():
        x = range(0, 256)  # Range of x-values
        y = [get_membership(val, fuzzy_set) for val in x]
        axs[0].plot(x, y, label=label)
    axs[0].set_title('Fuzzy Membership Functions for Inputs')
    axs[0].set_xlabel('Input Value')
    axs[0].set_ylabel('Membership Degree')
    axs[0].legend()

    # Plot Fuzzified Values for Speed and Acceleration
    axs[1].bar(speed_fuzzy.keys(), speed_fuzzy.values(), color='blue', alpha=0.7, label='Speed Fuzzy Values')
    axs[1].bar(accel_fuzzy.keys(), accel_fuzzy.values(), color='green', alpha=0.7, label='Acceleration Fuzzy Values')
    axs[1].set_title('Fuzzified Inputs')
    axs[1].set_xlabel('Fuzzy Sets')
    axs[1].set_ylabel('Membership Value')
    axs[1].legend()

    # Mark the throttle value on the graph
    axs[1].plot([throttle, throttle], [0, 1], 'k--', label=f'Throttle Output: {throttle:.2f}')
    axs[1].text(throttle + 5, 0.5, f'{output_set}', color='red', fontsize=12)

    plt.tight_layout()
    plt.show()


# Step 5: Calculate Areas and Defuzzification
areas, weighted_areas = calculate_areas(rule_strengths)
throttle = defuzzify(areas, weighted_areas)

# Display Results
print(f"Throttle Output: {throttle:.2f}")
print("Speed Fuzzy:", {k: f"{v:.2f}" for k, v in speed_fuzzy.items() if v > 0})
print("Accel Fuzzy:", {k: f"{v:.2f}" for k, v in accel_fuzzy.items() if v > 0})
print("Rules:", {k: (f"{v[0]:.2f}", v[1]) for k, v in rule_strengths.items()})
print("Areas:", {k: f"{v:.2f}" for k, v in areas.items()})
print("Weighted Areas:", {k: f"{v:.2f}" for k, v in weighted_areas.items()})

# Get output fuzzy set from the rule
output_set = RULES[1][2]  # Example: you can adapt this to get the output fuzzy set of the final rule

# Plot the graphs
plot_graph(throttle, output_set)
