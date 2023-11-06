import math
from typing import List

from animal import Animal
from sheep import Sheep


class Wolf(Animal):

    def __init__(self, sheep_list: List[Sheep], movement):
        super().__init__(movement)
        self.__sheep_list = sheep_list

    def move(self): #TODO to obczaić jeszcze
        closest_sheep = self.__sheep_list[0]
        closest_dist = self.__calculate_dist(self.__sheep_list[0].get_x(),
                                             self.__sheep_list[0].get_y())
        for i in range(1, len(self.__sheep_list)):
            if self.__sheep_list[i].is_eaten():
                continue
            distance = self.__calculate_dist(self.__sheep_list[i].get_x(),
                                             self.__sheep_list[i].get_y())
            if distance < closest_dist:
                closest_dist = distance
                closest_sheep = self.__sheep_list[i]
        if closest_dist <= self._movement:
            closest_sheep.eaten()
            self._x = closest_sheep.get_x()
            self._y = closest_sheep.get_y()
        else:
            normalized_direction = (
                (closest_sheep.get_x() - self._x) / closest_dist,
                (closest_sheep.get_y() - self._y) / closest_dist)
            self._x = self._x + normalized_direction[0] * self._movement
            self._y = self._y + normalized_direction[1] * self._movement

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def __calculate_dist(self, sheep_x, sheep_y):
        return math.sqrt(
            math.pow(self._x - sheep_x, 2) + math.pow(self._y - sheep_y, 2))
