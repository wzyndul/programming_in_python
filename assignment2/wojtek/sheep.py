import random

from animal import Animal


class Sheep(Animal):
    def __init__(self, limit, movement, index):
        super().__init__(movement)
        self._x = random.uniform(-limit, limit)
        self._y = random.uniform(-limit, limit)
        self.__is_alive = True
        self._index = index

    def move(self):
        choice = random.choice(["left", "right", "up", "down"])
        if choice == "left":
            self._x -= self._movement
        elif choice == "right":
            self._x += self._movement
        elif choice == "up":
            self._y += self._movement
        else:
            self._y -= self._movement

    def eaten(self):
        self.__is_alive = False

    def is_eaten(self):
        return not self.__is_alive

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def get_index(self):
        return self._index