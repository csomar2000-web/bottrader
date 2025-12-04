from strategies.base_strategy import Strategy
from ml.inference.predictor import Predictor

class TransformerStrategy(Strategy):
    def __init__(self, name, cfg):
        super().__init__(name, cfg)
        self.model = Predictor(cfg["model"])

    def generate_signal(self, data):
        out = self.model.predict(data)
        p = out["prediction"]
        c = out["confidence"]
        if abs(p) < self.config.get("threshold", 0.001):
            return None
        return {
            "action": "buy" if p > 0 else "sell",
            "confidence": c,
            "strength": abs(p)
        }
