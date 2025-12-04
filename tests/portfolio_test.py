import sys, os
sys.path.insert(0, os.getcwd())

from portfolio.portfolio_manager import PortfolioManager

# Portfolio configuration
cfg = {
    "starting_balance": 10000,
    "hedging": {
        "hedge_threshold": 0.3,    # trigger if exposure/balance exceeds 30%
        "hedge_size_mult": 1.0,
        "hedge_symbol": "BTCUSDT"
    }
}

pm = PortfolioManager(cfg)

# Initial market snapshot
market = {"mid": 100}

#########################################
# 1️⃣ Open a long position
#########################################

fill_open = {
    "type": "open",
    "symbol": "BTCUSDT",
    "side": "long",
    "price": 100,
    "size": 1,
    "exchange": "binance"
}

hedges = pm.process_fill(fill_open, market)

print("\n--- AFTER OPEN ---")
print("Balance:", pm.balance)
print("Positions:", pm.positions)
print("Exposure:", pm.exposure())
print("Realized/Unrealized:", pm.metrics.stats())
print("Hedge Orders:", hedges)


#########################################
# 2️⃣ Update market to new price
#########################################

market = {"mid": 105}
pm.update_unrealized(market)

print("\n--- AFTER PRICE MOVE TO 105 ---")
print("Unrealized PnL:", pm.metrics.unrealized_pnl)
print("Exposure:", pm.exposure())


#########################################
# 3️⃣ Close the position (realize profit)
#########################################

fill_close = {
    "type": "close",
    "symbol": "BTCUSDT",
    "side": "long",
    "price": 105,
    "size": 1,
    "exchange": "binance"
}

hedges = pm.process_fill(fill_close, market)

print("\n--- AFTER CLOSE ---")
print("Balance:", pm.balance)
print("Positions:", pm.positions)
print("Realized/Unrealized:", pm.metrics.stats())
print("Hedge Orders:", hedges)
