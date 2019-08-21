from battlefield import Battlefield
from ship import Ship
from random import choice
import copy
import random
def valid_actions(grid):
        #List of tuples
        actions = []
        for i in range(10):
            for j in range(10):
                if grid[i][j] == 0 or grid[i][j] == 1:
                    actions.append((i,j))
        return actions

def sample_random_particles(n_particles):
        particles = []
        for _ in range(n_particles): 
            battlefield = Battlefield()
            particles.append(battlefield)
        return particles

def particle_list_update(simulator, old_particle_list, state_from_history, real_action, real_observation):
        updated_particle_list = []
        particles_needing_noise = []
        for _ in range(len(old_particle_list)):
            sampled_belief_state = choice(old_particle_list)
            _, observation_from_sample, _, _ = simulator.step(sampled_belief_state, real_action)
            if real_observation == observation_from_sample:
                updated_particle_list.append(sampled_belief_state)
            else:
                particles_needing_noise.append(sampled_belief_state)
        #if there are not enough particles, then we need particle reinvigoration
        lack_of_particles = len(old_particle_list) - len(updated_particle_list)
        while lack_of_particles != 0:
            noised_belief_state = apply_noise_to_state(choice(particles_needing_noise), state_from_history)
            _, observation_from_sample, _, _ = simulator.step(noised_belief_state, real_action)
            if real_observation == observation_from_sample:
                updated_particle_list.append(noised_belief_state)
                lack_of_particles -= 1
        return updated_particle_list

def apply_noise_to_state(particle_to_transform, state_from_history):
    ships = find_all_ships(particle_to_transform)
    transformation = choice([2])
    if transformation == 1:
        #Two ships of different sizes swap location
        #Choose two ships that have the same direction
        print('transformation 1')
        return swap_location_transformation(particle_to_transform, ships, state_from_history)
    elif transformation == 2:
        #1 or 2 ships are moved to a new location
        print('transformation 2')
        return move_ship_position(particle_to_transform, ships, state_from_history)

def find_all_ships(particle):
        ships = []
        for i in range(particle.rows):
            for j in range(particle.columns):
                if particle.grid[i][j] == 1 and (j+1) != particle.columns:
                    if particle.grid[i][j+1] == 1:
                        ship = []
                        ship_already_found = False
                        for found_ships in ships:
                            for coordinate in found_ships:
                                if (i,j) == coordinate:
                                    ship_already_found = True
                        if ship_already_found:
                            continue
                        k = j
                        while particle.grid[i][k] == 1:
                            ship.append((i,k))
                            k += 1
                            if k == 10:
                                break
                        ships.append(ship)
                if particle.grid[i][j] == 1 and (i+1) != particle.rows:
                    if particle.grid[i+1][j] == 1:
                        ship = []
                        ship_already_found = False
                        for found_ships in ships:
                            for coordinate in found_ships:
                                if (i,j) == coordinate:
                                    ship_already_found = True
                        if ship_already_found:
                            continue
                        k = i
                        while particle.grid[k][j] == 1:
                            ship.append((k,j))
                            k += 1
                            if k == 10:
                                break
                        ships.append(ship)
        return ships



def is_new_particle_valid(particle, state_from_history):
        battlefield = copy.deepcopy(particle)
        for i in range(10):
            for j in range(10):
                if battlefield.grid[i][j] == 1 and state_from_history.grid[i][j] == 2:
                    return False
        ships = find_all_ships(particle)
        if len(ships) < 4:
            return False
        list_of_Ships = []
        for ship in ships:
            aux_ship = Ship(-1, -1, -1, -1)
            aux_ship.ndarray_to_ship(ship)
            list_of_Ships.append(aux_ship)
        is_particle_valid = True
        for ship in list_of_Ships:
            if ship.direction == 1:
                for i in range(ship.y, ship.y + ship.length):
                    battlefield.grid[ship.x][i] = 0
            else:
                for i in range(ship.x, ship.x + ship.length):
                    battlefield.grid[i][ship.y] = 0
            if not battlefield.is_ship_valid(ship):
                is_particle_valid = False
                if ship.direction == 1:
                    for i in range(ship.y, ship.y + ship.length):
                        battlefield.grid[ship.x][i] = 1
                else:
                    for i in range(ship.x, ship.x + ship.length):
                        battlefield.grid[i][ship.y] = 1
                break
            if ship.direction == 1:
                for i in range(ship.y, ship.y + ship.length):
                    battlefield.grid[ship.x][i] = 1
            else:
                for i in range(ship.x, ship.x + ship.length):
                    battlefield.grid[i][ship.y] = 1
        return is_particle_valid

