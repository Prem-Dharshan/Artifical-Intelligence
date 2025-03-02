from queue import PriorityQueue
import numpy as np
import copy


def expand(state):
    i, j = np.where(state == 0)
    i, j = int(i[0]), int(j[0])
    res = []

    directions = [(i, j - 1), (i - 1, j), (i + 1, j), (i, j + 1)]

    for row, col in directions:
        if 0 <= row < 3 and 0 <= col < 3:
            dummy = copy.deepcopy(state)
            dummy[i][j], dummy[row][col] = dummy[row][col], dummy[i][j]
            res.append(dummy)

    return res


def state_to_tuple(state):
    return tuple(map(tuple, state))


def tuple_to_state(tpl):
    return np.array(tpl)


def search(pq, goal_state):
    visited = set()
    parent_map = {}
    depth_map = {state_to_tuple(tuple_to_state(pq.queue[0][1])): 0}

    while not pq.empty():
        puz_tuple = pq.get()[1]
        puz = tuple_to_state(puz_tuple)
        current_depth = depth_map[puz_tuple]

        if np.array_equal(puz, goal_state):
            return reconstruct_path(parent_map, puz_tuple), current_depth

        if puz_tuple in visited:
            continue

        visited.add(puz_tuple)

        successors = expand(puz)

        for successor in successors:
            successor_tuple = state_to_tuple(successor)
            if successor_tuple not in visited:
                pq.put((current_depth + 1, successor_tuple))
                parent_map[successor_tuple] = puz_tuple
                depth_map[successor_tuple] = current_depth + 1

    return False, None


def reconstruct_path(parent_map, end_state):
    path = [end_state]
    while end_state in parent_map:
        end_state = parent_map[end_state]
        path.append(end_state)
    path.reverse()
    return [tuple_to_state(state) for state in path]


def main():
    pq = PriorityQueue()

    start_state = np.array([[8, 1, 2], [0, 4, 3], [7, 6, 5]])

    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    pq.put((0, state_to_tuple(start_state)))
    path, depth = search(pq, state_to_tuple(goal_state))

    if path:
        for state in path:
            print(state)
        print(f"Number of levels to reach the solution: {depth}")
    else:
        print("No solution found")


if __name__ == "__main__":
    main()
