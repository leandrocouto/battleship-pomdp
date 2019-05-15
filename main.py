import numpy as np
import random

grid_x = 10
grid_y = 10
number_of_ships = 4

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
    def print_ship(self):
        print('x: %d, y: %d, direction: %d, length: %d' %(self.x,self.y,self.direction,self.length))

class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = np.zeros((rows, columns))
    
    #Assume ship is already valid
    def place_ship(self,ship):
        for i in range(ship.length):
            if ship.direction == 0: #up
                self.grid[ship.x - i][ship.y] = 1
            elif ship.direction == 1: #right
                self.grid[ship.x][ship.y + i] = 1
            elif ship.direction == 2: #down
                self.grid[ship.x + i][ship.y] = 1
            elif ship.direction == 3: #left
                self.grid[ship.x][ship.y - i] = 1
    def check_for_ship(self, x, y):
        if x >= self.rows or x < 0 or y >= self.columns or y < 0:
            return False
        elif self.grid[x][y] == 1:
            return True
        else:
            return False
    def is_ship_valid(self, ship):
        #up
        if ship.direction == 0:
            #if the ship won't fit
            if ship.length > (ship.x + 1):
                return False
            else:
                #Check for ships in the neighborhood
                for i in range(ship.x, ship.x-ship.length, -1):
                    if (self.check_for_ship(i+1, ship.y-1) or self.check_for_ship(i+1, ship.y)
								or self.check_for_ship(i+1, ship.y+1) or self.check_for_ship(i, ship.y-1)
								or self.check_for_ship(i, ship.y) or self.check_for_ship(i, ship.y+1)
                                or self.check_for_ship(i-1, ship.y-1) or self.check_for_ship(i-1, ship.y)
                                or self.check_for_ship(i-1, ship.y+1)):
                                    return False
        #right
        elif ship.direction == 1:
            #if the ship won't fit
            if ship.length > (self.columns - ship.y):
                    return False
            else:
                #Check for ships in the neighborhood
                for i in range(ship.y, ship.y+ship.length):
                    if (self.check_for_ship(ship.x-1, i-1) or self.check_for_ship(ship.x, i-1)
								or self.check_for_ship(ship.x+1, i-1) or self.check_for_ship(ship.x-1, i)
								or self.check_for_ship(ship.x, i) or self.check_for_ship(ship.x+1, i)
                                or self.check_for_ship(ship.x-1, i+1) or self.check_for_ship(ship.x, i+1)
                                or self.check_for_ship(ship.x+1, i+1)):
                                    return False
        #down
        elif ship.direction == 2:
            if ship.length > (self.rows - ship.x):
                return False
            else:
                #Check for ships in the neighborhood
                for i in range(ship.x, ship.length+ship.x):
                    if (self.check_for_ship(i+1, ship.y-1) or self.check_for_ship(i+1, ship.y)
								or self.check_for_ship(i+1, ship.y+1) or self.check_for_ship(i, ship.y-1)
								or self.check_for_ship(i, ship.y) or self.check_for_ship(i, ship.y+1)
                                or self.check_for_ship(i-1, ship.y-1) or self.check_for_ship(i-1, ship.y)
                                or self.check_for_ship(i-1, ship.y+1)):
                                    return False
        #left
        elif ship.direction == 3:
            if ship.length > (ship.y+1):
                return False
            else:
                #Check for ships in the neighborhood
                for i in range(ship.y, ship.y-ship.length, -1):
                    if (self.check_for_ship(ship.x-1, i-1) or self.check_for_ship(ship.x, i-1)
								or self.check_for_ship(ship.x+1, i-1) or self.check_for_ship(ship.x-1, i)
								or self.check_for_ship(ship.x, i) or self.check_for_ship(ship.x+1, i)
                                or self.check_for_ship(ship.x-1, i+1) or self.check_for_ship(ship.x, i+1)
                                or self.check_for_ship(ship.x+1, i+1)):
                                    return False
        return True

battlefield = Grid(grid_x, grid_y)

ships = []
ship_length = 2
for _ in range(number_of_ships):
    ship = Ship(random.randrange(grid_x), random.randrange(grid_y),
                random.randrange(4), ship_length)
    ships.append(ship)
    ship_length += 1
for ship in ships:
    valid_ship = battlefield.is_ship_valid(ship)
    if valid_ship:
        battlefield.place_ship(ship)
    else:
        while valid_ship == False:
            ship.generate_random_ship(grid_x, grid_y, ship.length)
            valid_ship = battlefield.is_ship_valid(ship)
        battlefield.place_ship(ship)
print(battlefield.grid)
print()
for ship in ships:
    ship.print_ship()
