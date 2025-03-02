from queue import PriorityQueue


class State:
    def __init__(self, left, right, boat_position):
        self.left = left  # (M, C)
        self.right = right  # (M, C)
        self.boat_position = (
            boat_position  # True if boat is on the left, False if on the right
        )

    def getLeftMissionaries(self):
        return self.left[0]

    def getLeftCannibals(self):
        return self.left[1]

    def getRightMissionaries(self):
        return self.right[0]

    def getRightCannibals(self):
        return self.right[1]

    def is_valid(self):
        return (self.left[0] == 0 or self.left[0] >= self.left[1]) and (
            self.right[0] == 0 or self.right[0] >= self.right[1]
        )

    def is_goal(self):
        return self.right == (3, 3)

    def get_successors(self):
        l_m = self.getLeftMissionaries()
        l_c = self.getLeftCannibals()
        r_m = self.getRightMissionaries()
        r_c = self.getRightCannibals()

        successors = []

        if self.boat_position:  # Boat on the left
            moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
            for m in moves:
                new_left = (l_m - m[0], l_c - m[1])
                new_right = (r_m + m[0], r_c + m[1])
                new_state = State(new_left, new_right, False)
                if new_state.is_valid():
                    successors.append(new_state)
        else:  # Boat on the right
            moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
            for m in moves:
                new_left = (l_m + m[0], l_c + m[1])
                new_right = (r_m - m[0], r_c - m[1])
                new_state = State(new_left, new_right, True)
                if new_state.is_valid():
                    successors.append(new_state)

        return successors

    def __lt__(self, other):
        return (self.getRightMissionaries() + self.getRightCannibals()) < (
            other.getRightMissionaries() + other.getRightCannibals()
        )

    def __str__(self):
        return f"Left: {self.left} & Right: {self.right}, Boat on {'Left' if self.boat_position else 'Right'}"


def main():
    start_state = State(left=(3, 3), right=(0, 0), boat_position=True)

    queue = PriorityQueue()
    queue.put((0, start_state))

    visited = set()
    states_generated = 0
    path_to_goal = []

    while not queue.empty():
        level, current_state = queue.get()

        # Check if we reached the goal state
        if current_state.is_goal():
            print("Goal reached!")
            print(current_state)
            path_to_goal.append(current_state)  # Add goal state to path
            break

        # Add current state to visited set with boat position included
        visited.add(
            (current_state.left, current_state.right, current_state.boat_position)
        )

        # Track the path taken to reach this state
        path_to_goal.append(current_state)

        # Generate successors and add them to the queue if not visited
        for successor in current_state.get_successors():
            states_generated += 1
            if (
                successor.left,
                successor.right,
                successor.boat_position,
            ) not in visited:
                queue.put((level + 1, successor))

    print(f"Total states generated: {states_generated}")

    # Print the path taken to reach the goal
    print("Path to goal:")
    for state in path_to_goal:
        print(state)


if __name__ == "__main__":
    main()
