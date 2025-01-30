from collections import deque


class State:
    def __init__(self, three=0, five=0):
        self.three = three
        self.five = five

    def __eq__(self, other):
        return isinstance(other, State) and self.three == other.three and self.five == other.five

    def __hash__(self):
        return hash((self.three, self.five))

    def __repr__(self):
        return f"State(three={self.three}, five={self.five})"


def main():
    start_state = State(0, 0)
    goal_state = State(0, 4)

    queue = deque([start_state])
    visited = {start_state}

    while queue:
        curr = queue.popleft()

        if curr == goal_state:
            print("Goal state reached!")
            return

        actions = [
            State(3, curr.five),  # Fill 3-liter jug
            State(curr.three, 5),  # Fill 5-liter jug
            State(0, curr.five),  # Empty 3-liter jug
            State(curr.three, 0),  # Empty 5-liter jug
            # Pour water from 3-liter to 5-liter
            State(curr.three - min(curr.three, 5 - curr.five), curr.five + min(curr.three, 5 - curr.five)),
            # Pour water from 5-liter to 3-liter
            State(curr.three + min(curr.five, 3 - curr.three), curr.five - min(curr.five, 3 - curr.three))
        ]

        for action in actions:
            if action not in visited:
                queue.append(action)
                visited.add(action)

    print("No solution found!")


if __name__ == "__main__":
    main()