def swap_location_transformation(particle_to_transform, ships, state_from_history):
    while True:
        particle = copy.deepcopy(particle_to_transform)
        indexes = random.sample(range(len(ships)), 2)
        if len(ships[indexes[0]]) == len(ships[indexes[1]]):
            continue
        first_index_row_of_ship1 = ships[indexes[0]][0][0]
        first_index_column_of_ship1 = ships[indexes[0]][0][1]
        last_index_row_of_ship1 = ships[indexes[0]][len(ships[indexes[0]]) - 1][0]
        last_index_column_of_ship1 = ships[indexes[0]][len(ships[indexes[0]]) - 1][1]
        first_index_row_of_ship2 = ships[indexes[1]][0][0]
        first_index_column_of_ship2 = ships[indexes[1]][0][1]
        last_index_row_of_ship2 = ships[indexes[1]][len(ships[indexes[1]]) - 1][0]
        last_index_column_of_ship2 = ships[indexes[1]][len(ships[indexes[1]]) - 1][1]
        #Check if both are in a horizontal direction
        if ships[indexes[0]][0][1] == ships[indexes[0]][1][1] - 1 and \
            ships[indexes[1]][0][1] == ships[indexes[1]][1][1] - 1:
                #If first ship is bigger than the second
                if len(ships[indexes[0]]) > len(ships[indexes[1]]):
                    dif = len(ships[indexes[0]]) - len(ships[indexes[1]])
                    #Check if it can append the difference at the end of the second ship
                    if last_index_column_of_ship2 + dif < particle.columns:
                        #Add at the end of second ship
                        for i in range(dif):
                            particle.grid[last_index_row_of_ship2][last_index_column_of_ship2 + (i + 1)] = 1
                        #Remove from the start of the first ship
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship1][first_index_column_of_ship1 + i] = 0
                        #Check if transformation is valid
                        if not is_new_particle_valid(particle, state_from_history):
                            continue
                    #Check if it can append the difference at the start of the second ship
                    elif first_index_column_of_ship2 - dif >= 0:
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship2][first_index_column_of_ship2 - (i + 1)] = 1
                        #Remove from the end of the first ship
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship1][last_index_column_of_ship1 - i] = 0
                        #Check if transformation is valid
                        if not is_new_particle_valid(particle, state_from_history):
                            continue
                    else:
                        continue
                elif len(ships[indexes[0]]) < len(ships[indexes[1]]):
                    dif = len(ships[indexes[1]]) - len(ships[indexes[0]])
                    #Check if it can append the difference at the end of the first ship
                    if last_index_column_of_ship1 + dif < particle.columns:
                        #Add at the end of second ship
                        for i in range(dif):
                            particle.grid[last_index_row_of_ship1][last_index_column_of_ship1 + (i + 1)] = 1
                        #Remove from the start of the second ship
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship2][first_index_column_of_ship2 + i] = 0
                        #Check if transformation is valid
                        if not is_new_particle_valid(particle, state_from_history):
                            continue
                    #Check if it can append the difference at the start of the first ship
                    elif first_index_column_of_ship1 - dif >= 0:
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship1][first_index_column_of_ship1 - (i + 1)] = 1
                        #Remove from the end of the second ship
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship2][last_index_column_of_ship2 - i] = 0
                        #Check if transformation is valid
                        if not is_new_particle_valid(particle, state_from_history):
                            continue
                    else:
                        continue
                else:
                    continue
                break
        #Check if both are in a vertical direction
        elif ships[indexes[0]][0][0] == ships[indexes[0]][1][0] - 1 and \
            ships[indexes[1]][0][0] == ships[indexes[1]][1][0] - 1:
                #If first ship is bigger than the second
                if len(ships[indexes[0]]) > len(ships[indexes[1]]):
                    dif = len(ships[indexes[0]]) - len(ships[indexes[1]])
                    #Check if it can append the difference at the end of the second ship
                    if last_index_row_of_ship2 + dif < particle.rows:
                        #Add at the end of second ship
                        for i in range(dif):
                            particle.grid[last_index_row_of_ship2 + (i + 1)][last_index_column_of_ship2] = 1
                        #Remove from the start of the first ship
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship1 + i][first_index_column_of_ship1] = 0
                        #Check if transformation is valid
                        if not is_new_particle_valid(particle, state_from_history):
                            continue
                    #Check if it can append the difference at the start of the second ship
                    elif first_index_row_of_ship2 - dif >= 0:
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship2 - (i + 1)][first_index_column_of_ship2] = 1
                        #Remove from the end of the first ship
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship1 - i][last_index_column_of_ship1] = 0
                        #Check if transformation is valid
                        if not is_new_particle_valid(particle, state_from_history):
                            continue
                    else:
                        continue
                elif len(ships[indexes[0]]) < len(ships[indexes[1]]):
                    dif = len(ships[indexes[1]]) - len(ships[indexes[0]])
                    #Check if it can append the difference at the end of the first ship
                    if last_index_row_of_ship1 + dif < particle.rows:
                        #Add at the end of second ship
                        for i in range(dif):
                            particle.grid[last_index_row_of_ship1 + (i + 1)][last_index_column_of_ship1] = 1
                        #Remove from the start of the second ship
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship2 + i][first_index_column_of_ship2] = 0
                        #Check if transformation is valid
                        if not is_new_particle_valid(particle, state_from_history):
                            continue
                    #Check if it can append the difference at the start of the first ship
                    elif first_index_row_of_ship1 - dif >= 0:
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship1 - (i + 1)][first_index_column_of_ship1] = 1
                        #Remove from the end of the second ship
                        for i in range(dif):
                            particle.grid[first_index_row_of_ship2 - i][last_index_column_of_ship2] = 0
                        #Check if transformation is valid
                        if not is_new_particle_valid(particle, state_from_history):
                            continue
                    else:
                        continue
                else:
                    continue
                break
        else:
            continue
    return particle

