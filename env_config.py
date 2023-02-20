################################################################
#   Environment of the assignment
################################################################

################################################################
#   Grid World
#   Feel free to modify the grid world in any way
################################################################

generate_random_environment = False
grid = [
    ['G','W','G','Wh','Wh', 'G'],
    ['Wh','R','Wh','G','W', 'R'],
    ['Wh','Wh','R','Wh','G', 'Wh'],
    ['Wh','Wh','Wh','R','Wh', 'G'],
    ['Wh','W','W','W','R', 'Wh'],
    ['Wh','Wh','Wh','Wh','Wh', 'Wh'],
]


################################################################
#   Rewards
#   Feel free to modify the rewards in any way
#   Make sure the reward array has the same shape
#   as the grid array
################################################################

reward_map = {'G': +1, 'R': -1, 'W': 0, 'Wh': -0.04}

rewards = [[reward_map[cell] for cell in row] for row in grid]

################################################################
#   Actions
#   The actions are NORTH, SOUTH, EAST and WEST
#   Each action is represented by a tuple
#   
#   NORTH: (-1, 0)
#   SOUTH: (1, 0)
#   EAST:  (0, 1)
#   WEST:  (0, -1)
################################################################

actions = {
    "UP": (-1, 0), 
    "DOWN": (1, 0), 
    "RIGHT": (0, 1), 
    "LEFT": (0, -1)
}

################################################################
#   Pygame Display Settings
#   Feel free to modify the rewards in any way
#   Make sure the reward array has the same shape
#   as the grid array
################################################################

RATIO = 1
UTILITY_FONT_SIZE = 15 * RATIO
UTILITY_OFFSET = (4, 14)
POLICY_FONT_SIZE = 30 * RATIO
POLICY_OFFSET = (17, 5)
POLICY_FONT = "assets/seguisym.ttf"
UTILITY_FONT = "assets/seguisym.ttf"

block_size=50
width=300
height=300