import sys, os
sys.path.insert(0, os.getcwd())

from strategies.strategy_loader import StrategyLoader

loader = StrategyLoader()

loader.load({
    "grid": {
        "module": "strategies.rule_based.grid_engine",
        "class": "GridStrategy",
        "params": {
            "upper": 105,
            "lower": 95,
            "step": 2
        }
    }
})

tick = {"mid": 100}

signals = loader.run_all(tick)
print("Signals:", signals)
