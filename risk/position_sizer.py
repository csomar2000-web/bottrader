import numpy as np

class PositionSizer:
    def __init__(self, cfg):
        self.cfg = cfg
        self.min_vol = cfg.get("min_vol", 0.0001)
        self.max_leverage = cfg.get("max_leverage", 3)
        self.max_position_value = cfg.get("max_position_value", 0.2)  # 20% of balance
        self.kelly_factor = cfg.get("kelly_factor", 0.5)

    def size(self, balance, price, volatility, confidence, regime):
        vol = max(volatility, self.min_vol)

        # Base size in dollars (risk-based)
        risk_pct = self.cfg.get("risk_per_trade", 0.01)
        base_risk = balance * risk_pct  

        # Leverage factor
        leverage_factor = min(self.max_leverage, 1 / vol)

        # Confidence scaling
        conf_factor = np.clip(confidence, 0.1, 2.0)

        # Regime multiplier
        regime_factor = self._regime_mult(regime)

        # Kelly sizing modification
        kelly_mult = self.kelly_factor

        position_value = base_risk * leverage_factor * conf_factor * regime_factor * kelly_mult

        # Cap position value
        position_value = min(position_value, balance * self.max_position_value)

        # Convert dollars → asset units
        size_units = position_value / price

        return max(0, size_units)

    def _regime_mult(self, regime):
        return {
            "high_volatility": 0.4,
            "low_volatility": 1.5,
            "trend": 1.3,
            "ranging": 0.9,
        }.get(regime, 1.0)
