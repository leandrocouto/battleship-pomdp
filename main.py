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
    def is_valid(self, battlefield):
        if self.direction == 0:
            print('Sou up. x: ', self.x, ' y: ', self.y, ' length: ', self.length)
        #There's already a ship in this exact coordinate
        if battlefield.grid[self.x][self.y] == 1:
            print('Deu errado')
            return False
        else:
            #Check if it's possible to place this ship according to its direction and length
            #up
            if self.direction == 0:
                if self.length > (self.x+1):
                    return False
                else:
				#Check for ships in the way
                    for i in range(self.x-1, self.x-self.length, -1):
                        if battlefield.grid[i][self.y] == 1:
                            return False
				#Check for ships in the neighborhood
                    for i in range(self.x, self.x-self.length, -1):
                        if i == self.x:
                            if (battlefield.check_cell_for_ship(i+1, self.y) or battlefield.check_cell_for_ship(i+1, self.y-1)
								or battlefield.check_cell_for_ship(i+1, self.y+1) or battlefield.check_cell_for_ship(i, self.y-1)
								or battlefield.check_cell_for_ship(i, self.y+1)) == True:
                                    return False
                        else:
                            if (battlefield.check_cell_for_ship(i-1, self.y-1)
								or battlefield.check_cell_for_ship(i-1, self.y+1) or battlefield.check_cell_for_ship(i, self.y-1)
								or battlefield.check_cell_for_ship(i, self.y+1)) == True:
                                    return False
                            
            #right
            elif self.direction == 1: 
                if self.length > (battlefield.columns - self.y):
                    return False
                else:
					#Check for ships in the way
                    for i in range(self.y+1, self.y+self.length):
                        if battlefield.grid[self.x][i] == 1:
                            return False
                    #Check for ships in the neighborhood
                    for i in range(self.y, self.y+self.length):
                        if i == self.y:
                            if (battlefield.check_cell_for_ship(i+1, self.y) or battlefield.check_cell_for_ship(i+1, self.y-1)
								or battlefield.check_cell_for_ship(i+1, self.y+1) or battlefield.check_cell_for_ship(i, self.y-1)
								or battlefield.check_cell_for_ship(i, self.y+1)) == True:
                                    return False
                        else:
                            if (battlefield.check_cell_for_ship(i-1, self.y-1)
								or battlefield.check_cell_for_ship(i-1, self.y+1) or battlefield.check_cell_for_ship(i, self.y-1)
								or battlefield.check_cell_for_ship(i, self.y+1)) == True:
                                    return False
            #down
            elif self.direction == 2: 
                if self.length > (battlefield.rows - self.x):
                    return False
                else:
					#Check for ships in the way
                    for i in range(self.x+1, self.x+self.length):
                        if battlefield.grid[self.x][i] == 1:
                            return False
            #left
            elif self.direction == 3: 
                if self.length > (self.y+1):
                    return False
                else:
					#Check for ships in the way
                    for i in range(self.y-1, self.y-self.length, -1):
                        if battlefield.grid[i][self.y] == 1:
                            return False
            return True        

class Grid:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = np.zeros((rows, columns))

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
    def check_cell_for_ship(self, x, y):
        if x >= self.rows or x < 0 or y >= self.columns or y < 0:
            return False
        elif self.grid[x][y] == 1:
            return True
        else:
            return False

battlefield = Grid(grid_x, grid_y)

ships = []
ship_length = 2
for _ in range(number_of_ships):
    ship = Ship(random.randrange(grid_x), random.randrange(grid_y),
                random.randrange(4), ship_length)
                #0, ship_length)
    ships.append(ship)
    ship_length += 1
for ship in ships:
    valid_ship = ship.is_valid(battlefield)
    if valid_ship:
        battlefield.place_ship(ship)
    else:
        while valid_ship == False:
            ship.generate_random_ship(grid_x, grid_y, ship.length)
            valid_ship = ship.is_valid(battlefield)
        battlefield.place_ship(ship)
print(battlefield.grid)
for ship in ships:
    ship.print_ship()
