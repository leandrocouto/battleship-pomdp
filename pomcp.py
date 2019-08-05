from random import choice
from simulator import Simulator
from tree import Tree
from grid import Grid
from ship import Ship
from utils import valid_actions
import random
import copy

class POMCP:
    def __init__(self, simulator, gamma, c, threshold, timeout, n_particles):
        self.gamma = gamma
        if gamma >= 1:
            raise ValueError('Gamma value should be less than 1.')
        self.simulator = simulator
        self.threshold = threshold
        self.c = c
        self.timeout = timeout
        self.n_particles = n_particles
        self.tree = Tree(simulator.start_state)
        self.history = History()
    def simulate(self, s, h, depth):
        # Check significance of update
        if (self.gamma**depth < self.threshold or self.gamma == 0 ) and depth != 0:
            return 0
        
        # If it is a leaf node
        if self.tree.is_leaf_node(self.tree.nodes[h]):
            for action in valid_actions(self.tree.nodes[h]):
                print(action)
                self.tree.expand(h, action, IsAction=True)
            reward_from_rollout = self.rollout(s,depth)
            self.tree.nodes[h].n_visits += 1
            self.tree.nodes[h].value = reward_from_rollout
            return reward_from_rollout
        
        total_reward = 0
        # Get best action and node (with applied action - "ha") given h
        a, ha = self.search_best_action(h)
        
        sample_state, sample_observation, reward, is_terminal = self.simulator.step(s, a)
        # Get "hao" node
        hao = self.tree.get_observation_node(ha, sample_observation)
        # Estimate node Value
        total_reward += reward + self.gamma*self.simulate(sample_state, hao, depth + 1)
        
        self.tree.nodes[h].particle_list.append(s)
        #Just in case adding the new state in the particles list reaches the total 
        #number of particles set previously
        if len(self.tree.nodes[h].particle_list) > self.no_particles:
            self.tree.nodes[h].particle_list = self.tree.nodes[h].particle_list[1:]
        self.tree.nodes[h].n_visits += 1
        self.tree.nodes[ha].n_visits += 1
        self.tree.nodes[ha].value += (total_reward - self.tree.nodes[ha].value)/self.tree.nodes[ha].n_visits
        return total_reward
        
    def rollout(self, s, depth):
        # Check significance of update
        if (self.gamma**depth < self.e or self.gamma == 0 ) and depth != 0:
            return 0
            
        # Uniform random rollout policy
        action = choice(s.valid_actions())
        
        # Generate states and observations from the simulator
        successor_state, observation, reward = self.Simulator(s,action)
        return reward + self.gamma*self.rollout(successor_state, depth + 1)
    def search(self):
        particles = self.tree.nodes[-1].particle_list.copy()
        #Loop until timeout
        for _ in range(self.timeout):
            if len(particles) == 0:
                state = choice(self.sample_random_particles())
            else:
                state = choice(particles)
            self.simulate(state, -1, 0)
        best_action, _ = self.search_best_action(-1)
        return best_action
    def search_best_action(self, h):
        max_value = None
        result = None
        resulta = None
        #if it is not an action node
        if self.tree.nodes[h].particle_list != -1:
            children = self.tree.nodes[h].children
            # UCB for each child node
            for action, child in children.items():
                # if node is unvisited return it
                if self.tree.nodes[child].n_visits == 0:
                    return action, child
                ucb = UCB(self.tree.nodes[h].n_visits, self.tree.nodes[child].n_visits, 
                self.tree.nodes[child].value, self.c)
        
                # Max is kept 
                if max_value is None or max_value < ucb:
                    max_value = ucb
                    result = child
                    resulta = action
        #return action-child_id values
        return resulta, result
    def sample_random_particles(self):
        particles = []
        for _ in range(self.n_particles): 
            battlefield = Grid()
            particles.append(battlefield.grid)
        return particles
    def particle_list_update(self, old_particle_list, real_action, real_observation):
        updated_particle_list = []
        particles_needing_noise = []
        for _ in range(len(old_particle_list)):
            sampled_belief_state = choice(old_particle_list)
            _, observation_from_sample, _ = Simulator(sampled_belief_state, real_action)
            if real_observation == observation_from_sample:
                updated_particle_list.append(sampled_belief_state)
            else:
                particles_needing_noise.append(sampled_belief_state)
        #if there are not enough particles, then we need particle reinvigoration
        lack_of_particles = len(old_particle_list) - len(updated_particle_list)
        while lack_of_particles != 0:
            noised_belief_state = apply_noise_to_state(choice(particles_needing_noise))
            _, observation_from_sample, _ = Simulator(noised_belief_state, real_action)
            if real_observation == observation_from_sample:
                updated_particle_list.append(noised_belief_state)
                lack_of_particles -= 1
        return updated_particle_list
    def find_all_ships(self, particle):
        rows, columns = particle.shape
        ships = []
        for i in range(rows):
            for j in range(columns):
                if particle[i][j] == 1 and (j+1) != columns:
                    if particle[i][j+1] == 1:
                        ship = []
                        ship_already_found = False
                        for found_ships in ships:
                            for coordinate in found_ships:
                                if (i,j) == coordinate:
                                    ship_already_found = True
                        if ship_already_found:
                            continue
                        k = j
                        while particle[i][k] == 1:
                            ship.append((i,k))
                            k += 1
                            if k == 10:
                                break
                        ships.append(ship)
                if particle[i][j] == 1 and (i+1) != rows:
                    if particle[i+1][j] == 1:
                        ship = []
                        ship_already_found = False
                        for found_ships in ships:
                            for coordinate in found_ships:
                                if (i,j) == coordinate:
                                    ship_already_found = True
                        if ship_already_found:
                            continue
                        k = i
                        while particle[k][j] == 1:
                            ship.append((k,j))
                            k += 1
                            if k == 10:
                                break
                        ships.append(ship)
        return ships
    def is_new_particle_valid(self, particle):
        battlefield = Grid()
        battlefield.set_grid(particle)
        ships = self.find_all_ships(particle)
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
    def swap_location_transformation(self, particle_to_transform, ships, rows, columns):
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
                        if last_index_column_of_ship2 + dif < columns:
                            #Add at the end of second ship
                            for i in range(dif):
                                particle[last_index_row_of_ship2][last_index_column_of_ship2 + (i + 1)] = 1
                            #Remove from the start of the first ship
                            for i in range(dif):
                                particle[first_index_row_of_ship1][first_index_column_of_ship1 + i] = 0
                            #Check if transformation is valid
                            if not self.is_new_particle_valid(particle):
                                continue
                        #Check if it can append the difference at the start of the second ship
                        elif first_index_column_of_ship2 - dif >= 0:
                            for i in range(dif):
                                particle[first_index_row_of_ship2][first_index_column_of_ship2 - (i + 1)] = 1
                            #Remove from the end of the first ship
                            for i in range(dif):
                                particle[first_index_row_of_ship1][last_index_column_of_ship1 - i] = 0
                            #Check if transformation is valid
                            if not self.is_new_particle_valid(particle):
                                continue
                        else:
                            continue
                    elif len(ships[indexes[0]]) < len(ships[indexes[1]]):
                        dif = len(ships[indexes[1]]) - len(ships[indexes[0]])
                        #Check if it can append the difference at the end of the first ship
                        if last_index_column_of_ship1 + dif < columns:
                            #Add at the end of second ship
                            for i in range(dif):
                                particle[last_index_row_of_ship1][last_index_column_of_ship1 + (i + 1)] = 1
                            #Remove from the start of the second ship
                            for i in range(dif):
                                particle[first_index_row_of_ship2][first_index_column_of_ship2 + i] = 0
                            #Check if transformation is valid
                            if not self.is_new_particle_valid(particle):
                                continue
                        #Check if it can append the difference at the start of the first ship
                        elif first_index_column_of_ship1 - dif >= 0:
                            for i in range(dif):
                                particle[first_index_row_of_ship1][first_index_column_of_ship1 - (i + 1)] = 1
                            #Remove from the end of the second ship
                            for i in range(dif):
                                particle[first_index_row_of_ship2][last_index_column_of_ship2 - i] = 0
                            #Check if transformation is valid
                            if not self.is_new_particle_valid(particle):
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
                        if last_index_row_of_ship2 + dif < rows:
                            #Add at the end of second ship
                            for i in range(dif):
                                particle[last_index_row_of_ship2 + (i + 1)][last_index_column_of_ship2] = 1
                            #Remove from the start of the first ship
                            for i in range(dif):
                                particle[first_index_row_of_ship1 + i][first_index_column_of_ship1] = 0
                            #Check if transformation is valid
                            if not self.is_new_particle_valid(particle):
                                continue
                        #Check if it can append the difference at the start of the second ship
                        elif first_index_row_of_ship2 - dif >= 0:
                            for i in range(dif):
                                particle[first_index_row_of_ship2 - (i + 1)][first_index_column_of_ship2] = 1
                            #Remove from the end of the first ship
                            for i in range(dif):
                                particle[first_index_row_of_ship1 - i][last_index_column_of_ship1] = 0
                            #Check if transformation is valid
                            if not self.is_new_particle_valid(particle):
                                continue
                        else:
                            continue
                    elif len(ships[indexes[0]]) < len(ships[indexes[1]]):
                        dif = len(ships[indexes[1]]) - len(ships[indexes[0]])
                        #Check if it can append the difference at the end of the first ship
                        if last_index_row_of_ship1 + dif < rows:
                            #Add at the end of second ship
                            for i in range(dif):
                                particle[last_index_row_of_ship1 + (i + 1)][last_index_column_of_ship1] = 1
                            #Remove from the start of the second ship
                            for i in range(dif):
                                particle[first_index_row_of_ship2 + i][first_index_column_of_ship2] = 0
                            #Check if transformation is valid
                            if not self.is_new_particle_valid(particle):
                                continue
                        #Check if it can append the difference at the start of the first ship
                        elif first_index_row_of_ship1 - dif >= 0:
                            for i in range(dif):
                                particle[first_index_row_of_ship1 - (i + 1)][first_index_column_of_ship1] = 1
                            #Remove from the end of the second ship
                            for i in range(dif):
                                particle[first_index_row_of_ship2 - i][last_index_column_of_ship2] = 0
                            #Check if transformation is valid
                            if not self.is_new_particle_valid(particle):
                                continue
                        else:
                            continue
                    else:
                        continue
                    break
            else:
                continue
        return particle
    def move_ship_position(self, particle_to_transform, ships, rows, columns):
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
                    particle[ship_selected.x][ship_selected.y + i] = 0
                elif ship_selected.direction == 2: #down
                    particle[ship_selected.x + i][ship_selected.y] = 0
            #Randomize a new position and then check if it is a valid one
            while True:
                new_ship = Ship(random.randrange(rows), random.randrange(columns),
                        random.randint(1,2), ship_selected.length)
                #if the ship won't fit
                if new_ship.direction == 1:
                    if new_ship.length > (columns - new_ship.y):
                        continue
                if new_ship.direction == 2:
                    if new_ship.length > (rows - new_ship.x):
                        continue
                temp_particle = copy.deepcopy(particle)
                for i in range(new_ship.length):
                    if new_ship.direction == 1: #right
                        temp_particle[new_ship.x][new_ship.y + i] = 1
                    elif new_ship.direction == 2: #down
                        temp_particle[new_ship.x + i][new_ship.y] = 1
                if self.is_new_particle_valid(temp_particle):
                    particle = copy.deepcopy(temp_particle)
                    break
        return particle
    def apply_noise_to_state(self, particle_to_transform):
        print('PARTICLE TO TRANSFORM')
        print(particle_to_transform)
        rows, columns = particle_to_transform.shape
        ships = self.find_all_ships(particle_to_transform)
        transformation = 2#choice([1,2,3])
        if transformation == 1:
            #Two ships of different sizes swap location
            #Choose two ships that have the same direction
            return self.swap_location_transformation(particle_to_transform, ships, rows, columns)
        elif transformation == 2:
            #1 or 2 ships are moved to a new location
            return self.move_ship_position(particle_to_transform, ships, rows, columns)
        else:
            print()

    