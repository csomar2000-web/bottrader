from strategies.base_strategy import Strategy
from ml.inference.predictor import Predictor

class LSTMStrategy(Strategy):
    def __init__(self, name, cfg):
        super().__init__(name, cfg)
        self.model = Predictor(cfg["model"])

    def generate_signal(self, data):
        out = self.model.predict(data)
        p = out["prediction"]
        c = out["confidence"]

        if p > 0 and c >= self.config.get("min_conf", 0.4):
            return {"action": "buy", "confidence": c, "value": p}
        if p < 0 and c >= self.config.get("min_conf", 0.4):
            return {"action": "sell", "confidence": c, "value": p}
        return None
