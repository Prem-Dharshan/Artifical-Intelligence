from queue import PriorityQueue
import numpy as np
import copy
import networkx as nx
import matplotlib.pyplot as plt
import streamlit as st


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


def search(pq, goal_state, graph):
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

                # Add the edge to the graph
                graph.add_edge(puz_tuple, successor_tuple)

    return False, None


def reconstruct_path(parent_map, end_state):
    path = [end_state]
    while end_state in parent_map:
        end_state = parent_map[end_state]
        path.append(end_state)
    path.reverse()
    return [tuple_to_state(state) for state in path]


def plot_graph(graph, path):
    fig, ax = plt.subplots(figsize=(12, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=False, node_size=50, node_color="skyblue", edge_color="gray")

    # Highlight the solution path
    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color="red", width=2)
    nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color="green", node_size=100)
    plt.title("State-Space Graph with Solution Path")
    st.pyplot(fig)


def main():
    st.title("8-Puzzle State-Space Graph Visualization")
    st.write("Visualizing the state space for an 8-puzzle using NetworkX.")

    start_state = np.array([[1, 2, 5], [0, 3, 4], [7, 8, 6]])
    goal_state = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])

    pq = PriorityQueue()
    pq.put((0, state_to_tuple(start_state)))

    graph = nx.DiGraph()

    st.write("### Initial State")
    st.write(start_state)
    st.write("### Goal State")
    st.write(goal_state)

    path, depth = search(pq, state_to_tuple(goal_state), graph)

    if path:
        st.write("### Solution Path")
        for state in path:
            st.write(state)

        st.write(f"Number of levels to reach the solution: {depth}")
        st.write("### State-Space Graph")
        fig, ax = plt.subplots(figsize=(12, 8))
        plot_graph(graph, [state_to_tuple(state) for state in path])
        st.pyplot(fig)
    else:
        st.write("No solution found.")


if __name__ == "__main__":
    main()
