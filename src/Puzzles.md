### **1. The Towers of Hanoi Problem**
- **Problem Statement**:  
  Move a stack of disks from one peg to another, following these rules:
  1. Only one disk can be moved at a time.
  2. A disk cannot be placed on a smaller disk.
  3. All disks must be moved from the source peg to the destination peg.
- **Informed Search Application**:  
  The **heuristic function** can be the number of disks remaining to be moved.

---

### **2. The Knight’s Tour Problem**
- **Problem Statement**:  
  A knight on a chessboard must visit each square exactly once using legal knight moves.
- **Informed Search Application**:  
  Use a heuristic based on the **Warnsdorff’s rule**, which prioritizes moves leading to the fewest onward moves.

---

### **3. The Traveling Salesman Problem (TSP)**
- **Problem Statement**:  
  Given a set of cities and distances between them, find the shortest route that visits each city exactly once and returns to the starting city.
- **Informed Search Application**:  
  The **A* heuristic** can be the sum of the current path cost and a minimum spanning tree (MST) estimate for unvisited cities.

---

### **4. The N-Queens Problem**
- **Problem Statement**:  
  Place N queens on an N×N chessboard such that no two queens attack each other.
- **Informed Search Application**:  
  The heuristic function can be **the number of conflicting queens** in a given state.

---

### **5. The Block World Problem**
- **Problem Statement**:  
  A robot must rearrange a set of blocks from an initial configuration to a goal configuration using a robotic arm.
- **Informed Search Application**:  
  The heuristic can be **the number of misplaced blocks**.

---

### **6. The Sliding Tile Puzzle (15-Puzzle, 8-Puzzle, etc.)**
- **Problem Statement**:  
  Arrange tiles in the correct order by sliding them into an empty space.
- **Informed Search Application**:  
  Use **Manhattan Distance** as a heuristic.

---

### **7. Rush Hour Puzzle**
- **Problem Statement**:  
  Move cars in a grid to free a blocked vehicle.
- **Informed Search Application**:  
  Use **blocking heuristics** (counting how many cars block the target vehicle).

---

### **8. The Pancake Sorting Problem**
- **Problem Statement**:  
  Given a stack of pancakes of different sizes, sort them using a spatula that can flip the top k pancakes at once.
- **Informed Search Application**:  
  The heuristic can be **the number of pancakes out of order**.

---

### **9. Sokoban (Warehouse Keeper)**
- **Problem Statement**:  
  A player must push boxes onto target locations in a grid-based warehouse.
- **Informed Search Application**:  
  Use heuristics like **Manhattan Distance from each box to its goal**.

---

### **10. The Cannibals and Missionaries with a Boat Capacity Constraint**
- **Problem Statement**:  
  A variation where the boat has a capacity of **three or more** instead of two.
- **Informed Search Application**:  
  Modify heuristics accordingly.

---

### **11. The Frog Puzzle (Leapfrog Puzzle)**
- **Problem Statement**:  
  Frogs of different colors must switch places using legal jumps.
- **Informed Search Application**:  
  A heuristic can be **the number of misplaced frogs**.

---
