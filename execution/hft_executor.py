import time
import numpy as np

class HFTExecutor:
    def __init__(self, cfg):
        self.cfg = cfg

    def execute(self, tick, side, size):
        mid = tick["mid"]
        sp = tick["spread"]
        slip = self.cfg.get("slippage_mult", 0.1) * sp
        price = mid + slip if side == "buy" else mid - slip
        return {
            "side": side,
            "size": size,
            "price": price,
            "timestamp": time.time(),
            "exchange": tick.get("source", "HFT")
        }
