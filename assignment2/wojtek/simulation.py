# To generate random numbers, use the random module from the standard library.
# If more advanced mathematical calculations are necessary, use the math module from the standard library.
import csv

from sheep import Sheep
from wolf import Wolf


class Simulation:
    def __init__(self, max_round_nr, sheep_nr, limit, sheep_move, wolf_move):
        self._max_round_nr = max_round_nr
        self._sheep_nr = sheep_nr
        self._limit = limit
        self._sheep_move = sheep_move
        self._wolf_move = wolf_move
        self._sheep_list = []
        self._wolf = None
        self._sheep_eaten = 0
        self._round = 0

    def __display_info(self, sheep_alive, curr_sheep):

        info = f"Round number: {self._round}\nWolf Position:" \
               f" ({round(self._wolf.get_x(), 3)}," \
               f"{round(self._wolf.get_y(), 3)})" \
               f"sheep_alive: {sheep_alive}\n"

        if curr_sheep.is_eaten():
            info += f"The sheep was eaten, sheep number:" \
                    f" {curr_sheep.get_index()}\n\n"
        else:
            info += f"The wolf is chasing, sheep number:" \
                    f" {curr_sheep.get_index()}\n\n"
        return info


    def __data_json(self): # TODO rozkminic jak robic z tymi niezywymi owcami !!!
        pass               # TODO w jaki sposob je przechowywac i przy okazji informowac o tym indeksie
                            # TODO zawsze moge w sumei w olfie zwracac index i podmieniac w tabeli na None i wtedy znam i
                            # indeks i czy niezyje itd

    def __data_csv(self):
        # Dane do zapisania w pliku alive.csv
        round_number = self._round
        # num_alive_sheep = self._count_alive_sheep()

        # Sprawdź, czy plik alive.csv już istnieje
        file_exists = False
        try:
            with open('alive.csv', 'r'):
                file_exists = True
        except FileNotFoundError:
            file_exists = False

        with open('alive.csv', 'a' if file_exists else 'w',
                  newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if not file_exists:
                # Jeśli plik nie istnieje, zapisz nagłówki
                csvwriter.writerow(['Round Number', 'Number of Alive Sheep'])

            csvwriter.writerow([round_number, num_alive_sheep])


    def __spawn_animals(self):
        self._sheep_list = [
            Sheep(limit=self._limit, movement=self._sheep_move, index=x) for x
            in range(self._sheep_nr)]
        self._wolf = Wolf(sheep_list=self._sheep_list,
                          movement=self._wolf_move)

    def start(self):
        self.__spawn_animals()
        for _ in range(self._max_round_nr):
            sheep_alive = 0
            for sheep in self._sheep_list:
                if not sheep.is_eaten():
                    sheep_alive += 1
                    sheep.move()
            curr_sheep = self._wolf.move()
            print(self.__display_info(sheep_alive, curr_sheep))
            self._round += 1

        # for sheep in self._sheep_list:
        #     print(f"koordynaty: ({sheep.get_x()},{sheep.get_y()}),"
        #           f" zyje?: {sheep.is_eaten()}")
        #
        # print(
        #     f"WOLF koordynaty: ({self._wolf.get_x()},{self._wolf.get_y()})")
