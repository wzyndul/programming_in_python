import random

from animal import Animal


class Sheep(Animal):
    def __init__(self, limit, movement, index, logger=None):
        super().__init__(movement, logger)
        self.x = random.uniform(-limit, limit)
        self.y = random.uniform(-limit, limit)
        self.is_alive = True
        self.index = index
        self.direction = None
        if self.logger:
            self.logger.debug(
                f"Sheep {self.index} created at ({self.x}, {self.y})")

    def move(self):
        self.direction = random.choice(["left", "right", "up", "down"])
        if self.direction == "left":
            self.x -= self.movement
        elif self.direction == "right":
            self.x += self.movement
        elif self.direction == "up":
            self.y += self.movement
        else:
            self.y -= self.movement
        if self.logger:
            self.logger.debug(
                f"Sheep {self.index} chosen direction:  {self.direction}")
            self.logger.debug(
                f"Sheep {self.index} moved to ({self.x}, {self.y})")

    def eaten(self):
        self.is_alive = False
