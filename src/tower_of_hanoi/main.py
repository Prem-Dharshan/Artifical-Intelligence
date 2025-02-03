from collections import deque
from typing import Tuple


class State:

    def __init__(self, rod_1: Tuple[int, ...], rod_2: Tuple[int, ...], rod_3: Tuple[int, ...]):
        self.rod_1 = rod_1
        self.rod_2 = rod_2
        self.rod_3 = rod_3

    def __eq__(self, other):
        return (self.rod_1, self.rod_2, self.rod_3) == (other.rod_1, other.rod_2, other.rod_3)

    def __hash__(self):
        return hash((self.rod_1, self.rod_2, self.rod_3))

    def __repr__(self):
        return f"State({self.rod_1}, {self.rod_2}, {self.rod_3})"


def main():
    start = State((3, 2, 1), (), ())
    goal = State((), (), (3, 2, 1))

    queue = deque([start])
    visited = set()

    while queue:
        curr = queue.popleft()
        visited.add(curr)

        if curr == goal:
            print('Goal state found:', curr)
            return

        # Move disk from rod 1 to rod 2 or rod 3 given that the move is valid
        if curr.rod_1:
            if not curr.rod_2 or curr.rod_1[-1] < curr.rod_2[-1]:
                new_state = State(curr.rod_1[:-1], curr.rod_2 + (curr.rod_1[-1],), curr.rod_3)
                if new_state not in visited:
                    queue.append(new_state)
                    visited.add(new_state)
            if not curr.rod_3 or curr.rod_1[-1] < curr.rod_3[-1]:
                new_state = State(curr.rod_1[:-1], curr.rod_2, curr.rod_3 + (curr.rod_1[-1],))
                if new_state not in visited:
                    queue.append(new_state)
                    visited.add(new_state)

        # Move disk from rod 2 to rod 1 or rod 3 given that the move is valid
        if curr.rod_2:
            if not curr.rod_1 or curr.rod_2[-1] < curr.rod_1[-1]:
                new_state = State(curr.rod_1 + (curr.rod_2[-1],), curr.rod_2[:-1], curr.rod_3)
                if new_state not in visited:
                    queue.append(new_state)
                    visited.add(new_state)
            if not curr.rod_3 or curr.rod_2[-1] < curr.rod_3[-1]:
                new_state = State(curr.rod_1, curr.rod_2[:-1], curr.rod_3 + (curr.rod_2[-1],))
                if new_state not in visited:
                    queue.append(new_state)
                    visited.add(new_state)

        # Move disk from rod 3 to rod 1 or rod 2 given that the move is valid
        if curr.rod_3:
            if not curr.rod_1 or curr.rod_3[-1] < curr.rod_1[-1]:
                new_state = State(curr.rod_1 + (curr.rod_3[-1],), curr.rod_2, curr.rod_3[:-1])
                if new_state not in visited:
                    queue.append(new_state)
                    visited.add(new_state)
            if not curr.rod_2 or curr.rod_3[-1] < curr.rod_2[-1]:
                new_state = State(curr.rod_1, curr.rod_2 + (curr.rod_3[-1],), curr.rod_3[:-1])
                if new_state not in visited:
                    queue.append(new_state)
                    visited.add(new_state)

    print('Goal not found')
    return


if __name__ == '__main__':
    main()
