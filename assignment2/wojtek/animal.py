from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, movement, logger=None):
        self.x = 0
        self.y = 0
        self.movement = movement
        self.logger = logger

    @abstractmethod
    def move(self):
        pass
