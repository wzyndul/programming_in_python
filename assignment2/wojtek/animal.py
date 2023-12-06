from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, movement):
        self.x = 0
        self.y = 0
        self.movement = movement

    @abstractmethod
    def move(self):
        pass
