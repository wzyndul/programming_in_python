# To generate random numbers, use the random module from the standard library.
# If more advanced mathematical calculations are necessary, use the math module from the standard library.
from sheep import Sheep
from wolf import Wolf


class Simulation:
    def __init__(self, round_nr, sheep_nr, limit, sheep_move, wolf_move):
        self._round_nr = round_nr
        self._sheep_nr = sheep_nr
        self._limit = limit
        self._sheep_move = sheep_move
        self._wolf_move = wolf_move
        self._sheep_list = None
        self._wolf = None
        self._sheep_eaten = 0
        self._round = 0

    def __display_info(self):
        pass

    def __spawn_animals(self):
        self._sheep_list = [
            Sheep(limit=self._limit, movement=self._sheep_move) for _ in
            range(self._sheep_nr)]
        self._wolf = Wolf(sheep_list=self._sheep_list,
                          movement=self._wolf_move)

    def start(self):
        self.__spawn_animals()
        for _ in range(self._round_nr):
            for sheep in self._sheep_list:
                if not sheep.is_eaten():
                    sheep.move()
            self._wolf.move()
        for sheep in self._sheep_list:
            print(f"koordynaty: ({sheep.get_x()},{sheep.get_y()}),"
                  f" zyje?: {sheep.is_eaten()}")

        print(
            f"WOLF koordynaty: ({self._wolf.get_x()},{self._wolf.get_y()})")

