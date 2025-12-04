import importlib
import os
from typing import Dict, Any, List
from core.logger import trading_logger

class StrategyLoader:
    def __init__(self, base_path: str = "strategies"):
        self.base_path = base_path
        self.active_strategies = {}

    def load_class(self, module_path: str, class_name: str):
        module = importlib.import_module(module_path)
        return getattr(module, class_name)

    def discover(self) -> List[str]:
        out = []
        for root, _, files in os.walk(self.base_path):
            for f in files:
                if f.endswith(".py") and not f.startswith("__"):
                    p = os.path.join(root, f).replace("/", ".").rstrip(".py")
                    out.append(p)
        return out

    def load(self, strategies_config: Dict[str, Any]):
        for strat_name, cfg in strategies_config.items():
            module_path = cfg["module"]
            class_name = cfg["class"]
            params = cfg.get("params", {})

            try:
                cls = self.load_class(module_path, class_name)
                instance = cls(strat_name, params)
                self.active_strategies[strat_name] = instance
                trading_logger.info(f"strategy_loaded:{strat_name}")
            except Exception as e:
                trading_logger.error(f"strategy_load_failed:{strat_name} | {e}")

    def unload(self, name: str):
        if name in self.active_strategies:
            del self.active_strategies[name]
            trading_logger.info(f"strategy_unloaded:{name}")

    def get(self, name: str):
        return self.active_strategies.get(name)

    def run_all(self, market_data: Dict[str, Any]):
        out = []
        for name, strat in self.active_strategies.items():
            try:
                signal = strat.run(market_data)
                if signal:
                    out.append(signal)
            except Exception as e:
                trading_logger.error(f"strategy_runtime_error:{name} | {e}")
        return out

    def enable(self, name: str):
        if name in self.active_strategies:
            self.active_strategies[name].enable()

    def disable(self, name: str):
        if name in self.active_strategies:
            self.active_strategies[name].disable()

    def list(self) -> List[str]:
        return list(self.active_strategies.keys())
