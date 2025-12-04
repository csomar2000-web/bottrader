from execution.trade_manager import TradeManager
from execution.hft_executor import HFTExecutor
from execution.hft_router import HFTRouter

class HybridExecutor:
    def __init__(self, cfg, exchanges):
        self.cfg = cfg
        self.regular = TradeManager(exchanges, cfg["regular"])
        self.hft = HFTExecutor(cfg["hft"])
        self.router = HFTRouter({})

    def update_ticks(self, ticks):
        self.router.feeds = ticks

    def execute(self, order, tick):
        if order["size"] <= self.cfg.get("hft_threshold", 0.001):
            b = self.router.best_tick()
            return self.hft.execute(b, order["side"], order["size"])
        return self.regular.process(order, tick)
