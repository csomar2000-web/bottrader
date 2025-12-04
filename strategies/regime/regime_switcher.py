from strategies.base_strategy import Strategy

class RegimeSwitcher(Strategy):
    def __init__(self, name, cfg):
        super().__init__(name, cfg)
        self.strategies = cfg["strategies"]

    def generate_signal(self, data):
        regime = data.get("regime", "normal")
        strat = self.strategies.get(regime)
        if strat is None:
            return None
        return strat.run(data)
