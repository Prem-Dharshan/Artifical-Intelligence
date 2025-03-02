from collections import deque


class State:
    def __init__(self, first=0, second=0):
        self.first = first
        self.second = second

    def __eq__(self, other):
        return isinstance(other, State) and self.first == other.first and self.second == other.second

    def __hash__(self):
        return hash((self.first, self.second))

    def __repr__(self):
        return f"State(first={self.first}, second={self.second})"


def solve_water_jug_problem(capacity_first, capacity_second, goal_state):
    capacity = State(capacity_first, capacity_second)
    start_state = State(0, 0)

    queue = deque([start_state])
    visited = {start_state}

    # Perform BFS
    while queue:
        curr = queue.popleft()

        if curr == goal_state:
            print("Goal state reached:", curr)
            return

        actions = [
            State(capacity.first, curr.second),  # Fill first jug
            State(curr.first, capacity.second),  # Fill second jug
            State(0, curr.second),  # Empty first jug
            State(curr.first, 0),  # Empty second jug
            # Pour from first jug to second jug
            State(curr.first - min(curr.first, capacity.second - curr.second),
                  curr.second + min(curr.first, capacity.second - curr.second)),
            # Pour from second jug to first jug
            State(curr.first + min(curr.second, capacity.first - curr.first),
                  curr.second - min(curr.second, capacity.first - curr.first))
        ]

        for action in actions:
            if action not in visited:
                queue.append(action)
                visited.add(action)

    print("No solution found!")


if __name__ == "__main__":
    first_jug_capacity = 3
    second_jug_capacity = 5
    goal = State(0, 4)

    solve_water_jug_problem(first_jug_capacity, second_jug_capacity, goal)
