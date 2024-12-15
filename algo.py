import numpy as np
import heapq
import random
import math

def heuristic(node, goal):
    """Manhattan distance heuristic."""
    return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
def A_star(env, start, goal):
    open_list = [(0, start, [])] 
    closed_list = set()
    explored = []

    while open_list:
        _, current, path = heapq.heappop(open_list)
        if current == goal:
            return path + [current], explored
        if current in closed_list:
            # Record the explored nodes at this state
            explored.append(list(closed_list))
            continue
        closed_list.add(current)
        explored.append(list(closed_list))

        row, col = current
        for dr, dc in [(0,1),(0,-1),(1,0),(-1,0)]:
            r, c = row+dr, col+dc
            if 0 <= r < env.shape[0] and 0 <= c < env.shape[1] and env[r,c] != 1:
                if (r,c) not in closed_list:
                    g_cost = len(path)+1
                    h_cost = heuristic((r,c), goal)
                    f_cost = g_cost+ 2* h_cost
                    heapq.heappush(open_list, (f_cost, (r,c), path+[current]))

    return None, explored




import numpy as np
import math
import random

def is_free(env, point):
    r, c = point
    if 0 <= r < env.shape[0] and 0 <= c < env.shape[1]:
        return env[r, c] != 1
    return False

def line_collision(env, p1, p2):
    """
    For one-step moves, line_collision is trivial: just ensure both p1 and p2 are free.
    If you had larger steps, you'd need to check all cells along the path.
    """
    if not is_free(env, p1):
        return False
    if not is_free(env, p2):
        return False
    return True

def distance(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])  

def nearest(nodes, q_rand):
    """Return the nearest node in nodes to q_rand by Manhattan distance."""
    return min(nodes, key=lambda x: distance(x, q_rand))

def steer(q_nearest, q_rand):
    """
    Move from q_nearest towards q_rand by 1 step either up, down, left, or right.
    We choose the direction that decreases Manhattan distance without diagonals.
    """
    r_near, c_near = q_nearest
    r_rand, c_rand = q_rand
    dr = r_rand - r_near
    dc = c_rand - c_near

    # Decide which direction to move
    # Move in the dimension with the greatest absolute difference first
    if abs(dr) > abs(dc):
        # Move vertically
        if dr > 0:
            # move down
            q_new = (r_near + 1, c_near)
        else:
            # move up
            q_new = (r_near - 1, c_near)
    else:
        # Move horizontally
        if dc > 0:
            # move right
            q_new = (r_near, c_near + 1)
        else:
            # move left
            q_new = (r_near, c_near - 1)
    return q_new

def RRT(env, start, goal, max_iterations=2000, goal_threshold=1):
    """
    RRT algorithm that does not move diagonally. It expands in four directions only.
    Returns path and explored states.
    """
    if not is_free(env, start) or not is_free(env, goal):
        return None, []

    tree = [start]
    parents = {start: None}
    explored = []

    for i in range(max_iterations):
        # Bias towards goal 10% of the time
        if random.random() < 0.2:
            q_rand = goal
        else:
            q_rand = (random.randint(0, env.shape[0]-1),
                      random.randint(0, env.shape[1]-1))

        if not is_free(env, q_rand):
            continue

        q_nearest = nearest(tree, q_rand)
        q_new = steer(q_nearest, q_rand)

        # Check if we moved to a new node
        if q_new == q_nearest:
            continue

        if is_free(env, q_new) and line_collision(env, q_nearest, q_new):
            # Add q_new to the tree
            if q_new not in tree:
                tree.append(q_new)
                parents[q_new] = q_nearest
                explored.append(list(tree))  # record explored state

                # Check if we are close enough to goal
                if distance(q_new, goal) < goal_threshold:
                    if is_free(env, goal) and line_collision(env, q_new, goal):
                        # If we can step into the goal directly:
                        q_new = goal
                        tree.append(q_new)
                        parents[q_new] = parents[q_new] if q_new in parents else q_new
                    # Reconstruct path including goal
                    path = []
                    current = q_new
                    while current is not None:
                        path.append(current)
                        current = parents[current]
                    path.reverse()
                    # Ensure goal is at the end if not already
                    if path[-1] != goal and line_collision(env, path[-1], goal) and is_free(env, goal):
                        path.append(goal)
                    return path, explored

    # If we reach here, no path found
    return None, explored
