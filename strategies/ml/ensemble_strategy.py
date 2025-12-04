from strategies.base_strategy import Strategy
from ml.inference.ensemble import EnsemblePredictor

class EnsembleAI(Strategy):
    def __init__(self, name, cfg):
        super().__init__(name, cfg)
        self.ensemble = EnsemblePredictor(cfg["models"], cfg["weights"])

    def generate_signal(self, data):
        out = self.ensemble.predict(data)
        p = out["prediction"]
        c = out["confidence"]
        if c < self.config.get("min_conf", 0.5):
            return None
        return {"action": "buy" if p > 0 else "sell", "confidence": c, "value": p}
