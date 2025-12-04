import numpy as np

class TrailingStop:
    def __init__(self, cfg):
        self.cfg = cfg
        self.entry = None
        self.side = None
        self.level = None

    def start(self, entry, side, atr):
        self.entry = entry
        self.side = side
        self.level = entry - atr * self.cfg["atr_mult"] if side == "long" else entry + atr * self.cfg["atr_mult"]

    def update(self, price, atr):
        if self.side == "long":
            new_level = price - atr * self.cfg["atr_mult"]
            if new_level > self.level:
                self.level = new_level
        else:
            new_level = price + atr * self.cfg["atr_mult"]
            if new_level < self.level:
                self.level = new_level
        return self.level

    def triggered(self, price):
        if self.side == "long":
            return price <= self.level
        return price >= self.level
