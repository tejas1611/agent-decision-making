from enum import Enum


class Agent:
    def __init__(self, actions: dict):
        self.ACTIONS = Enum('ACTIONS', actions)

    def solve(self):
        raise NotImplementedError
