# Pathfinding Visualization: A* and RRT

This project demonstrates the behavior of two pathfinding algorithms, **A*** and **RRT (Rapidly-Exploring Random Tree)**, in a 2D grid environment. It includes a side-by-side animation of their exploration and pathfinding processes.

## Features

* **A***:
   * Finds the shortest path using a heuristic-based search.
   * Uses the **Manhattan distance** heuristic.
   * Guarantees an optimal path if one exists.

* **RRT**:
   * Randomly explores the grid until it reaches the goal.
   * Moves in **4 cardinal directions only** (no diagonals).
   * Ensures the exact goal is reached.

* **Visualization**:
   * Shows explored nodes (yellow), final paths (blue), start (green), and goal (red).
   * Displays obstacles (black) in the environment.

## Requirements

* Python 3.7+
* Libraries: `numpy`, `matplotlib`

Install dependencies using:

```bash
pip install requirements.txt
```

## How to Run

1. Define the grid environment:
   * `0`: Free space
   * `1`: Obstacle
   * `2`: Start (optional)
   * `3`: Goal (optional)

2. Run the script:

```bash
python main.py
```



## Functions

### A* Algorithm

```python
path, explored = A_star(env, start, goal)
```

* **Inputs**:
   * `env`: 2D grid (0 = free, 1 = obstacle)
   * `start`: Starting position (row, col)
   * `goal`: Goal position (row, col)

* **Outputs**:
   * `path`: List of grid cells representing the shortest path.
   * `explored`: List of explored nodes at each step.

### RRT Algorithm

```python
path, explored = RRT(env, start, goal)
```

* **Inputs**:
   * `env`: 2D grid (0 = free, 1 = obstacle)
   * `start`: Starting position (row, col)
   * `goal`: Goal position (row, col)

* **Outputs**:
   * `path`: List of grid cells representing the found path.
   * `explored`: List of explored nodes at each step.

### Visualization

```python
visualize_two_algorithms(env, start, goal, path_a, explored_a, path_r, explored_r)
```

* **Inputs**:
   * `env`: 2D grid environment.
   * `start`: Starting position.
   * `goal`: Goal position.
   * `path_a`: Path from A*.
   * `explored_a`: Explored nodes from A*.
   * `path_r`: Path from RRT.
   * `explored_r`: Explored nodes from RRT.

* **Output**: Animated side-by-side visualization.

## Notes

* **A*** guarantees the shortest path if one exists.
* **RRT** may not find the optimal path but will reach the goal if reachable within the iteration limit.
* Ensure obstacles don't completely block the goal for either algorithm to succeed.
* **A*** is more optimal for this task as the environment is not too complicated so there is not high complexity.

## License

This project is licensed under the MIT License.
