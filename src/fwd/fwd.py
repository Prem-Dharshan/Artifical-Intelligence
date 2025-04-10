import numpy as np
from tabulate import tabulate

def forward_algorithm(states, sequence, start_prob, transition_prob, emission_prob):
    T = len(sequence)
    alpha = np.zeros((len(states), T))

    # Initialization
    for i, state in enumerate(states):
        alpha[i, 0] = start_prob[state] * emission_prob[state][sequence[0]]

    # Recursion
    for t in range(1, T):
        for i, state in enumerate(states):
            alpha[i, t] = sum(
                alpha[j, t - 1] * transition_prob[prev_state][state]
                for j, prev_state in enumerate(states)
            ) * emission_prob[state][sequence[t]]

    # Termination
    final_prob = np.sum(alpha[:, -1])

    # Display Table
    table_data = [["State"] + list(sequence)]
    for i, state in enumerate(states):
        table_data.append([state] + [f"{alpha[i, t]:.8f}" for t in range(T)])

    print("\nForward Probability Table:")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    print(f"\nFinal Probability of sequence '{sequence}': {final_prob:.8f}")
    print("-" * 60)


states = ["H", "L"]
sequence = "GGCA"
start_prob = {"H": 0.5, "L": 0.5}
transition_prob = {"H": {"H": 0.5, "L": 0.5}, "L": {"H": 0.4, "L": 0.6}}
emission_prob = {
    "H": {"A": 0.2, "C": 0.3, "G": 0.3, "T": 0.2},
    "L": {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3}
}

print("Test Case 1: H/L States")
forward_algorithm(states, sequence, start_prob, transition_prob, emission_prob)


S1, S2 = "S1", "S2"
states = [S1, S2]
start_prob = {S1: 0.5, S2: 0.5}
transition_prob = {
    S1: {S1: 0.8, S2: 0.2},
    S2: {S1: 0.2, S2: 0.8}
}
emission_prob = {
    S1: {"A": 0.4, "C": 0.1, "G": 0.4, "T": 0.1},
    S2: {"A": 0.1, "C": 0.4, "G": 0.1, "T": 0.4}
}
sequence = "CGTCAG"

print("\n\nTest Case 2: S1/S2 States")
forward_algorithm(states, sequence, start_prob, transition_prob, emission_prob)
