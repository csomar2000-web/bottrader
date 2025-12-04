from strategies.base_strategy import Strategy

class GridStrategy(Strategy):
    def generate_signal(self, data):
        price = data["mid"]
        upper = self.config["upper"]
        lower = self.config["lower"]
        step = self.config["step"]

        if price <= lower:
            return {"action": "buy", "level": "lower"}

        if price >= upper:
            return {"action": "sell", "level": "upper"}

        grid_levels = self._levels(lower, upper, step)
        for lvl in grid_levels:
            if abs(price - lvl) <= step * 0.1:
                side = "buy" if price < lvl else "sell"
                return {"action": side, "grid": lvl}
        return None

    def _levels(self, low, high, step):
        return [low + i * step for i in range(int((high - low) / step) + 1)]
