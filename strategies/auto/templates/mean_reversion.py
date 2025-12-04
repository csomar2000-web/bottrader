from strategies.base_strategy import Strategy

class MeanReversionStrategy(Strategy):
    def generate_signal(self, data):
        z = data.get("zclose", 0)
        if z < -self.config.get("z", 1):
            return {"action": "buy", "confidence": abs(z)}
        if z > self.config.get("z", 1):
            return {"action": "sell", "confidence": abs(z)}
