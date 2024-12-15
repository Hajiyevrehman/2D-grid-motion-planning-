import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib.animation as animation
from helper import find_start_goal


def visualize_environment(env, path=None, explored=None, start=None, goal=None):
    """Visualizes environment, showing explored states first, then the final path at the end."""
    if start is None or goal is None:
        # If not given, find start and goal
        s = np.argwhere(env == 10)
        g = np.argwhere(env == 100)
        start = tuple(s[0]) if len(s) > 0 else start
        goal = tuple(g[0]) if len(g) > 0 else goal

    env_vis = env.copy()

    # Set start and goal in the visualization array
    # 2 = green (Start), 3 = red (Goal)
    if start is not None:
        env_vis[start] = 2
    if goal is not None:
        env_vis[goal] = 3

    # Define colormap
    cmap = colors.ListedColormap(['white', 'black', 'green', 'red', 'blue', 'yellow'])
    # 0=Empty(white),1=Obstacle(black),2=Start(green),3=Goal(red),4=Path(blue),5=Explored(yellow)
    bounds = [0,1,2,3,4,5,6]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    img = ax.imshow(env_vis, cmap=cmap, norm=norm, origin='lower')

    ax.set_xticks(np.arange(-0.5, env.shape[1], 1), minor=True)
    ax.set_yticks(np.arange(-0.5, env.shape[0], 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=1)

    cbar = fig.colorbar(img, ax=ax, ticks=[0.5,1.5,2.5,3.5,4.5,5.5])
    cbar.ax.set_yticklabels(['Empty','Obstacle','Start','Goal','Path','Explored'])

    explored_data = explored if explored else []
    # One extra frame to show final path
    max_frames = len(explored_data) + (1 if path else 1)
    # If no path is found, last frame just shows full exploration.

    # Scatter for explored states
    explored_scatter = ax.scatter([], [], c='yellow', marker='o', s=60, zorder=3)
    # Line for path
    path_line, = ax.plot([], [], color='blue', linewidth=2, zorder=4)

    def animate(i):
        # Up to second-to-last frame, show explored nodes incrementally
        # On the last frame, show final path if available
        if i < len(explored_data):
            # Show explored nodes up to frame i
            exp_nodes = explored_data[i]
            if exp_nodes:
                ey, ex = zip(*exp_nodes)
            else:
                ex, ey = [], []
            explored_scatter.set_offsets(np.c_[ex, ey])
            # No path shown yet
            path_line.set_data([], [])
        else:
            # Last frame: show all explored nodes and the full path
            if explored_data:
                exp_nodes = explored_data[-1]
                if exp_nodes:
                    ey, ex = zip(*exp_nodes)
                else:
                    ex, ey = [], []
                explored_scatter.set_offsets(np.c_[ex, ey])
            else:
                # No explored nodes? Just empty
                explored_scatter.set_offsets([])

            # Now show full path if we have one
            if path:
                py, px = zip(*path)
                path_line.set_data(px, py)
            else:
                path_line.set_data([], [])
        return explored_scatter, path_line

    ani = animation.FuncAnimation(fig, animate, frames=max_frames, interval=300, blit=False, repeat=False)
    plt.title("A* Pathfinding Visualization")
    plt.show()
    return ani




def visualize_two_algorithms(env, start, goal, 
                             path_a=None, explored_a=None, 
                             path_r=None, explored_r=None):
    """
    Visualize A* (left) and RRT (right) side-by-side.
    path_a, explored_a: results from A*
    path_r, explored_r: results from RRT
    """

    # Copy env for stable background
    env_vis_a = env.copy()
    env_vis_r = env.copy()

    # Set start (2) and goal (3) cells
    if start is not None:
        env_vis_a[start] = 2
        env_vis_r[start] = 2
    if goal is not None:
        env_vis_a[goal] = 3
        env_vis_r[goal] = 3

    # Colormap: 0=Empty,1=Obstacle,2=Start,3=Goal,4=Path,5=Explored
    cmap = colors.ListedColormap(['white', 'black', 'green', 'red', 'blue', 'yellow'])
    bounds = [0,1,2,3,4,5,6]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, (ax_a, ax_r) = plt.subplots(1, 2, figsize=(10,5))

    # A* subplot
    img_a = ax_a.imshow(env_vis_a, cmap=cmap, norm=norm, origin='lower')
    ax_a.set_title("A*")
    ax_a.set_xticks(np.arange(-0.5, env.shape[1], 1), minor=True)
    ax_a.set_yticks(np.arange(-0.5, env.shape[0], 1), minor=True)
    ax_a.grid(which="minor", color="gray", linestyle='-', linewidth=1)

    # RRT subplot
    img_r = ax_r.imshow(env_vis_r, cmap=cmap, norm=norm, origin='lower')
    ax_r.set_title("RRT")
    ax_r.set_xticks(np.arange(-0.5, env.shape[1], 1), minor=True)
    ax_r.set_yticks(np.arange(-0.5, env.shape[0], 1), minor=True)
    ax_r.grid(which="minor", color="gray", linestyle='-', linewidth=1)

    # Colorbar (shared)
    cbar = fig.colorbar(img_a, ax=[ax_a, ax_r], ticks=[0.5,1.5,2.5,3.5,4.5,5.5])
    cbar.ax.set_yticklabels(['Empty','Obstacle','Start','Goal','Path','Explored'])

    explored_a_data = explored_a if explored_a else []
    explored_r_data = explored_r if explored_r else []

    # Determine number of frames
    max_frames = max(len(explored_a_data), len(explored_r_data)) + 1

    # Scatter and path lines for A*
    explored_scatter_a = ax_a.scatter([], [], c='yellow', marker='o', s=60, zorder=3)
    path_line_a, = ax_a.plot([], [], color='blue', linewidth=2, zorder=4)

    # Scatter and path lines for RRT
    explored_scatter_r = ax_r.scatter([], [], c='yellow', marker='o', s=60, zorder=3)
    path_line_r, = ax_r.plot([], [], color='blue', linewidth=2, zorder=4)

    def animate(i):
        # For A*
        if i < len(explored_a_data):
            exp_nodes_a = explored_a_data[i]
            if exp_nodes_a:
                ey_a, ex_a = zip(*exp_nodes_a)
            else:
                ex_a, ey_a = [], []
            explored_scatter_a.set_offsets(np.c_[ex_a, ey_a])
            path_line_a.set_data([], [])
        else:
            # final frame for A*
            if explored_a_data:
                exp_nodes_a = explored_a_data[-1]
                if exp_nodes_a:
                    ey_a, ex_a = zip(*exp_nodes_a)
                else:
                    ex_a, ey_a = [], []
                explored_scatter_a.set_offsets(np.c_[ex_a, ey_a])
            else:
                explored_scatter_a.set_offsets([])
            # Show final path if available
            if path_a:
                py_a, px_a = zip(*path_a)
                path_line_a.set_data(px_a, py_a)
            else:
                path_line_a.set_data([], [])

        # For RRT
        if i < len(explored_r_data):
            exp_nodes_r = explored_r_data[i]
            if exp_nodes_r:
                ey_r, ex_r = zip(*exp_nodes_r)
            else:
                ex_r, ey_r = [], []
            explored_scatter_r.set_offsets(np.c_[ex_r, ey_r])
            path_line_r.set_data([], [])
        else:
            # final frame for RRT
            if explored_r_data:
                exp_nodes_r = explored_r_data[-1]
                if exp_nodes_r:
                    ey_r, ex_r = zip(*exp_nodes_r)
                else:
                    ex_r, ey_r = [], []
                explored_scatter_r.set_offsets(np.c_[ex_r, ey_r])
            else:
                explored_scatter_r.set_offsets([])
            # Show final path if available
            if path_r:
                py_r, px_r = zip(*path_r)
                path_line_r.set_data(px_r, py_r)
            else:
                path_line_r.set_data([], [])

        return explored_scatter_a, path_line_a, explored_scatter_r, path_line_r

    ani = animation.FuncAnimation(fig, animate, frames=max_frames, interval=100, blit=False, repeat=False)
    plt.suptitle("A* vs RRT Visualization")
    plt.show()
    return ani
