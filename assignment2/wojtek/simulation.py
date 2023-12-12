import csv
import json
import logging
import os

from sheep import Sheep
from wolf import Wolf


class Simulation:

    def __init__(self, max_round_nr, sheep_nr, limit, sheep_move, wolf_move,
                 pause, logger=None):
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
        self.logger = logger

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
        sheep_pos = [[sheep.x, sheep.y] if sheep is not None else None for
                     sheep in self.sheep_list]
        new_data = {"round_no": self.round,
                    "wolf_pos": [self.wolf.x, self.wolf.y],
                    "sheep_pos": sheep_pos}

        try:
            with open("pos.json", "r") as json_file:
                try:
                    existing_data = json.load(json_file)  # Load existing data
                except json.JSONDecodeError:
                    existing_data = []
        except FileNotFoundError:
            existing_data = []

        if self.round == 0:  # If round number is 0, overwrite the file
            with open("pos.json", "w") as json_file:
                json.dump([new_data], json_file, indent=4)
        else:  # If round number is not 0, append to the file
            existing_data.append(new_data)
            with open("pos.json", "w") as json_file:
                json.dump(existing_data, json_file, indent=4)

        if self.logger:
            self.logger.debug(f"simulation data was saved to json file.")

    def data_csv(self, num_alive_sheep):
        file_exists = os.path.isfile('alive.csv')
        with open('alive.csv', 'a' if file_exists and self.round != 0 else 'w',
                  newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow([self.round, num_alive_sheep])

        if self.logger:
            self.logger.debug(f"simulation data was saved to csv file.")

    def spawn_animals(self):
        self.sheep_list = [
            Sheep(limit=self.limit, movement=self.sheep_move, index=x,
                  logger=self.logger) for x in
            range(self.sheep_nr)]
        self.wolf = Wolf(sheep_list=self.sheep_list,
                         movement=self.wolf_move)
        if self.logger:
            self.logger.info(f"initial positions of all sheep were determined")

    def start(self):
        self.spawn_animals()
        for _ in range(self.max_round_nr):
            if self.logger:
                self.logger.info(f"round number: {self.round} just started")
            sheep_alive = 0
            for sheep in self.sheep_list:
                if sheep is not None:
                    sheep_alive += 1
                    sheep.move()
            if self.logger:
                self.logger.info(f"all alive sheep moved")
            if sheep_alive == 0:
                if self.logger:
                    self.logger.info(f"simulation ended all sheep are dead")
                print("All sheep are dead")
                break
            index_sheep = self.wolf.move()
            if self.logger:
                if self.sheep_list[index_sheep] is None:
                    self.logger.info(f"sheep number: {index_sheep} was eaten")
                else:
                    self.logger.info(
                        f"wolf is chasing sheep number: {index_sheep}")
                self.logger.info(
                    f"End of the round number,"
                    f" number of alive sheep: {sheep_alive}")
            print(self.display_info(sheep_alive, index_sheep))
            self.data_csv(sheep_alive)
            self.data_json()
            self.round += 1
            if self.pause:
                input("Press Enter to continue...")
        if self.logger:
            self.logger.info(f"simulation ended max round number reached")
