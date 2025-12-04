class PortfolioMetrics:
    def __init__(self):
        self.realized_pnl = 0
        self.unrealized_pnl = 0

    def pnl(self, pos, fill):
        if pos["side"] == "long":
            return (fill["price"] - pos["entry"]) * pos["size"]
        return (pos["entry"] - fill["price"]) * pos["size"]

    def update_realized(self, pnl):
        self.realized_pnl += pnl

    def unrealized(self, pos, price):
        if pos["side"] == "long":
            return (price - pos["entry"]) * pos["size"]
        return (pos["entry"] - price) * pos["size"]

    def equity(self, balance):
        return balance + self.realized_pnl + self.unrealized_pnl

    def stats(self):
        return {
            "realized": self.realized_pnl,
            "unrealized": self.unrealized_pnl,
            "total": self.realized_pnl + self.unrealized_pnl
        }
