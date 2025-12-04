import sys, os
sys.path.insert(0, os.getcwd())

from risk.risk_manager import RiskManager

cfg = {
    "position_sizer": {
        "risk_per_trade": 0.01
    },
    "trailing_stop": {
        "atr_mult": 2
    }
}

risk = RiskManager(cfg)

signal = {
    "action": "buy",
    "strategy": "grid",
    "confidence": 0.8
}

market = {
    "mid": 100,
    "atr": 1.5
}

portfolio = {
    "balance": 10000
}

decision = risk.evaluate(signal, market, portfolio)

print("Decision:", decision)
