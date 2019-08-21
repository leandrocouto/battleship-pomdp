from ship import Ship
from battlefield import Battlefield
from history import History
from tree import Tree
from pomcp import POMCP
from random import choice
from simulator import Simulator
from utils import particle_list_update
from utils import valid_actions
import copy

simulator = Simulator()
print('inicio')
print(simulator.start_state.grid)
print()
pomcp = POMCP(simulator, gamma=1, c=1, epsilon=0.005, n_simulations=100, n_particles=100)
real_initial_state = copy.deepcopy(simulator.start_state)
time = 0
h = History()
while time < 100:
    time += 1
    print('Time ', time -1)
    action = pomcp.search(h)
    h.add_only_action(action)
    #print('Estado representado pela raiz')
    #print(real_initial_state.grid)
    successor_state, observation, _, _ = simulator.step(real_initial_state, action)
    real_initial_state = copy.deepcopy(successor_state)
    h.add_only_observation(observation)
    print('Action from POCMP: ', action, 'Real observation: ', observation)
    #Save the 'old' particle list to update afterwards
    old_particle_list = copy.deepcopy(pomcp.tree.nodes[pomcp.tree.root_key].particle_list)
    #print('tamanho old list: ', len(old_particle_list))
    pomcp.tree.prune_and_make_new_root(action, observation)
    #print('Historico oficial')
    #h.print_history()
    state_from_history, _ = simulator.get_dummy_state_and_legal_actions_given_history(h)
    #Now update the belief state
    pomcp.tree.nodes[pomcp.tree.root_key].particle_list = particle_list_update(simulator, old_particle_list, int(pomcp.n_simulations),
                                                                                 state_from_history, action, observation, 100)
    if len(pomcp.tree.nodes[pomcp.tree.root_key].particle_list) == 0:
        break
print('Out of particles, finishing episode with SelectRandom')
time = 0
while time < 100:
    action = choice(valid_actions(real_initial_state))
    successor_state, observation, reward, is_terminal = simulator.step(real_initial_state, action)
    if is_terminal:
        print('Finished')
        break
    h.add(action, observation)

print('Historico oficial')
h.print_history()

