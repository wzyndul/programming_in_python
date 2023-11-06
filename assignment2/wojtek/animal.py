from abc import ABC, abstractmethod


class Animal(ABC):
    def __init__(self, movement):
        self._x = 0
        self._y = 0
        self._movement = movement

    @abstractmethod
    def move(self):
        pass
