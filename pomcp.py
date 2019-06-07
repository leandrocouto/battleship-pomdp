from random import choice
from simulator import Simulator
from tree import Tree
import random

class POMCP:
    def __init__(self, Simulator=1, gamma=0.1, c=1, threshold=1, timeout=1, n_particles=1):
        self.gamma = gamma
        if gamma >= 1:
            raise ValueError('Gamma value should be less than 1.')
        self.Simulator = Simulator
        self.threshold = threshold
        self.c = c
        self.timeout = timeout
        self.n_particles = n_particles
        self.tree = Tree()
    def simulate(self):
        print()
    def rollout(self, s, depth):
        # Check significance of update
        if (self.gamma**depth < self.e or self.gamma == 0 ) and depth != 0:
            return 0
        
        total_reward = 0
        
        # Pick random action; maybe change this later
        # Need to also add observation in history if this is changed
        action = choice(self.actions)
        
        # Generate states and observations
        successor_state, _, reward = self.Simulator(s,action)
        total_reward += reward + self.gamma*self.Rollout(successor_state, depth + 1)
        return total_reward
    def search(self):
        particles = self.tree.nodes[-1].particle_list.copy()
        #Loop until timeout
        for _ in range(self.timeout):
            if len(particles) == 0:
                state = choice(self.states)
            else:
                state = choice(particles)
            self.simulate(state, -1, 0)
        best_action, _ = self.search_best(-1)
        return best_action
    def search_best(self, h):
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
    def sample_random_particles(self, k):
        particles = []
        for _ in range(k): 
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
        for ship in ships:
            print(ship)
        return ships
    def apply_noise_to_state(self, particle):
        print(particle)
        rows, columns = particle.shape
        ships = self.find_all_ships(particle)
        transformation = 1#choice([1,2,3])
        if transformation == 1:
            #Two ships of different sizes swap location
            #Choose two ships that have the same direction
            ship_one = []
            ship_two = []
            while True:
                indexes = random.sample(range(len(ships)), 2)
                print('sorteados:' , indexes)
                #Check if both are in a horizontal direction
                if ships[indexes[0]][0][1] == ships[indexes[0]][1][1] - 1 and \
                    ships[indexes[1]][0][1] == ships[indexes[1]][1][1] - 1:
                        if len(ships[indexes[0]]) > len(ships[indexes[1]]):
                            dif = len(ships[indexes[0]]) - len(ships[indexes[1]])
                            if ships[indexes[1]][len(ships[indexes[1]]) - 1] + dif < 
                        break
                #Check if both are in a vertical direction
                if ships[indexes[0]][0][0] == ships[indexes[0]][1][0] - 1 and \
                    ships[indexes[1]][0][0] == ships[indexes[1]][1][0] - 1:
                        break
            print('deu certo')
            
        elif transformation == 2:
            print()
        else:
            print()

    