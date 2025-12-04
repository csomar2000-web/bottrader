class ReportData:
    def __init__(self):
        self.equity = []
        self.trades = []
        self.metrics = {}

    def add_equity(self, v):
        self.equity.append(v)

    def add_trade(self, t):
        self.trades.append(t)

    def set_metrics(self, m):
        self.metrics = m

    def snapshot(self):
        return {
            "equity": self.equity,
            "trades": self.trades,
            "metrics": self.metrics
        }
