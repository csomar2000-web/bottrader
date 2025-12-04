class OrderValidator:
    def __init__(self, cfg):
        self.cfg = cfg

    def validate(self, order, market):
        if order["size"] <= 0:
            return False
        if market["spread"] > self.cfg.get("max_spread", 5):
            return False
        if order["side"] == "buy" and order["price"] >= market["ask"]:
            return True
        if order["side"] == "sell" and order["price"] <= market["bid"]:
            return True
        return False

    def sanitize(self, order, market):
        o = dict(order)
        if o["side"] == "buy":
            o["price"] = min(o["price"], market["ask"])
        else:
            o["price"] = max(o["price"], market["bid"])
        return o
