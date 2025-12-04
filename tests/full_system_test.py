import sys, os
sys.path.insert(0, os.getcwd())

from datafeed.feed_manager import FeedManager
from strategies.strategy_loader import StrategyLoader
from risk.risk_manager import RiskManager
from execution.trade_manager import TradeManager
from portfolio.portfolio_manager import PortfolioManager


############################
# CONFIG
############################

strategy_cfg = {
    "grid": {
        "module": "strategies.rule_based.grid_engine",
        "class": "GridStrategy",
        "params": {"upper": 105, "lower": 95, "step": 2}
    }
}

risk_cfg = {
    "position_sizer": {"risk_per_trade": 0.01},
    "trailing_stop": {"atr_mult": 2}
}

execution_cfg = {
    "validator": {"min_size": 0.001, "max_spread": 5},
    "router": {"default_exchange": "binance"},
    "executor": {"slippage": 0.0}
}

portfolio_cfg = {
    "starting_balance": 10000
}


############################
# INITIALIZE
############################

loader = StrategyLoader()
loader.load(strategy_cfg)

risk = RiskManager(risk_cfg)
tm = TradeManager({"binance": {}}, execution_cfg)
pm = PortfolioManager(portfolio_cfg)


############################
# SIMULATED MARKET DATA
############################

tick = {
    "mid": 99,
    "high": 102,
    "low": 98,
    "bid": 98.5,
    "ask": 99.5,
    "spread": 1,
    "atr": 1.3
}




print("\n--- MARKET TICK RECEIVED ---")
print(tick)

# Strategy signal
signals = loader.run_all(tick)
print("\nSignals:", signals)

if not signals:
    print("No strategy signal.")
    exit()

signal = signals[0]

# Risk
decision = risk.evaluate(signal, tick, {"balance": pm.balance})
print("\nRisk Decision:", decision)

if not decision:
    print("Risk blocked trade.")
    exit()

# Execution
fill = tm.process(decision, tick)
print("\nExecution Fill:", fill)

# Portfolio
hedges = pm.process_fill(fill, tick)
print("\nPortfolio Updated")
print("Balance:", pm.balance)
print("Positions:", pm.positions)
print("Hedges:", hedges)

print("\n--- FULL PIPELINE COMPLETE ---\n")
