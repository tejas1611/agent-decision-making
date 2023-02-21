import argparse

from config import actions, grid, rewards
from display_manager import DisplayManager
from environment import Environment
from policy_iteration import PolicyIteration
from value_iteration import ValueIteration
from custom_grid import generate_grid


def parse_args():
    """ Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Deep Colorizer")
    parser.add_argument(
        "--algorithm", help="Select Algorithm",
        default="value_iteration", required=True)
    parser.add_argument(
        "--random_grid", help="Use grid in Assignment 1 (False) OR generate random grid (True)",
        default="False", required=False)
    parser.add_argument(
        "--debug", help="Print grid and results in command line",
        default="False", required=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    if args.random_grid:
        grid, rewards = generate_grid(grid_height=20, grid_width=20,
                            prob_green=0.166, prob_red=0.166,
                            prob_wall=0.168, prob_white=0.5)
    
    algorithm = args.algorithm
    env = Environment(grid_world=grid, rewards=rewards, initial_state=(len(grid)-1, 0))

    if algorithm == "value_iteration":
        agent = ValueIteration(actions=actions, epsilon=0.1, gamma=0.99)
        result = agent.solve(env)
        result["grid"] = grid

        if args.debug:
            print(grid, result)

        DisplayManager(height=len(grid), width=len(grid[0])).display(result)

    elif algorithm == "policy_iteration":
        agent = PolicyIteration(actions=actions, k=300, gamma=0.99)
        result = agent.solve(env)
        result["grid"] = grid

        if args.debug:
            print(grid, result)

        DisplayManager(height=len(grid), width=len(grid[0])).display(result)