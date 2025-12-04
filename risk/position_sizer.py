import numpy as np

class PositionSizer:
    def __init__(self, cfg):
        self.cfg = cfg

    def size(self, balance, volatility, confidence, regime):
        base = balance * self.cfg.get("risk_per_trade", 0.01)
        vol_factor = 1 / (volatility + 1e-12)
        conf_factor = confidence
        regime_factor = self._regime_mult(regime)
        size = base * vol_factor * conf_factor * regime_factor
        return max(0, size)

    def _regime_mult(self, regime):
        if regime == "high_volatility":
            return self.cfg.get("high_vol_mult", 0.5)
        if regime == "low_volatility":
            return self.cfg.get("low_vol_mult", 1.5)
        if regime == "trend":
            return self.cfg.get("trend_mult", 1.2)
        return 1.0
