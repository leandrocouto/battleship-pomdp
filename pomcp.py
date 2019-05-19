class POMCP:
    def __init__(self, generator, gamma, c, threshold, timeout, n_particles):
        self.gamma = gamma
        if gamma >= 1:
            raise ValueError('Gamma value should be less than 1.')
        self.generator = generator
        self.threshold = threshold
        self.c = c
        self.timeout = timeout
        self.n_particles = n_particles
        self.tree = Tree()
    def simulate():
        print()
    def rollout():
        print()
    