import sys, os
sys.path.insert(0, os.getcwd())

from backtesting.data_loader import DataLoader
from backtesting.backtester import BacktesterV2

# Load CSV OHLCV
data = DataLoader("tests/data/btc_usdt.csv").load_csv()

cfg = {
    "symbol": "BTCUSDT",
    "portfolio": {"starting_balance": 10000},
    "risk": {
        "position_sizer": {"risk_per_trade": 0.01},
        "trailing_stop": {"atr_mult": 2},
        "max_exposure": 0.25
    },
    "execution": {"slippage": 0.0002},
    "fees": {"taker": 0.0004},
    "strategies": {
        "grid": {
            "module": "strategies.rule_based.grid_engine",
            "class": "GridStrategy",
            "params": {"upper": 105, "lower": 95, "step": 2}
        }
    }
}

bt = BacktesterV2(cfg, data)
results = bt.run()

print("Final equity:", results["final_equity"])
print("Trades:", len(results["trades"]))
print("Equity curve length:", len(results["equity"]))
