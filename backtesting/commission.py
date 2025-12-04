class CommissionModel:
    def __init__(self, cfg):
        self.maker = cfg.get("maker", 0.0002)
        self.taker = cfg.get("taker", 0.0004)

    def calculate(self, fill):
        fee_rate = self.taker
        return fill["price"] * fill["size"] * fee_rate
