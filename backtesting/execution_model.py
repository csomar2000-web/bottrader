class ExecutionModel:
    def __init__(self, cfg):
        self.cfg = cfg
        self.slippage = cfg.get("slippage", 0.0002)  # 2 bps
        self.partial_fill = cfg.get("partial_fill", True)

    def fill_order(self, order, bar):
        """
        bar = {
            "timestamp": ...,
            "open": ...,
            "high": ...,
            "low": ...,
            "close": ...,
            "volume": ...
        }
        """

        # Market order
        price = bar["open"]

        slip = price * self.slippage
        if order["side"] == "buy":
            price = price + slip
        else:
            price = price - slip

        # Partial fills (optional)
        size = order["size"]
        max_liq = bar.get("volume", size)

        if self.partial_fill:
            size = min(size, max_liq)

        return {
            "timestamp": bar["timestamp"],
            "symbol": order["symbol"],
            "type": order["type"],
            "side": order["side"],
            "price": price,
            "size": size,
        }
