import numpy as np
from tabulate import tabulate

# Define states and sequence
states = ["H", "L"]
sequence = "GGCACTGAA"

# Probability definitions (log probabilities)
start_probs = {"H": -1, "L": -1}
transition_probs = {"H": {"H": -1, "L": -1}, "L": {"H": -1.322, "L": -0.737}}
emission_probs = {
    "H": {"A": -2.322, "C": -1.737, "G": -1.737, "T": -2.322},
    "L": {"A": -1.737, "C": -2.322, "G": -2.322, "T": -1.737}
}

T = len(sequence)
N = len(states)

# Initialize Viterbi (delta) table
delta = np.full((N, T), -np.inf)  # Fill with negative infinity for log probs

# Step 1: Initialization
for i, state in enumerate(states):
    delta[i, 0] = start_probs[state] + emission_probs[state][sequence[0]]

# Step 2: Recursion using the given formula
for t in range(1, T):
    for i, curr_state in enumerate(states):
        delta[i, t] = max(
            delta[j, t - 1] + transition_probs[prev_state][curr_state]
            for j, prev_state in enumerate(states)
        ) + emission_probs[curr_state][sequence[t]]

best_path_states = [states[np.argmax(delta[:, t])] for t in range(T)]

table_data = [["State"] + list(sequence)]
for i, state in enumerate(states):
    table_data.append([state] + [f"{delta[i, t]:.3f}" for t in range(T)])

print("\nViterbi Algorithm Probability Table:")
print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

# Get final probability
final_prob = np.max(delta[:, -1])  # Final probability is max of last column

print(f"\nFinal Probability of Sequence: {final_prob:.3f}")

print("\nMost Likely Hidden State Sequence:")
print(" → ".join(best_path_states))
