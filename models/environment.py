import random
from collections import defaultdict
from typing import *


class Environment:
    '''
    Contains: States, Transformer function, Step & Reward, Initial state
    '''

    def __init__(self, grid_world: List[List], rewards: List[List], initial_state: Tuple):
        self.generate_environment(grid_world, rewards, initial_state)

    def generate_environment(self, grid_world: List[List], rewards: List[List], initial_state: Tuple) -> Tuple[Tuple, float]:
        self.grid_world: List[List] = grid_world
        self.grid_width = len(grid_world[-1])
        self.grid_height = len(grid_world)
        self.rewards: List[List] = rewards
        self.agent_pos: Tuple = initial_state

        return (initial_state, rewards[initial_state[0]][initial_state[1]])

    def get_reward(self, state: Tuple) -> float:
        return self.rewards[state[0]][state[1]]

    def is_within_bounds(self, state: Tuple) -> bool:
        return (0 <= state[0] < self.grid_width and 0 <= state[1] < self.grid_height)

    def is_wall(self, state: Tuple) -> bool:
        return (self.grid_world[state[0]][state[1]] == 'W')

    def is_valid_state(self, state: Tuple) -> bool:
        """
        Check if state is within bounds and not a wall

        Args:
            state (Tuple): Current state

        Returns:
            bool: True if state is valid
        """
        return (self.is_within_bounds(state) and not self.is_wall(state))

    def state_transformer(self, state: Tuple, action: Tuple) -> dict:
        """
        Returns each potential next state with probabilities given the agent's current state and action

        Args:
            state (Tuple): Current state
            action (Tuple): Current action

        Returns:
            model (dict): Next states and probabilities 
        """
        model: DefaultDict = defaultdict(int)
        possible_actions: List[Tuple] = [action, (action[1], action[0]), (-action[1], -action[0])]
        probability_actions: Tuple = (0.8, 0.1, 0.1)

        for a, prob in zip(possible_actions, probability_actions):
            next_state: Tuple = (state[0]+a[0], state[1]+a[1])
            next_state = next_state if self.is_valid_state(next_state) else state

            model[next_state] += prob

        return dict(model)

    def step(self, state: Tuple, action: Tuple) -> Tuple[Tuple, float]:
        """
        Return next state and reward when agent takes an action in current state

        Args:
            state (Tuple): Current state
            action (Tuple): Current action

        Returns:
            Tuple: Contains the next state and reward
        """
        assert action is not None
        assert state is not None

        transformer_model: dict = self.state_transformer(state, action)
        next_state: Tuple = random.choices(list(transformer_model.keys()), weights=list(transformer_model.values()), k=1)[0]

        reward: float = self.get_reward(next_state)

        return (next_state, reward)
