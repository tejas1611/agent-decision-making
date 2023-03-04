from enum import Enum


class Agent:
    """
    Abstract class representing Agent object.
    """
    def __init__(self, actions: dict):
        self.ACTIONS = Enum('ACTIONS', actions)

    def solve(self):
        raise NotImplementedError

    def get_data(self):
        raise NotImplementedError
