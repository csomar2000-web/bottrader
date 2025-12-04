import sys, os
sys.path.insert(0, os.getcwd())

from execution.trade_manager import TradeManager

cfg = {
    "validator": {
        "min_size": 0.001,
        "max_spread": 5
    },
    "router": {
        "default_exchange": "binance"
    },
    "executor": {
        "slippage": 0.0
    }
}

exchanges = {
    "binance": {
        "name": "Binance Dummy Connection"
    }
}

tm = TradeManager(exchanges, cfg)

order = {
    "type": "open",
    "side": "long",
    "size": 1,
    "price": 100
}

market = {
    "mid": 100,
    "bid": 99.5,
    "ask": 100.5,
    "spread": 1
}

fill = tm.process(order, market)

print("Fill:", fill)
