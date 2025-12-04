class HedgingEngine:
    def __init__(self, cfg):
        self.cfg = cfg

    def evaluate(self, balance, exposure, market):
        out = []
        total_exp = sum(abs(v["long"] - v["short"]) for v in exposure.values())
        threshold = self.cfg.get("hedge_threshold", 0.3)

        if total_exp <= 0:
            return out

        risk_ratio = total_exp / balance
        if risk_ratio >= threshold:
            hedge_size = total_exp * self.cfg.get("hedge_size_mult", 1.0)
            out.append({
                "type": "open",
                "side": "short",
                "exchange": self.cfg.get("hedge_symbol", "BTC"),
                "size": hedge_size,
                "price": market["mid"]
            })
        return out
