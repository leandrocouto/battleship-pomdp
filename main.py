from ship import Ship
from battlefield import Battlefield
from history import History
from tree import Tree
from pomcp import POMCP
from random import choice
from simulator import Simulator
from utils import particle_list_update
import copy

simulator = Simulator()
print('inicio')
print(simulator.start_state.grid)
print()
pomcp = POMCP(simulator, 1, 1, 0.005, 100, 100)
time = 0
h = History()
while time < 100:
    time += 1
    print('Time ', time -1)
    print('Estado representado pela raiz')
    action = pomcp.search(h)
    h.add_only_action(action)
    last_state, _ = simulator.get_last_state_and_legal_actions(h)
    print(last_state.grid)
    _, observation, _, _ = simulator.step(last_state, action)
    h.add_only_observation(observation)
    print('Action from POCMP: ', action, 'Real observation: ', observation)
    #Save the 'old' particle list to update afterwards
    old_particle_list = copy.deepcopy(pomcp.tree.nodes[-1].particle_list)
    contador = 0
    for key, value in pomcp.tree.nodes.items():
        contador+=1
    print('Numero de nós antes: ', contador)
    if h in pomcp.tree.nodes:
        print('Antes estava aqui')
    else:
        print('Antes nao estava aqui')
    pomcp.tree.prune_and_make_new_root(action,observation)
    print('Historico oficial')
    h.print_history()
    print('hash dele:', h)
    contador = 0
    for key, value in pomcp.tree.nodes.items():
        #key.print_history()
        #print()
        contador+=1
    print('Numero de nós dps: ', contador)
    if h in pomcp.tree.nodes:
        print('Depois estava aqui')
    else:
        print('Depois nao estava aqui')



    #Now update the belief state
    pomcp.tree.nodes[-1].particle_list = particle_list_update(simulator, old_particle_list, action, observation)