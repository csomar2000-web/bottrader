class TrailingStop:
    def __init__(self, cfg):
        self.cfg = cfg
        self.entry = None
        self.side = None
        self.level = None
        self.hard_stop = None

    def start(self, entry, side, atr):
        self.entry = entry
        self.side = side
        mult = self.cfg.get("atr_mult", 2.0)
        hard_mult = self.cfg.get("hard_stop_mult", 4.0)

        if side == "long":
            self.level = entry - atr * mult
            self.hard_stop = entry - atr * hard_mult
        else:
            self.level = entry + atr * mult
            self.hard_stop = entry + atr * hard_mult

    def update(self, price, atr):
        mult = self.cfg.get("atr_mult", 2.0)

        if self.side == "long":
            new_level = price - atr * mult
            if new_level > self.level:
                self.level = new_level
        else:
            new_level = price + atr * mult
            if new_level < self.level:
                self.level = new_level

    def triggered(self, price):
        if self.side == "long":
            return price <= self.level or price <= self.hard_stop
        return price >= self.level or price >= self.hard_stop
