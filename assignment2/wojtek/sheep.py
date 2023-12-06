import random

from animal import Animal


class Sheep(Animal):
    def __init__(self, limit, movement, index):
        super().__init__(movement)
        self.x = random.uniform(-limit, limit)
        self.y = random.uniform(-limit, limit)
        self.is_alive = True
        self.index = index

    def move(self):
        choice = random.choice(["left", "right", "up", "down"])
        if choice == "left":
            self.x -= self.movement
        elif choice == "right":
            self.x += self.movement
        elif choice == "up":
            self.y += self.movement
        else:
            self.y -= self.movement

    def eaten(self):
        self.is_alive = False

