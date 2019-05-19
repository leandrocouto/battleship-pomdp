from ship import Ship
from grid import Grid

import random

grid_x = 10
grid_y = 10
number_of_ships = 4

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
