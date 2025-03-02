from enum import Enum
from typing import Set, Optional
from collections import deque


class People(Enum):
    BLONDEMOM = '👱‍♀️'
    BRUNETTEMOM = '👱🏾‍♀️'
    BLONDEDAUGHTER = '👧🏻'
    BLONESON = '👦🏻'
    BRUNETTEDAUGHTER = '👧🏾'
    BRUNETTESON = '👦🏾'
    POLICEMAN = '👮🏼‍♂️'
    THIEF = '🏃🏼‍♂️'


class State:
    def __init__(self, left: Set[People], right: Set[People], boat_position: bool, parent: Optional["State"] = None):
        self.left = left
        self.right = right
        self.boat_position = boat_position  # True = Left, False = Right
        self.parent = parent  # Track the state we came from

    def __eq__(self, other):
        return isinstance(other, State) and self.left == other.left and self.right == other.right and self.boat_position == other.boat_position

    def __hash__(self):
        return hash((frozenset(self.left), frozenset(self.right), self.boat_position))

    def __str__(self):
        left_people = ", ".join([p.value for p in self.left])
        right_people = ", ".join([p.value for p in self.right])
        return f"Left: [{left_people}], Right: [{right_people}], Boat on {'Left' if self.boat_position else 'Right'}"

    def is_valid(self):
        """Checks if the current state is valid based on rules."""
        invalid_states = [
            {People.BLONDEMOM, People.BRUNETTEDAUGHTER, People.BRUNETTESON},
            {People.BRUNETTEMOM, People.BLONDEDAUGHTER, People.BLONESON},
            {People.BLONDEMOM, People.BRUNETTEDAUGHTER},
            {People.BLONDEMOM, People.BRUNETTESON},
            {People.BRUNETTEMOM, People.BLONDEDAUGHTER},
            {People.BRUNETTEMOM, People.BLONESON},
            {People.BLONDEMOM, People.BRUNETTEMOM, People.BLONDEDAUGHTER, People.BLONESON, People.BRUNETTEDAUGHTER,
             People.BRUNETTESON, People.POLICEMAN},
            {People.BLONDEMOM, People.BRUNETTEMOM, People.BLONDEDAUGHTER, People.BLONESON, People.BRUNETTEDAUGHTER,
             People.BRUNETTESON, People.THIEF}
        ]

        if self.left in invalid_states or self.right in invalid_states:
            print(f"🚫 Invalid state detected: {self}")
            return False

        return True

    def move_people(self, people_to_move: Set[People], from_left_to_right: bool):
        """Moves people and returns a new state."""
        new_left = self.left.copy()
        new_right = self.right.copy()

        if from_left_to_right:
            new_left.difference_update(people_to_move)
            new_right.update(people_to_move)
            new_boat_position = False
        else:
            new_right.difference_update(people_to_move)
            new_left.update(people_to_move)
            new_boat_position = True

        new_state = State(new_left, new_right, new_boat_position, parent=self)

        print(
            f"⛵ Moving {people_to_move} {'from Left to Right' if from_left_to_right else 'from Right to Left'} -> New State: {new_state}")

        return new_state

    def track_path(self):
        """Tracks the solution path and saves it to `path.txt`."""
        path = []
        state = self

        while state:
            path.append(state)
            state = state.parent  # Go back to previous state

        path.reverse()

        with open("path.txt", "w", encoding="utf-8") as f:
            f.write("\nSolution Path:\n")
            for step in path:
                f.write(str(step) + "\n")

        print("\nSolution found! Path written to path.txt")


def bfs_solve(start_state: State, goal_state: State):
    """Performs BFS to find the solution."""
    queue = deque([start_state])
    visited = set()

    while queue:
        curr = queue.popleft()

        print(f"\nProcessing State: {curr}")  # Debug print

        if curr == goal_state:
            print("🎉 Solution found!")
            curr.track_path()
            return

        if curr in visited:
            print("Already visited, skipping.")
            continue

        visited.add(curr)

        # Possible moves
        possible_moves = [
            {People.POLICEMAN, People.THIEF},
            {People.BLONDEMOM, People.BLONDEDAUGHTER},
            {People.BLONDEMOM, People.BLONESON},
            {People.BRUNETTEMOM, People.BRUNETTEDAUGHTER},
            {People.BRUNETTEMOM, People.BRUNETTESON},
            {People.BLONDEDAUGHTER, People.BLONESON},
            {People.BRUNETTEDAUGHTER, People.BRUNETTESON},
            {People.POLICEMAN},
            {People.THIEF}
        ]

        from_left_to_right = curr.boat_position

        for move in possible_moves:
            if (from_left_to_right and move.issubset(curr.left)) or (not from_left_to_right and move.issubset(curr.right)):
                new_state = curr.move_people(move, from_left_to_right)

                if not new_state.is_valid():
                    print(f"🚨 Invalid state generated: {new_state}")
                    continue

                if new_state in visited:
                    print(f"🔄 Already visited: {new_state}")
                    continue

                print(f"✅ New state added to queue: {new_state}")
                queue.append(new_state)

    print("❌ No solution found.")


def main():
    start_state = State(
        left={People.BLONDEMOM, People.BRUNETTEMOM, People.BLONDEDAUGHTER, People.BLONESON,
              People.BRUNETTEDAUGHTER, People.BRUNETTESON, People.POLICEMAN, People.THIEF},
        right=set(),
        boat_position=True
    )

    goal_state = State(
        left=set(),
        right={People.BLONDEMOM, People.BRUNETTEMOM, People.BLONDEDAUGHTER, People.BLONESON,
               People.BRUNETTEDAUGHTER, People.BRUNETTESON, People.POLICEMAN, People.THIEF},
        boat_position=False
    )

    bfs_solve(start_state, goal_state)


if __name__ == "__main__":
    main()
