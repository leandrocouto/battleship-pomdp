from ship import Ship
from grid import Grid

import random

class Simulator:
    def __init__(grid_x = 10, grid_y = 10, n_ships = 4):
        self.battlefield = create_grid(grid_x, grid_y, n_ships)
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.n_ships = n_ships
    def create_grid(grid_x, grid_y, n_ships):
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
                while not valid_ship:
                    ship.generate_random_ship(grid_x, grid_y, ship.length)
                    valid_ship = battlefield.is_ship_valid(ship)
                self.battlefield.place_ship(ship)
    def valid_actions(self):
        #List of tuples
        actions = []
        for i in range(self.grid_x):
            for j in range(self.grid_y):
                if self.battlefield[i,j] == 0 or self.battlefield[i,j] == 1:
                    actions.append((i,j))
        return actions
    def sample(self, state, action):
        return successor_state, observation, reward