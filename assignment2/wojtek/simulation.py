import csv
import json

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

    def __display_info(self, sheep_alive, index_sheep):

        info = f"Round number: {self._round}\nWolf Position:" \
               f" ({round(self._wolf.get_x(), 3)}," \
               f"{round(self._wolf.get_y(), 3)})" \
               f"sheep_alive: {sheep_alive}\n"

        if self._sheep_list[index_sheep] is None:
            info += f"The sheep was eaten, sheep number:" \
                    f" {index_sheep}\n\n"
        else:
            info += f"The wolf is chasing, sheep number:" \
                    f" {index_sheep}\n\n"
        return info


    def __data_json(self):
        sheep_pos = [[sheep.get_x(), sheep.get_y()] if sheep is not None else None for sheep in self._sheep_list]
        new_data = {"round_no": self._round, "wolf_pos": [self._wolf.get_x(), self._wolf.get_y()], "sheep_pos": sheep_pos}

        try:
            with open("pos.json", "r") as json_file:
                try:
                    existing_data = json.load(json_file) # if json file exists but is empty
                except json.JSONDecodeError:
                    existing_data = []
        except FileNotFoundError:
            existing_data = []

        existing_data.append(new_data)
        with open("pos.json", "w") as json_file:
            json_file.write('\n')
            json.dump(existing_data, json_file, indent=4)

    def __data_csv(self, num_alive_sheep): #TODO czy czysicic plik json i csv na poczatku kazdego wywolania programu
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
                csvwriter.writerow(['Round Number', 'Number of Alive Sheep']) #TODO czy dopisać nazwy kolumn czy out?

            csvwriter.writerow([self._round, num_alive_sheep])


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
                if sheep is not None:
                    sheep_alive += 1
                    sheep.move()
            index_sheep = self._wolf.move()
            print(self.__display_info(sheep_alive, index_sheep))
            self.__data_csv(sheep_alive)
            self.__data_json()
            self._round += 1