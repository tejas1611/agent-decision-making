################################################################
#   Config Variables for the Environment of the assignment
################################################################

# Grid World
grid = [
    ['G','W','G','Wh','Wh', 'G'],
    ['Wh','R','Wh','G','W', 'R'],
    ['Wh','Wh','R','Wh','G', 'Wh'],
    ['Wh','Wh','Wh','R','Wh', 'G'],
    ['Wh','W','W','W','R', 'Wh'],
    ['Wh','Wh','Wh','Wh','Wh', 'Wh'],
]


# Rewards
reward_map = {'G': +1, 'R': -1, 'W': 0, 'Wh': -0.04}
rewards = [[reward_map[cell] for cell in row] for row in grid]


# Actions
'''
    UP: (-1, 0)
    DOWN: (1, 0)
    RIGHT:  (0, 1)
    LEFT:  (0, -1)
'''
actions = {
    "UP": (-1, 0), 
    "DOWN": (1, 0), 
    "RIGHT": (0, 1), 
    "LEFT": (0, -1)
}


# Pygame Display Settings
RATIO = 1
UTILITY_FONT_SIZE = 14 * RATIO
UTILITY_OFFSET = (4, 14)
POLICY_FONT_SIZE = 30 * RATIO
POLICY_OFFSET = (11, 5)
POLICY_FONT = "Calibri"
UTILITY_FONT = "Calibri"

block_size=50

# Random Grid Generator
SEED = 1