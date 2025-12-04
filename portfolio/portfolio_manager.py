import time
from typing import Dict, Any
from portfolio.metrics import PortfolioMetrics
from portfolio.hedging import HedgingEngine

class PortfolioManager:
    def __init__(self, cfg):
        self.cfg = cfg
        self.balance = cfg.get("starting_balance", 10000)
        self.positions = {}    # {symbol: [positions]}
        self.metrics = PortfolioMetrics()
        self.hedger = HedgingEngine(cfg.get("hedging", {}))

    def open(self, fill):
        sym = fill["symbol"]

        if sym not in self.positions:
            self.positions[sym] = []

        pos = {
            "side": fill["side"],   # long or short
            "size": fill["size"],
            "entry": fill["price"],
            "timestamp": time.time()
        }
        self.positions[sym].append(pos)

    def close(self, fill):
        sym = fill["symbol"]

        if sym not in self.positions or not self.positions[sym]:
            return

        pos = self.positions[sym].pop(0)

        pnl = self.metrics.pnl(pos, fill)
        self.balance += pnl
        self.metrics.update_realized(pnl)

        if not self.positions[sym]:
            del self.positions[sym]

    def update_unrealized(self, market):
        total = 0

        for sym, pos_list in self.positions.items():
            price = market["mid"]
            for pos in pos_list:
                total += self.metrics.unrealized(pos, price)

        self.metrics.unrealized_pnl = total
        return total

    def exposure(self):
        out = {}

        for sym, pos_list in self.positions.items():
            long_exp = sum(p["size"] for p in pos_list if p["side"] == "long")
            short_exp = sum(p["size"] for p in pos_list if p["side"] == "short")
            out[sym] = {"long": long_exp, "short": short_exp}

        return out

    def process_fill(self, fill, market):
        if fill["type"] == "open":
            self.open(fill)
        else:
            self.close(fill)

        self.update_unrealized(market)
        hedges = self.hedger.evaluate(self.balance, self.exposure(), market)
        return hedges
