import random
from strategies.auto.registry import STRATEGY_TEMPLATES

class StrategyGenerator:
    def __init__(self, cfg):
        self.cfg = cfg

    def generate(self):
        name = random.choice(list(STRATEGY_TEMPLATES.keys()))
        cls = STRATEGY_TEMPLATES[name]
        params = self._random_params()
        return cls(f"auto_{name}", params)

    def _random_params(self):
        p = self.cfg["param_space"]
        return {k: random.uniform(*v) for k, v in p.items()}
