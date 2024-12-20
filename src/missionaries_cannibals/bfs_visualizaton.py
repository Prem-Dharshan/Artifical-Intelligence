import streamlit as st
import networkx as nx
import plotly.graph_objects as go
from queue import PriorityQueue


class State:
    def __init__(self, left, right, boat_position):
        self.left = left  # (M, C)
        self.right = right  # (M, C)
        self.boat_position = boat_position  # True if boat is on the left, False if on the right

    def is_valid(self):
        # Ensure missionaries are not outnumbered on either side
        return (self.left[0] == 0 or self.left[0] >= self.left[1]) and (
                self.right[0] == 0 or self.right[0] >= self.right[1]
        )

    def is_goal(self):
        # Goal state: all missionaries and cannibals on the right
        return self.right == (3, 3)

    def get_successors(self):
        l_m, l_c = self.left
        r_m, r_c = self.right
        successors = []
        moves = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

        if self.boat_position:  # Boat on the left
            for m in moves:
                new_left = (l_m - m[0], l_c - m[1])
                new_right = (r_m + m[0], r_c + m[1])
                new_state = State(new_left, new_right, False)
                if new_state.is_valid():
                    successors.append(new_state)
        else:  # Boat on the right
            for m in moves:
                new_left = (l_m + m[0], l_c + m[1])
                new_right = (r_m - m[0], r_c - m[1])
                new_state = State(new_left, new_right, True)
                if new_state.is_valid():
                    successors.append(new_state)

        return successors

    def __str__(self):
        return f"L: {self.left}, R: {self.right}, Boat: {'Left' if self.boat_position else 'Right'}"

    def __lt__(self, other):
        # Comparison for priority queue
        return (self.right[0] + self.right[1]) > (other.right[0] + other.right[1])


def visualize_graph(graph, path):
    fig = go.Figure()

    pos = nx.spring_layout(graph)  # Node positions
    edge_x = []
    edge_y = []
    for edge in graph.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    # Add edges to the plot
    fig.add_trace(go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=1, color='gray'),
        hoverinfo='none',
        mode='lines'))

    # Highlight the path in red
    path_edges = list(zip(path[:-1], path[1:]))
    for edge in path_edges:
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        fig.add_trace(go.Scatter(
            x=[x0, x1],
            y=[y0, y1],
            line=dict(width=2, color='red'),
            hoverinfo='none',
            mode='lines'))

    # Add nodes to the plot
    node_x = []
    node_y = []
    node_text = []
    for node in graph.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        node_text.append(node)

    fig.add_trace(go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers+text',
        marker=dict(size=10, color='lightblue', line=dict(width=1, color='black')),
        text=node_text,
        textposition="top center"))

    fig.update_layout(showlegend=False)
    fig.update_layout(title="Missionaries and Cannibals Problem State Graph",
                      title_font_size=20,
                      margin=dict(l=20, r=20, t=40, b=20),
                      xaxis=dict(showgrid=False, zeroline=False, visible=False),
                      yaxis=dict(showgrid=False, zeroline=False, visible=False))
    return fig


def solve_missionaries_cannibals():
    start_state = State((3, 3), (0, 0), True)

    queue = PriorityQueue()
    queue.put((0, start_state))

    visited = set()
    parent_map = {}

    G = nx.DiGraph()

    while not queue.empty():
        level, current_state = queue.get()

        # If goal state is reached
        if current_state.is_goal():
            path = []
            while current_state:
                path.append(str(current_state))
                current_state = parent_map.get(str(current_state))
            path.reverse()
            return G, path

        visited.add(str(current_state))

        for successor in current_state.get_successors():
            if str(successor) not in visited:
                queue.put((level + 1, successor))
                parent_map[str(successor)] = current_state
                G.add_edge(str(current_state), str(successor))

    return G, []


def main():
    st.title("Missionaries and Cannibals Problem Visualization")
    st.write("This app visualizes the Missionaries and Cannibals problem as a graph.")

    G, path = solve_missionaries_cannibals()

    if path:
        st.success(f"Solution found! The path to the goal is:")
        for state in path:
            st.write(state)
    else:
        st.error("No solution found!")

    # Visualize the graph with the path
    fig = visualize_graph(G, path)
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
