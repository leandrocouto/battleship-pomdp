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