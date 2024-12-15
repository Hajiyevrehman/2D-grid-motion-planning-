import numpy as np

def generate_random_environment(Dimension=[10, 10], Number_of_obstancles=20):
    # 0 = empty space, 1 = static block
    env = np.zeros(Dimension)
    for i in range(Number_of_obstancles):
        # Randomly choose top-left corner of the obstacle
        x = np.random.randint(0, Dimension[0])
        y = np.random.randint(0, Dimension[1])

        # Randomly choose width and height of the obstacle (up to a max size)
        max_size = min(Dimension[0] // 3, Dimension[1] / 4, 4) # Limit size to avoid very large obstacles
        width = np.random.randint(1, max_size + 1)
        height = np.random.randint(1, max_size + 1)

        # Ensure obstacle stays within the environment bounds
        x_end = min(x + width, Dimension[0])
        y_end = min(y + height, Dimension[1])

        # Create the rectangular obstacle
        env[x:x_end, y:y_end] = 1

    return env
def place_agent_goal(env):
    Dimensions = env.shape
    d = True
    while d:
        x = np.random.randint(0, Dimensions[0])
        y = np.random.randint(0, Dimensions[1])
        if env[x, y] == 0:
            env[x, y] = 10
            d = False
    d = True
    while d:
        x = np.random.randint(0, Dimensions[0])
        y = np.random.randint(0, Dimensions[1])
        if env[x, y] == 0:
            env[x, y] = 100
            d = False
    return env
