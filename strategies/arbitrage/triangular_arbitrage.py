from strategies.base_strategy import Strategy

class TriangularArbitrage(Strategy):
    def generate_signal(self, data):
        a = data.get("A", 1)
        b = data.get("B", 1)
        c = data.get("C", 1)
        diff = (a * b) - c
        if abs(diff) >= self.config.get("min_edge", 0.002):
            return {"action": "arbitrage", "edge": diff}
        return None
