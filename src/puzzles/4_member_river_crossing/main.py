from dataclasses import dataclass
from collections import deque
from typing import Optional


@dataclass
class State:
    father: bool
    mother: bool
    daughter: bool
    son: bool
    boat: bool
    parent: Optional["State"] = None

    def __hash__(self):
        return hash((self.father, self.mother, self.daughter, self.son, self.boat))

    def __eq__(self, other):
        return (
            self.father == other.father and
            self.mother == other.mother and
            self.daughter == other.daughter and
            self.son == other.son and
            self.boat == other.boat
        )

    def __repr__(self):
        return (f"State(father={self.father}, mother={self.mother}, "
                f"daughter={self.daughter}, son={self.son}, boat={self.boat})")

    def backtrack(self):
        path = []
        current = self
        while current:
            path.append(current)
            current = current.parent
        return path[::-1]


def main():
    start = State(True, True, True, True, True, None)
    goal = State(False, False, False, False, False)

    queue = deque([start])
    visited = set()

    while queue:
        curr = queue.popleft()

        if curr == goal:
            print("Solution found!")
            for state in curr.backtrack():
                print(state)
            return

        if curr in visited:
            continue

        visited.add(curr)

        # Possible moves when the boat is on the left
        if curr.boat:
            if curr.father:
                new_state = State(False, curr.mother, curr.daughter, curr.son, False, curr)
                if new_state not in visited:
                    queue.append(new_state)

            if curr.mother:
                new_state = State(curr.father, False, curr.daughter, curr.son, False, curr)
                if new_state not in visited:
                    queue.append(new_state)

            if curr.daughter:
                new_state = State(curr.father, curr.mother, False, curr.son, False, curr)
                if new_state not in visited:
                    queue.append(new_state)

            if curr.son:
                new_state = State(curr.father, curr.mother, curr.daughter, False, False, curr)
                if new_state not in visited:
                    queue.append(new_state)

            if curr.daughter and curr.son:
                new_state = State(curr.father, curr.mother, False, False, False, curr)
                if new_state not in visited:
                    queue.append(new_state)

        # Possible moves when the boat is on the right
        else:
            if not curr.father:
                new_state = State(True, curr.mother, curr.daughter, curr.son, True, curr)
                if new_state not in visited:
                    queue.append(new_state)

            if not curr.mother:
                new_state = State(curr.father, True, curr.daughter, curr.son, True, curr)
                if new_state not in visited:
                    queue.append(new_state)

            if not curr.daughter:
                new_state = State(curr.father, curr.mother, True, curr.son, True, curr)
                if new_state not in visited:
                    queue.append(new_state)

            if not curr.son:
                new_state = State(curr.father, curr.mother, curr.daughter, True, True, curr)
                if new_state not in visited:
                    queue.append(new_state)

            if not curr.daughter and not curr.son:
                new_state = State(curr.father, curr.mother, True, True, True, curr)
                if new_state not in visited:
                    queue.append(new_state)

    print("No solution found.")
    return


if __name__ == "__main__":
    main()
