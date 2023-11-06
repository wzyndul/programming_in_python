from animal import Animal


class Wolf(Animal):

    def __init__(self, sheep_list, movement):
        super().__init__(movement)
        self.__sheep_list = sheep_list

    def move(self):
        pass

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y


wolf = Wolf(2, 1)
print(wolf.get_x())
print(wolf.get_y())
