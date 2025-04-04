import math


def value_iteration(transition, rewards, discount_factor=0.9, iterations=5, threshold=0.5):

    new_rewards = {}

    print("Initial Rewards:", rewards)

    for _ in range(iterations):
        for state in transition.keys():
            max_value = -math.inf  # Initialize max value

            for action in transition[state].keys():
                expected_value = sum(
                    rewards[next_state] * transition[state][action][next_state]
                    for next_state in transition[state][action]
                )
                max_value = max(max_value, expected_value)

            new_rewards[state] = rewards[state] + discount_factor * max_value

        # Convergence check
        if all(abs(rewards[s] - new_rewards[s]) < threshold for s in rewards):
            break

        rewards = new_rewards.copy()
        new_rewards = {}

        print("Updated Rewards:", rewards)

    return rewards


# Example MDP (same as your original)
transition_example = {
    'pu': {'s': {'pu': 1}, 'a': {'pu': 0.5, 'pf': 0.5}},
    'pf': {'s': {'rf': 0.5, 'pu': 0.5}, 'a': {'pf': 1}},
    'rf': {'s': {'rf': 0.5, 'ru': 0.5}, 'a': {'pf': 1}},
    'ru': {'s': {'ru': 0.5, 'pu': 0.5}, 'a': {'pu': 0.5, 'pf': 0.5}}
}

rewards_example = {'pu': 0, 'pf': 0, 'ru': 10, 'rf': 10}

# Run the value iteration
optimal_values = value_iteration(transition_example, rewards_example)

# Print final results
print("\nFinal Optimal Values:", optimal_values)
