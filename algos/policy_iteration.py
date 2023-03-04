import random
from collections import defaultdict
from enum import Enum
from typing import *

import numpy as np

from models.agent import Agent
from models.environment import Environment


class PolicyIteration(Agent):
    def __init__(self, actions: Enum,  k: Optional[int] = 100, gamma: Optional[float] = 0.99):
        """
        Initializes an agent that solves the MDP problem using Policy Iteration 

        Args:
            k (int): Maximum number of iterations (optional, default = 100)
            gamma (float): Discount factor (optional, default = 0.99)
        """
        super().__init__(actions)
        self.gamma = gamma
        self.k = k

        self.data_analysis = defaultdict(list)

    def policy_evaluation(self, policy: List[List], utilities: np.ndarray, env: Environment) -> Tuple[np.ndarray, int]:
        """
        Updates utilities using the current policy

        Args:
            policy (List[List]): Current policies
            utilities (np.ndarray): Current utilities
            env (Environment): Environment object defining the states and transformer model

        Returns:
            Updated utilities and number of iterations

        Note:
        For small state spaces, policy evaluation using exact solution methods is often the most efficient approach. 
        For large state spaces, O(n^3) time might be prohibitive. 
        Fortunately, it is not necessary to do exact policy evaluation. Instead, we can perform some number of
        simplified value iteration steps (simplified because the policy is fixed) to give a reasonably
        good approximation of the utilities.
        """
        iterations: int = 0
        
        while iterations < self.k:
            new_utilities: np.ndarray = utilities.copy()
            iterations += 1
            
            # Iterate through every state in environment
            for i in range(env.grid_height):
                for j in range(env.grid_width):
                    curr_state: Tuple = (i, j)

                    # If wall or invalid state, skip
                    if not env.is_valid_state(curr_state): continue

                    # Reward for current state
                    reward: float = env.get_reward(curr_state)

                    # Finding expected utility for the action given by current policy
                    action = policy[i][j]
                    state_transformer: dict = env.state_transformer(curr_state, action=action.value)            # Get state transformer model for current state and action
                    action_expected_utility: float = sum([ utilities[next_state[0]][next_state[1]]*prob \
                            for next_state, prob in state_transformer.items() ])                                # Calculate expected utility over all possible next states

                    # Bellman Update
                    new_utilities[i][j] = reward + self.gamma * action_expected_utility
                    
                    # Append state utility for analysis
                    self.data_analysis[str((j,i))].append(new_utilities[i][j])

            utilities = new_utilities.copy()

        return utilities, iterations

    def policy_improvement(self, policy: List[List], utilities: np.ndarray, env: Environment) -> Tuple[List[List], bool]:
        """
        Update policy for state by maximizing expected utility

        Args:
            policy (List[List]): Current policies
            utilities (np.ndarray): Current utilities
            env (Environment): Environment object defining the states and transformer model 

        Returns:
            Updated policies + boolean for whether policy has changed
        """
        is_policy_unchanged = True
        
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
                best_action = max(action_expected_utility, key=action_expected_utility.get)
                if policy[i][j] != best_action:
                    policy[i][j] = best_action
                    is_policy_unchanged = False

        return policy, is_policy_unchanged

    def solve(self, env: Environment) -> dict:
        """
        Initializes random policies and utilities and alternates between
        policy evaluation and imporvement steps until policy is unchanged

        Args:
            env (Environment): Environment object defining the states and transformer model

        Returns:
            Results including final utilities, optimal policies, no. of iterations
        """
        # Initialize random policy 
        policy: List[List] = [[random.choice(list(self.ACTIONS)) for _ in range(env.grid_width)] for _ in range(env.grid_height)]

        # Initialize utilities
        utilities: np.ndarray = np.zeros((env.grid_height, env.grid_width), dtype=np.float64)

        total_iterations: int = 0

        is_policy_unchanged = False
        while not is_policy_unchanged:
            utilities, iterations = self.policy_evaluation(policy, utilities, env)
            total_iterations += iterations

            policy, is_policy_unchanged = self.policy_improvement(policy, utilities, env)

        return {
            "utilities": utilities,
            "policy": policy,
            "iterations": iterations,
            "algorithm": "policy_iteration"
        }

    def get_data(self) -> dict:
        return dict(self.data_analysis)