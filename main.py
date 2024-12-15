from generation import generate_random_environment, place_agent_goal
from helper import find_start_goal
from algo import A_star, RRT
from visualization import visualize_environment, visualize_two_algorithms








def main(Dimension = [30, 30], Number_of_obstancles = 50 ):
    env = generate_random_environment(Dimension, Number_of_obstancles)
    env = place_agent_goal(env)
    start, goal = find_start_goal(env)
    print("Start:", start)
    print("Goal:", goal)


    path_a, explored_a = A_star(env, start, goal)
    path_r, explored_r = RRT(env, start, goal)

    visualize_two_algorithms(env, start, goal, path_a=path_a, explored_a=explored_a, path_r=path_r, explored_r=explored_r)



if __name__ == "__main__":
    main()
    