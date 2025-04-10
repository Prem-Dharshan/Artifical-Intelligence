import numpy as np
from tabulate import tabulate

# Define states and sequence

S1 = "S1"
S2 = "S2"

states = [S1, S2]
sequence =  "CGTCAG"

# Probability definitions (log probabilities)
start_probs = {
    S1: 0.5,
    S2: 0.5
}
transition_probs = {
    S1: {
        S1: 0.8,
        S2: 0.2
    },
    S2: {
        S1: 0.2,
        S2: 0.8
    }
}
emission_probs = {
    S1: {
        "A": 0.4,
        "C": 0.1,
        "G": 0.4,
        "T": 0.1
    },
    S2: {
        "A": 0.1,
        "C": 0.4,
        "G": 0.1,
        "T": 0.4
    }
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

#  Normal prob
#  2 ** final_prob
print(f"\nFinal Probability of Sequence: {2 ** final_prob:.10f}")