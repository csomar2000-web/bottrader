from strategies.base_strategy import Strategy

class MomentumStrategy(Strategy):
    def generate_signal(self, data):
        r = data.get("return", 0)
        if r > self.config.get("threshold", 0.001):
            return {"action": "buy", "confidence": r}
        if r < -self.config.get("threshold", 0.001):
            return {"action": "sell", "confidence": abs(r)}
