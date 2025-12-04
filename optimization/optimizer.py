import numpy as np
from backtesting.backtester import Backtester

class Optimizer:
    def __init__(self, cfg, data):
        self.cfg = cfg
        self.data = data

    def grid_search(self, params):
        best = None
        best_eq = -1e9
        for p in params:
            cfg = self._inject(p)
            bt = Backtester(cfg, self.data)
            r = bt.run()
            eq = r[-1]
            if eq > best_eq:
                best_eq = eq
                best = p
        return best, best_eq

    def random_search(self, space, n=20):
        best = None
        best_eq = -1e9
        for _ in range(n):
            p = {k: np.random.uniform(*v) for k, v in space.items()}
            cfg = self._inject(p)
            bt = Backtester(cfg, self.data)
            r = bt.run()
            eq = r[-1]
            if eq > best_eq:
                best = p
                best_eq = eq
        return best, best_eq

    def _inject(self, params):
        c = self.cfg.copy()
        for k, v in params.items():
            c["strategies"][list(c["strategies"].keys())[0]]["params"][k] = v
        return c
