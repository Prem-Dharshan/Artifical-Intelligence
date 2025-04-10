import numpy as np
from tabulate import tabulate
import math

def viterbi_log(sequence, states, start_prob, trans_prob, emission_prob, use_log=False):
    T = len(sequence)
    N = len(states)
    
    # Convert to log2 if not already log-probs
    if not use_log:
        start_prob = {k: math.log2(v) for k, v in start_prob.items()}
        trans_prob = {k: {j: math.log2(p) for j, p in trans_prob[k].items()} for k in trans_prob}
        emission_prob = {k: {s: math.log2(p) for s, p in emission_prob[k].items()} for k in emission_prob}

    # Initialize Viterbi table
    delta = np.full((N, T), -np.inf)

    # Step 1: Initialization
    for i, state in enumerate(states):
        delta[i, 0] = start_prob[state] + emission_prob[state][sequence[0]]

    # Step 2: Recursion
    for t in range(1, T):
        for i, curr_state in enumerate(states):
            delta[i, t] = max(
                delta[j, t - 1] + trans_prob[prev_state][curr_state]
                for j, prev_state in enumerate(states)
            ) + emission_prob[curr_state][sequence[t]]

    # Step 3: Backtracking best path (optional)
    best_path_states = [states[np.argmax(delta[:, t])] for t in range(T)]

    # Tabulate
    table_data = [["State"] + list(sequence)]
    for i, state in enumerate(states):
        table_data.append([state] + [f"{delta[i, t]:.3f}" for t in range(T)])

    print("\nViterbi Algorithm Log-Probability Table:")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

    final_log_prob = np.max(delta[:, -1])
    print(f"\nFinal Log Probability of Sequence: {final_log_prob:.3f}")
    print(f"Final Normal Probability of Sequence: {2 ** final_log_prob:.10f}")
    print("\nMost Likely Hidden State Sequence:")
    print(" → ".join(best_path_states))
    print("\n" + "-" * 60)

# --- Test Case 1: Log-space HMM (original question) ---
print("TEST CASE 1: [Log Space HMM]")
states1 = ["H", "L"]
seq1 = "GGCACTGAA"
start_probs1 = {"H": -1, "L": -1}
transition_probs1 = {"H": {"H": -1, "L": -1}, "L": {"H": -1.322, "L": -0.737}}
emission_probs1 = {
    "H": {"A": -2.322, "C": -1.737, "G": -1.737, "T": -2.322},
    "L": {"A": -1.737, "C": -2.322, "G": -2.322, "T": -1.737}
}

viterbi_log(seq1, states1, start_probs1, transition_probs1, emission_probs1, use_log=True)

# --- Test Case 2: Normal-prob HMM with S1/S2 ---
print("TEST CASE 2: [Normal Probabilities HMM]")
S1, S2 = "S1", "S2"
states2 = [S1, S2]
seq2 = "CGTCAG"

start_prob2 = {S1: 0.5, S2: 0.5}
trans_prob2 = {
    S1: {S1: 0.8, S2: 0.2},
    S2: {S1: 0.2, S2: 0.8}
}
emission_prob2 = {
    S1: {"A": 0.4, "C": 0.1, "G": 0.4, "T": 0.1},
    S2: {"A": 0.1, "C": 0.4, "G": 0.1, "T": 0.4}
}

viterbi_log(seq2, states2, start_prob2, trans_prob2, emission_prob2, use_log=False)
