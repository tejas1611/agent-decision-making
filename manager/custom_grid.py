from typing import *
import numpy as np
from config import SEED

# Set seed for reproducability
np.random.seed(SEED)

def generate_grid(grid_height: int, grid_width: int, prob_green: float = 0.166, prob_red: float = 0.166, 
                    prob_wall: float = 0.168, prob_white: float = 0.5) -> Tuple[List[List], List[List]]:
    """
    Generates a grid world environment of required dimensions based
    on probabilities of grid world objects.

    Args:
        grid_height (int): Number of rows in environment
        grid_width (int): Number of columns in environment
        prob_green (float): Probability that cell is green - +1 reward (optional, default = 0.166)
        prob_red (float): Probability that cell is red - -1 reward (optional, default = 0.166)
        prob_wall (float): Probability that cell is a wall - no reward (optional, default = 0.168)
        prob_white (float): Probability that cell is white - -0.04 reward (optional, default = 0.5)

    Returns:
        Grid world 2-D array
    """
    # Error checking in case sum of probabilities < 1
    assert (prob_green + prob_red + prob_wall + prob_white) == 1.0
    
    grid_things_arr = ['G', 'R', 'W', 'Wh']
    prob_arr        = [prob_green, prob_red, prob_wall, prob_white] 
    reward_map = {'G': +1, 'R': -1, 'W': 0, 'Wh': -0.04}

    grid = np.random.choice(grid_things_arr, (grid_height, grid_width), p=prob_arr)
    rewards = [[reward_map[cell] for cell in row] for row in grid]

    return grid, rewards