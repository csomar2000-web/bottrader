import numpy as np

class StrategyController:
    def __init__(self, cfg, strategies):
        self.cfg = cfg
        self.strategies = strategies
        self.weights = {}

    def score(self, metrics, sentiment, regime):
        p = metrics["profit"]
        d = metrics["drawdown"]
        v = metrics["volatility"]
        s = sentiment["score"]
        r = 1 if regime == "trend" else -1 if regime == "high_volatility" else 0
        return p - d - v + s + r

    def decide(self, reports, sentiment, regime):
        best = None
        best_score = -1e9
        for name, m in reports.items():
            sc = self.score(m, sentiment, regime)
            self.weights[name] = sc
            if sc > best_score:
                best = name
                best_score = sc
        return best

    def apply(self, selected):
        for name in self.strategies.list():
            if name == selected:
                self.strategies.enable(name)
            else:
                self.strategies.disable(name)
        return selected
