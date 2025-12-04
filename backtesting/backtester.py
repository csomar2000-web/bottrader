import numpy as np
from portfolio.portfolio_manager import PortfolioManager
from risk.risk_manager import RiskManager
from execution.trade_manager import TradeManager
from strategies.strategy_loader import StrategyLoader

class Backtester:
    def __init__(self, cfg, data):
        self.cfg = cfg
        self.data = data
        self.portfolio = PortfolioManager(cfg["portfolio"])
        self.risk = RiskManager(cfg["risk"])
        self.execution = TradeManager(cfg["exchanges"], cfg["execution"])
        self.strats = StrategyLoader()
        self.strats.load(cfg["strategies"])
        self.results = []

    def run(self):
        for tick in self.data:
            signals = self.strats.run_all(tick)
            for sig in signals:
                act = self.risk.evaluate(sig, tick, {"balance": self.portfolio.balance})
                if act:
                    fill = self.execution.process(act, tick)
                    hedge = self.portfolio.process_fill(fill, tick)
            eq = self.portfolio.metrics.equity(self.portfolio.balance)
            self.results.append(eq)
        return self.results
