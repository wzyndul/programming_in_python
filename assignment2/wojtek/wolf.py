import math
from typing import List

from animal import Animal
from sheep import Sheep


class Wolf(Animal):

    def __init__(self, sheep_list: List[Sheep], movement, logger=None):
        super().__init__(movement, logger)
        self.sheep_list = sheep_list

    def move(self):  # TODO to obczaić jeszcze
        closest_sheep = None
        closest_dist = math.inf
        for i in range(len(self.sheep_list)):
            if self.sheep_list[i] is None:
                continue
            distance = self.calculate_dist(self.sheep_list[i].x,
                                             self.sheep_list[i].y)
            if closest_sheep is None or distance < closest_dist:
                closest_dist = distance
                closest_sheep = self.sheep_list[i]
        if self.logger:
            self.logger.debug(f"Closest sheep is {closest_sheep.index} the distance to closest sheep is {closest_dist}")
        if closest_dist <= self.movement:
            closest_sheep.eaten()
            self.sheep_list[closest_sheep.index] = None
            self.x = closest_sheep.x
            self.y = closest_sheep.y
        else:
            normalized_direction = (
                (closest_sheep.x - self.x) / closest_dist,
                (closest_sheep.y - self.y) / closest_dist)
            self.x = self.x + normalized_direction[0] * self.movement
            self.y = self.y + normalized_direction[1] * self.movement

        if self.logger:
            self.logger.debug(f"Wolf moved to ({self.x}, {self.y})")
            self.logger.imfo(f"Wolf moved.")
        return closest_sheep.index

    def calculate_dist(self, sheep_x, sheep_y):
        return math.sqrt(
            math.pow(self.x - sheep_x, 2) + math.pow(self.y - sheep_y, 2))
