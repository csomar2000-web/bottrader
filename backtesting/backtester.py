from backtesting.execution_model import ExecutionModel
from backtesting.commission import CommissionModel

from strategies.strategy_loader import StrategyLoader
from risk.risk_manager import RiskManager
from portfolio.portfolio_manager import PortfolioManager


class BacktesterV2:
    def __init__(self, cfg, ohlcv_data):
        self.cfg = cfg
        self.data = ohlcv_data

        self.strats = StrategyLoader()
        self.strats.load(cfg["strategies"])

        self.risk = RiskManager(cfg["risk"])
        self.portfolio = PortfolioManager(cfg["portfolio"])

        self.execution = ExecutionModel(cfg["execution"])
        self.fees = CommissionModel(cfg["fees"])

        self.equity_curve = []
        self.trade_log = []

    def run(self):
        for bar in self.data:
            market = {
                "mid": bar["close"],
                "atr": bar.get("atr", 0.5),
                "vol": bar.get("vol", 0.01),
                "regime": bar.get("regime", "normal")
            }

            # 1. Strategy generates signals
            signals = self.strats.run_all(market)

            for sig in signals:
                order = self.risk.evaluate(sig, market, {"balance": self.portfolio.balance})

                if order:
                    order["symbol"] = self.cfg["symbol"]

                    # 2. Execution model fills order realistically
                    fill = self.execution.fill_order(order, bar)

                    # 3. Commission
                    fee = self.fees.calculate(fill)
                    fill["fee"] = fee

                    # 4. Portfolio updates
                    hedge_orders = self.portfolio.process_fill(fill, market)

                    # 5. Save trade
                    self.trade_log.append(fill)

                    # 6. Process hedges
                    for h in hedge_orders:
                        h["symbol"] = self.cfg["symbol"]
                        hedge_fill = self.execution.fill_order(h, bar)
                        fee = self.fees.calculate(hedge_fill)
                        hedge_fill["fee"] = fee
                        self.portfolio.process_fill(hedge_fill, market)
                        self.trade_log.append(hedge_fill)

            # 7. Equity tracking
            unreal = self.portfolio.metrics.unrealized_pnl
            equity = self.portfolio.balance + unreal
            self.equity_curve.append(equity)

        return {
            "equity": self.equity_curve,
            "trades": self.trade_log,
            "final_equity": self.equity_curve[-1] if self.equity_curve else None,
        }
