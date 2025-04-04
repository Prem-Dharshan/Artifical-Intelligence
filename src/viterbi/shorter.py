import numpy as np
from tabulate import tabulate

# Define HMM parameters
states = ["H", "L"]
sequence = "GGCACTGAA"
T, N = len(sequence), len(states)

# Log probabilities
start_probs = {"H": -1, "L": -1}
transition_probs = {"H": {"H": -1, "L": -1}, "L": {"H": -1.322, "L": -0.737}}
emission_probs = {
    "H": {"A": -2.322, "C": -1.737, "G": -1.737, "T": -2.322},
    "L": {"A": -1.737, "C": -2.322, "G": -2.322, "T": -1.737}
}

# Convert dicts to NumPy arrays for fast computation
start_vec = np.array([start_probs[s] for s in states])
trans_mat = np.array([[transition_probs[s1][s2] for s2 in states] for s1 in states])
emit_mat = np.array([[emission_probs[s][c] for c in sequence] for s in states])

# Step 1: Initialization
delta = np.full((N, T), -np.inf)
delta[:, 0] = start_vec + emit_mat[:, 0]

# Step 2: Recursion (vectorized max operation)
for t in range(1, T):
    delta[:, t] = emit_mat[:, t] + np.max(delta[:, t - 1][:, None] + trans_mat, axis=0)

# Step 3: Extract the most likely states
best_path_states = [states[np.argmax(delta[:, t])] for t in range(T)]

# Convert to table format
table_data = [["State"] + list(sequence)] + [[s] + [f"{delta[i, t]:.3f}" for t in range(T)] for i, s in enumerate(states)]

print("\nViterbi Algorithm Probability Table:")
print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
print(f"\nFinal Probability of Sequence: {np.max(delta[:, -1]):.3f}")
print("\nMost Likely Hidden State Sequence:")
print(" → ".join(best_path_states))
