import numpy as np
from tabulate import tabulate

# Define HMM parameters
states = ["H", "L"]
sequence = "GGCA"
T = len(sequence)

# Start, Transition, and Emission probabilities
start_prob = {"H": 0.5, "L": 0.5}
transition_prob = {"H": {"H": 0.5, "L": 0.5}, "L": {"H": 0.4, "L": 0.6}}
emission_prob = {
    "H": {"A": 0.2, "C": 0.3, "G": 0.3, "T": 0.2},
    "L": {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3}
}

# Initialize Forward probability table (alpha)
alpha = np.zeros((len(states), T))

# Step 1: Initialization
for i, state in enumerate(states):
    alpha[i, 0] = start_prob[state] * emission_prob[state][sequence[0]]

# Step 2: Recursion
for t in range(1, T):
    for i, state in enumerate(states):
        alpha[i, t] = sum(
            alpha[j, t - 1] * transition_prob[prev_state][state]
            for j, prev_state in enumerate(states)
        ) * emission_prob[state][sequence[t]]

# Step 3: Compute final probability
final_prob = np.sum(alpha[:, -1])

# Convert Forward Table to a readable format
table_data = [["State"] + list(sequence)]
for i, state in enumerate(states):
    table_data.append([state] + [f"{alpha[i, t]:.6f}" for t in range(T)])

print("\nForward Probability Table:")
print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

print(f"\nFinal Probability of sequence '{sequence}': {final_prob:.6f}")
