from typing import Dict, Any
from risk.position_sizer import PositionSizer
from risk.trailing_stop import TrailingStop

class RiskManager:
    def __init__(self, cfg):
        self.cfg = cfg
        self.sizer = PositionSizer(cfg["position_sizer"])
        self.stop = TrailingStop(cfg["trailing_stop"])
        self.state = {"position": None, "size": 0, "side": None}

    def evaluate(self, signal: Dict[str, Any], market: Dict[str, Any], portfolio: Dict[str, Any]):
        if signal is None:
            return None

        if self.state["position"] is None:
            size = self.sizer.size(
                balance=portfolio["balance"],
                volatility=market.get("vol", 0.01),
                confidence=signal.get("confidence", 0.5),
                regime=market.get("regime", "normal")
            )
            side = "long" if signal["action"] == "buy" else "short"
            self.state.update({"position": True, "side": side, "size": size})
            self.stop.start(market["mid"], side, market.get("atr", 0.001))
            return {
                "type": "open",
                "side": side,
                "size": size,
                "price": market["mid"]
            }

        price = market["mid"]
        atr = market.get("atr", 0.001)
        stop_level = self.stop.update(price, atr)

        if self.stop.triggered(price):
            result = {
                "type": "close",
                "side": self.state["side"],
                "size": self.state["size"],
                "price": price,
                "reason": "stop"
            }
            self.reset()
            return result

        if signal.get("action") == "sell" and self.state["side"] == "long":
            result = {
                "type": "close",
                "side": "long",
                "size": self.state["size"],
                "price": price,
                "reason": "reverse"
            }
            self.reset()
            return result

        if signal.get("action") == "buy" and self.state["side"] == "short":
            result = {
                "type": "close",
                "side": "short",
                "size": self.state["size"],
                "price": price,
                "reason": "reverse"
            }
            self.reset()
            return result

        return None

    def reset(self):
        self.state = {"position": None, "size": 0, "side": None}
