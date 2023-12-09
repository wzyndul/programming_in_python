import csv
import json
import logging
from sheep import Sheep
from wolf import Wolf


class Simulation:

    def __init__(self, max_round_nr, sheep_nr, limit, sheep_move, wolf_move, pause, log_level=None):
        self.max_round_nr = max_round_nr
        self.sheep_nr = sheep_nr
        self.limit = limit
        self.sheep_move = sheep_move
        self.wolf_move = wolf_move
        self.sheep_list = []
        self.wolf = None
        self.sheep_eaten = 0
        self.round = 0
        self.pause = pause
        self.log_level_mapping = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        self.log_level = self.log_level_mapping[log_level]



    def display_info(self, sheep_alive, index_sheep):

        info = f"Round number: {self.round}\nWolf Position:" \
               f" ({round(self.wolf.x, 3)}, " \
               f"{round(self.wolf.y, 3)}) " \
               f"sheep_alive: {sheep_alive}\n"

        if self.sheep_list[index_sheep] is None:
            info += f"The sheep number: {index_sheep} was eaten\n\n"
        else:
            info += f"The wolf is chasing sheep number:" \
                    f" {index_sheep}\n\n"
        return info

    def data_json(self):
        sheep_pos = [[sheep.x, sheep.y] if sheep is not None else None for sheep in self.sheep_list]
        new_data = {"round_no": self.round, "wolf_pos": [self.wolf.x, self.wolf.y], "sheep_pos": sheep_pos}

        try:
            with open("pos.json", "r") as json_file:
                try:
                    existing_data = json.load(json_file)  # if json file exists but is empty
                except json.JSONDecodeError:
                    existing_data = []
        except FileNotFoundError:
            existing_data = []

        existing_data.append(new_data)
        with open("pos.json", "w") as json_file:
            json_file.write('\n')
            json.dump(existing_data, json_file, indent=4)

    def data_csv(self, num_alive_sheep):  # TODO czy czysicic plik json i csv na poczatku kazdego wywolania programu
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
                csvwriter.writerow(['Round Number', 'Number of Alive Sheep'])  # TODO czy dopisać nazwy kolumn czy out?

            csvwriter.writerow([self.round, num_alive_sheep])

    def spawn_animals(self):
        self.sheep_list = [
            Sheep(limit=self.limit, movement=self.sheep_move, index=x) for x
            in range(self.sheep_nr)]
        self.wolf = Wolf(sheep_list=self.sheep_list,
                         movement=self.wolf_move)

    def start(self):
        self.spawn_animals()
        for _ in range(self.max_round_nr):
            sheep_alive = 0
            for sheep in self.sheep_list:
                if sheep is not None:
                    sheep_alive += 1
                    sheep.move()
            if sheep_alive == 0:
                print("All sheep are dead")
                break
            index_sheep = self.wolf.move()
            print(self.display_info(sheep_alive, index_sheep))
            self.data_csv(sheep_alive)
            self.data_json()
            self.round += 1
            if self.pause:
                input("Press Enter to continue...")