def move_ship_position(particle_to_transform, ships, state_from_history):
    particle = copy.deepcopy(particle_to_transform)
    number_of_ships_moved = choice([1,2])
    indexes_of_ships_to_be_changed = list(range(0, number_of_ships_moved))
    random.shuffle(indexes_of_ships_to_be_changed)
    for i in range(number_of_ships_moved):
        ship_selected = Ship(-1, -1, -1, -1)
        ship_selected.ndarray_to_ship(ships[indexes_of_ships_to_be_changed[i]])
        #First delete it from the grid
        for i in range(ship_selected.length):
            if ship_selected.direction == 1: #right
                particle.grid[ship_selected.x][ship_selected.y + i] = 0
            elif ship_selected.direction == 2: #down
                particle.grid[ship_selected.x + i][ship_selected.y] = 0
        #Randomize a new position and then check if it is a valid one
        while True:
            new_ship = Ship(random.randrange(particle.rows), random.randrange(particle.columns),
                    random.randint(1,2), ship_selected.length)
            #if the ship won't fit
            if new_ship.direction == 1:
                if new_ship.length > (particle.columns - new_ship.y):
                    continue
            if new_ship.direction == 2:
                if new_ship.length > (particle.rows - new_ship.x):
                    continue
            temp_particle = copy.deepcopy(particle)
            for i in range(new_ship.length):
                if new_ship.direction == 1: #right
                    temp_particle.grid[new_ship.x][new_ship.y + i] = 1
                elif new_ship.direction == 2: #down
                    temp_particle.grid[new_ship.x + i][new_ship.y] = 1
            if is_new_particle_valid(temp_particle, state_from_history):
                particle = copy.deepcopy(temp_particle)
                break
    return particle

