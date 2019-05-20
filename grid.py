import numpy as np

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
    #Already assumes that the action is valid (i.e.: not guessing an already guessed cell)
    #Returns the observation (+1 if a ship was hit, 0 otherwise)
    def apply_action(self, action):
        if self.check_for_ship(action[0], action[1]):
            self.grid[action[0]][action[1]] = 2
            return 1 #observation
        else:
            self.grid[action[0]][action[1]] = 2
            return 0 #observation
    def is_terminal(self):
        for i in range(self.rows):
            for j in range(self.columns):
                if self.grid[i,j] == 1: #There's still ships
                    return False
        return True