import numpy as np

def find_start_goal(env):
    start = np.argwhere(env == 10)[0]
    goal = np.argwhere(env == 100)[0]
    return tuple(start), tuple(goal)
