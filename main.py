from display_manager import DisplayManager
from config import actions, generate_random_environment, grid, rewards
from environment import Environment
from policy_iteration import PolicyIteration
from value_iteration import ValueIteration

# algorithm = "value_iteration"
algorithm = "policy_iteration"


def generate_grid():
    pass

if __name__ == "__main__":
    if generate_random_environment:
        generate_grid()
    
    env = Environment(grid, rewards, (len(grid)-1, 0))

    if algorithm == "value_iteration":
        agent = ValueIteration(actions=actions, epsilon=0.1, gamma=0.99)
        result = agent.solve(env)

        DisplayManager().display(result)

    elif algorithm == "policy_iteration":
        agent = PolicyIteration(actions=actions, k=300, gamma=0.99)
        result = agent.solve(env)

        DisplayManager().display(result)