import random

class Ship:
    def __init__(self, x, y, direction, length):
        self.x = x
        self.y = y
        self.direction = direction
        self.length = length
    def generate_random_ship(self, rows, columns, length):
        self.x = random.randrange(rows)
        self.y = random.randrange(columns)
        self.direction = random.randrange(4)
        self.length = length
    def ndarray_to_ship(self, coordinates):
        self.x = coordinates[0][0]
        self.y = coordinates[0][1]
        self.length = len(coordinates)
        if coordinates[0][1] < coordinates[1][1]:
            self.direction = 1
        elif coordinates[0][0] < coordinates[1][0]:
            self.direction = 2
            