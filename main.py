import argparse

from algos.policy_iteration import PolicyIteration
from algos.value_iteration import ValueIteration
from config import SEED, actions, grid, rewards
from manager.custom_grid import generate_grid
from manager.dataanalysis_manager import DataAnalysisManager
from manager.display_manager import DisplayManager
from models.environment import Environment


def parse_args():
    """
    Parse command line arguments.
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
    file_name = "assgn1"
    if args.random_grid == "True":
        grid, rewards = generate_grid(grid_height=20, grid_width=20,
                            prob_green=0.166, prob_red=0.166,
                            prob_wall=0.168, prob_white=0.5)
        file_name = "random" + str(SEED)
    
    algorithm = args.algorithm
    env = Environment(grid_world=grid, rewards=rewards, initial_state=(len(grid)-1, 0))

    if algorithm == "value_iteration":
        agent = ValueIteration(actions=actions, epsilon=0.1, gamma=0.99)
        result = agent.solve(env)
        result["grid"] = grid

        if args.debug:
            print(grid, result)

        DisplayManager(height=len(grid), width=len(grid[0]), output=file_name).display(result)
        DataAnalysisManager(algorithm=result['algorithm'], output=file_name).save(agent.get_data())

    elif algorithm == "policy_iteration":
        agent = PolicyIteration(actions=actions, k=300, gamma=0.99)
        result = agent.solve(env)
        result["grid"] = grid

        if args.debug:
            print(grid, result)

        DisplayManager(height=len(grid), width=len(grid[0]), output=file_name).display(result)
        DataAnalysisManager(algorithm=result['algorithm'], output=file_name).save(agent.get_data())

    else:
        print("INVALID ALGORITHM")
        print("Options: value_iteration | policy_iteration")