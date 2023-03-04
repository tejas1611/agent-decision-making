from collections import defaultdict
from enum import Enum
from typing import *

import numpy as np

from models.agent import Agent
from models.environment import Environment


class ValueIteration(Agent):
    def __init__(self, actions: Enum, epsilon: float, gamma: Optional[float] = 0.99):
        """
        Initializes an agent that solves the MDP problem using Value Iteration 

        Args:
            epsilon (float): Maximum error allowed in the utility of any state
            gamma (float): Discount factor (optional, default = 0.99)
        """
        super().__init__(actions)
        self.gamma = gamma
        self.epsilon = epsilon

        self.data_analysis = defaultdict(list)

    def solve_utilities(self, env: Environment) -> Tuple[np.ndarray, int]:
        utilities: np.ndarray = np.zeros((env.grid_height, env.grid_width), dtype=np.float64)

        threshold: float = self.epsilon * (1 - self.gamma) / self.gamma
        iterations: int = 0
        delta: float = float('inf')

        while delta > threshold:
            new_utilities: np.ndarray = utilities.copy()
            delta = 0
            iterations += 1
            
            # Iterate through every state in environment
            for i in range(env.grid_height):
                for j in range(env.grid_width):
                    curr_state: Tuple = (i, j)

                    # If wall or invalid state, skip
                    if not env.is_valid_state(curr_state): continue

                    # Reward for current state
                    reward: float = env.get_reward(curr_state)

                    # Finding action that maximizes expected utility
                    action_expected_utility: List = []
                    for action in self.ACTIONS:
                        state_transformer: dict = env.state_transformer(curr_state, action=action.value)        # Get state transformer model for current state and action
                        expected_utility: float = sum([ utilities[next_state[0]][next_state[1]]*prob \
                            for next_state, prob in state_transformer.items() ])                                # Calculate expected utility over all possible next states
                        action_expected_utility.append(expected_utility)

                    # Bellman Update
                    new_utilities[i][j] = reward + self.gamma * max(action_expected_utility)

                    # Update delta
                    delta = max(delta, abs(new_utilities[i][j] - utilities[i][j]))

                    # Append state utility for analysis
                    self.data_analysis[str((j,i))].append(new_utilities[i][j])

            utilities = new_utilities.copy()

        return utilities, iterations

    def solve_optimal_policy(self, utilities: np.ndarray, env: Environment) -> np.ndarray:
        """
        Function that calculates best policy by maximizing expected utility
        based on the utilities provided

        Args:
            utilities (np.ndarray): Current utilities
            env (Environment): Environment object defining the states and transformer model

        Returns:
            Optimal policies of all states
        """
        policy = [[None for _ in range(env.grid_width)] for _ in range(env.grid_height)]

        # Iterate through every state in environment
        for i in range(env.grid_height):
            for j in range(env.grid_width):
                curr_state: Tuple = (i, j)

                # If wall or invalid state, skip
                if not env.is_valid_state(curr_state): continue

                # Finding action that maximizes expected utility
                action_expected_utility: dict = {}
                for action in self.ACTIONS:
                    state_transformer: dict = env.state_transformer(curr_state, action=action.value)        # Get state transformer model for current state and action
                    expected_utility: float = sum([ utilities[next_state[0]][next_state[1]]*prob \
                        for next_state, prob in state_transformer.items() ])                                # Calculate expected utility over all possible next states
                    action_expected_utility[action] = expected_utility

                # Update Policy
                policy[i][j] = max(action_expected_utility, key=action_expected_utility.get)

        return policy

    def solve(self, env: Environment) -> dict:
        """
        Main function that calculates final utilities and policies of all states

        Args:
            env (Environment): Environment object defining the states and transformer model

        Returns:
            Results including final utilities, optimal policies, no. of iterations
        """
        utilities, iterations = self.solve_utilities(env)
        policy = self.solve_optimal_policy(utilities, env)

        return {
            "utilities": utilities,
            "policy": policy,
            "iterations": iterations,
            "algorithm": "value_iteration"
        }

    def get_data(self) -> dict:
        return dict(self.data_analysis)
