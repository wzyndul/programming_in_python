# To generate random numbers, use the random module from the standard library.
# If more advanced mathematical calculations are necessary, use the math module from the standard library.
class Simulation:
    def __init__(self, round_nr, sheep_nr, limit, sheep_move, wolf_move):
        self._round_nr = round_nr
        self._sheep_nr = sheep_nr
        self._limit = limit
        self._sheep_move = sheep_move
        self._wolf_move = wolf_move
        self._sheep_list = []
        self._wolf = None
        self._sheep_eaten = 0
        self._round = 0


