import numpy as np
from tabulate import tabulate

# Define HMM parameters
states = ["H", "L"]
sequence = "GGCA"
T, N = len(sequence), len(states)

# Start, Transition, and Emission probabilities
start_prob = {"H": 0.5, "L": 0.5}
transition_prob = {"H": {"H": 0.5, "L": 0.5}, "L": {"H": 0.4, "L": 0.6}}
emission_prob = {
    "H": {"A": 0.2, "C": 0.3, "G": 0.3, "T": 0.2},
    "L": {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3}
}

# Convert dictionaries to NumPy arrays for faster computation
start_vec = np.array([start_prob[s] for s in states])
trans_mat = np.array([[transition_prob[s1][s2] for s2 in states] for s1 in states])
emit_mat = np.array([[emission_prob[s][c] for c in sequence] for s in states])

# Step 1: Initialization
alpha = np.zeros((N, T))
alpha[:, 0] = start_vec * emit_mat[:, 0]

# Step 2: Recursion (using matrix-vector multiplication)
for t in range(1, T):
    alpha[:, t] = emit_mat[:, t] * (trans_mat.T @ alpha[:, t - 1])

# Step 3: Compute final probability
final_prob = np.sum(alpha[:, -1])

# Convert Forward Table to a readable format
table_data = [["State"] + list(sequence)] + [[s] + [f"{alpha[i, t]:.6f}" for t in range(T)] for i, s in enumerate(states)]

print("\nForward Probability Table:")
print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
print(f"\nFinal Probability of sequence '{sequence}': {final_prob:.6f}")
