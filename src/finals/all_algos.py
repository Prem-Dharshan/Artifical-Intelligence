import math
import numpy as np
from tabulate import tabulate


# Function for Value Iteration (MDP)
def value_iteration(transition, rewards, discount_factor=0.9, iterations=5, threshold=0.5):
    """Performs value iteration for the MDP"""
    new_rewards = {}
    print("\nInitial Rewards:", rewards)

    # Initialize table data for display
    table_data = [["Iteration"] + list(rewards.keys()), ["0"] + [rewards[state] for state in rewards]]

    for i in range(1, iterations + 1):
        for state in transition.keys():
            max_value = -math.inf

            for action in transition[state].keys():
                expected_value = sum(
                    rewards[next_state] * transition[state][action][next_state]
                    for next_state in transition[state][action]
                )
                max_value = max(max_value, expected_value)

            new_rewards[state] = rewards[state] + discount_factor * max_value

        # Save current iteration results
        table_data.append([str(i)] + [new_rewards[state] for state in rewards])

        # Convergence check
        if all(abs(rewards[s] - new_rewards[s]) < threshold for s in rewards):
            break

        rewards = new_rewards.copy()
        new_rewards = {}

    print("\nValue Iteration Results:")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

    return rewards


# Function for Forward Algorithm (HMM)
def forward_algorithm(states, sequence, start_prob, transition_prob, emission_prob):
    """Runs the Forward Algorithm for HMM"""
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

    # Final probability
    final_prob = np.sum(alpha[:, -1])

    # Display table
    table_data = [["State"] + list(sequence)]
    for i, state in enumerate(states):
        table_data.append([state] + [f"{alpha[i, t]:.6f}" for t in range(T)])

    print("\nForward Algorithm Probability Table:")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))
    print(f"\nFinal Probability of sequence '{sequence}': {final_prob:.6f}")

    return final_prob


# Function for Viterbi Algorithm (HMM)
def viterbi_algorithm(states, sequence, start_probs, transition_probs, emission_probs):
    """Runs the Viterbi Algorithm for HMM"""
    T = len(sequence)
    N = len(states)
    delta = np.full((N, T), -np.inf)  # Fill with negative infinity

    # Initialization
    for i, state in enumerate(states):
        delta[i, 0] = start_probs[state] + emission_probs[state][sequence[0]]

    # Recursion
    for t in range(1, T):
        for i, curr_state in enumerate(states):
            delta[i, t] = max(
                delta[j, t - 1] + transition_probs[prev_state][curr_state]
                for j, prev_state in enumerate(states)
            ) + emission_probs[curr_state][sequence[t]]

    # Best path
    best_path_states = [states[np.argmax(delta[:, t])] for t in range(T)]

    # Display table
    table_data = [["State"] + list(sequence)]
    for i, state in enumerate(states):
        table_data.append([state] + [f"{delta[i, t]:.3f}" for t in range(T)])

    print("\nViterbi Algorithm Probability Table:")
    print(tabulate(table_data, headers="firstrow", tablefmt="grid"))

    # Final probability
    final_prob = np.max(delta[:, -1])

    print(f"\nFinal Probability of Sequence: {final_prob:.3f}")
    print("\nMost Likely Hidden State Sequence:")
    print(" → ".join(best_path_states))

    return final_prob, best_path_states


# MDP Inputs
transition_example = {
    'pu': {'s': {'pu': 1}, 'a': {'pu': 0.5, 'pf': 0.5}},
    'pf': {'s': {'rf': 0.5, 'pu': 0.5}, 'a': {'pf': 1}},
    'rf': {'s': {'rf': 0.5, 'ru': 0.5}, 'a': {'pf': 1}},
    'ru': {'s': {'ru': 0.5, 'pu': 0.5}, 'a': {'pu': 0.5, 'pf': 0.5}}
}
rewards_example = {'pu': 0, 'pf': 0, 'ru': 10, 'rf': 10}

# HMM Inputs for Forward Algorithm
states_forward = ["H", "L"]
sequence_forward = "GGCA"
start_prob_forward = {"H": 0.5, "L": 0.5}
transition_prob_forward = {"H": {"H": 0.5, "L": 0.5}, "L": {"H": 0.4, "L": 0.6}}
emission_prob_forward = {
    "H": {"A": 0.2, "C": 0.3, "G": 0.3, "T": 0.2},
    "L": {"A": 0.3, "C": 0.2, "G": 0.2, "T": 0.3}
}

# HMM Inputs for Viterbi Algorithm
sequence_viterbi = "GGCACTGAA"
start_probs_viterbi = {"H": -1, "L": -1}
transition_probs_viterbi = {"H": {"H": -1, "L": -1}, "L": {"H": -1.322, "L": -0.737}}
emission_probs_viterbi = {
    "H": {"A": -2.322, "C": -1.737, "G": -1.737, "T": -2.322},
    "L": {"A": -1.737, "C": -2.322, "G": -2.322, "T": -1.737}
}

# Run MDP Value Iteration
value_iteration(transition_example, rewards_example)

# Run Forward Algorithm for HMM
forward_algorithm(states_forward, sequence_forward, start_prob_forward, transition_prob_forward, emission_prob_forward)

# Run Viterbi Algorithm for HMM
viterbi_algorithm(states_forward, sequence_viterbi, start_probs_viterbi, transition_probs_viterbi, emission_probs_viterbi)
