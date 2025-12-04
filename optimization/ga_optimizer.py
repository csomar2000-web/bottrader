import numpy as np
from backtesting.backtester import Backtester

class GAOptimizer:
    def __init__(self, cfg, data, pop=10, gen=15, mut=0.1):
        self.cfg = cfg
        self.data = data
        self.pop = pop
        self.gen = gen
        self.mut = mut

    def random_params(self):
        s = self.cfg["param_space"]
        return {k: np.random.uniform(*v) for k, v in s.items()}

    def mutate(self, p):
        for k in p:
            if np.random.rand() < self.mut:
                r = self.cfg["param_space"][k]
                p[k] = np.random.uniform(*r)
        return p

    def crossover(self, a, b):
        c = {}
        for k in a:
            c[k] = a[k] if np.random.rand() < 0.5 else b[k]
        return c

    def fitness(self, params):
        x = self._inject(params)
        bt = Backtester(x, self.data)
        r = bt.run()
        return r[-1]

    def _inject(self, p):
        c = self.cfg["template"].copy()
        for k, v in p.items():
            c["strategies"]["main"]["params"][k] = v
        return c

    def run(self):
        pop = [self.random_params() for _ in range(self.pop)]
        for _ in range(self.gen):
            scores = np.array([self.fitness(p) for p in pop])
            idx = scores.argsort()[::-1]
            pop = [pop[i] for i in idx[: self.pop // 2]]
            while len(pop) < self.pop:
                a, b = np.random.choice(pop, 2)
                c = self.crossover(a, b)
                pop.append(self.mutate(c))
        best = max(pop, key=self.fitness)
        return best
