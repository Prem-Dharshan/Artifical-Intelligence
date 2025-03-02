### `a_star_with_visualization.py`

**Title**: State-Space Graph Visualization for 8-Puzzle

**Description**:  
This Python script implements the BFS search algorithm for solving an 8-puzzle and visualizes the state-space graph using NetworkX. The visualization is displayed using Streamlit.

#### Prerequisites
1. Python 3.8 or higher.
2. Install the required libraries:
   ```bash
   pip install numpy networkx matplotlib streamlit
   ```

#### How to Run
1. Save the script as `a_star_with_visualization.py`.
2. Run the Streamlit app:
   ```bash
   streamlit run a_star_with_visualization.py
   ```
3. Open the generated URL (e.g., `http://localhost:8501`) in your web browser to view the visualization.

#### Features
- Displays the initial and goal states.
- Solves the 8-puzzle problem using BFS and visualizes the solution path in the state-space graph.
- Highlights the shortest path from the initial state to the goal state in the graph.

#### Example Output
- **Solution Path**: Displays each state from the initial configuration to the goal.
- **State-Space Graph**: Shows all possible states and the connections between them, with the solution path highlighted.

---
