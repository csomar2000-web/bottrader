from risk.position_sizer import PositionSizer
from risk.trailing_stop import TrailingStop

class RiskManager:
    def __init__(self, cfg):
        self.cfg = cfg
        self.sizer = PositionSizer(cfg["position_sizer"])
        self.stop = TrailingStop(cfg["trailing_stop"])

        self.state = {
            "active": False,
            "side": None,
            "size": 0,
        }

        self.daily_loss_limit = cfg.get("daily_loss_limit", 0.15)
        self.max_exposure = cfg.get("max_exposure", 0.3)
        self.max_consecutive_losses = cfg.get("max_consecutive_losses", 5)
        self.consecutive_losses = 0
        self.entry_price = None

    def evaluate(self, signal, market, portfolio):
        if signal is None:
            return None

        balance = portfolio["balance"]
        price = market["mid"]
        volatility = market.get("vol", 0.01)
        regime = market.get("regime", "normal")
        confidence = signal.get("confidence", 0.6)

        # ----- 1) DAILY STOP-OUT PROTECTION -----
        if portfolio.get("drawdown", 0) >= self.daily_loss_limit:
            return None

        # ----- 2) MAX EXPOSURE PROTECTION -----
        if self.state["active"]:
            exposure_value = self.state["size"] * price
            if exposure_value > balance * self.max_exposure:
                return {
                    "type": "close",
                    "side": self.state["side"],
                    "size": self.state["size"],
                    "price": price,
                    "reason": "exposure_limit"
                }

        # ----- 3) TRAILING STOP CHECK -----
        if self.state["active"]:
            if self.stop.triggered(price):
                action = {
                    "type": "close",
                    "side": self.state["side"],
                    "size": self.state["size"],
                    "price": price,
                    "reason": "stop"
                }
                self.reset()
                self.consecutive_losses += 1
                return action

        # ----- 4) OPEN NEW POSITION -----
        if not self.state["active"]:
            size = self.sizer.size(
                balance=balance,
                price=price,
                volatility=volatility,
                confidence=confidence,
                regime=regime
            )

            side = "long" if signal["action"] == "buy" else "short"

            self.state.update({
                "active": True,
                "side": side,
                "size": size
            })

            self.entry_price = price
            self.stop.start(price, side, market.get("atr", 0.002))

            return {
                "type": "open",
                "side": side,
                "size": size,
                "price": price
            }

        # ----- 5) REVERSAL (long → short or short → long) -----
        if signal["action"] == "sell" and self.state["side"] == "long":
            action = {
                "type": "close",
                "side": "long",
                "size": self.state["size"],
                "price": price,
                "reason": "reverse"
            }
            self.reset()
            return action

        if signal["action"] == "buy" and self.state["side"] == "short":
            action = {
                "type": "close",
                "side": "short",
                "size": self.state["size"],
                "price": price,
                "reason": "reverse"
            }
            self.reset()
            return action

        return None

    def reset(self):
        self.state = {
            "active": False,
            "side": None,
            "size": 0
        }
