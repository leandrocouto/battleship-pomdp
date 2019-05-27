class POMCP:
    def __init__(self, Simulator, gamma, c, threshold, timeout, n_particles):
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
    def rollout(self):
        print()
    def search(self):
        particles = self.tree.nodes[-1].particle_list.copy()
        #Loop until timeout
        for _ in range(self.timeout):
            if len(particles) == 0:
                state = choice(self.states)
            else:
                state = choice(particles)
            self.simulate(state, -1, 0)
        best_action, _ = self.SearchBest(-1, UseUCB = False)
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

    