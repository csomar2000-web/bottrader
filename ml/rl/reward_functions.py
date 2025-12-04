import numpy as np

class RewardModel:
    def pnl(self, price, entry, pos):
        if pos == 0:
            return 0
        return price - entry

    def volatility_penalty(self, vol, weight=0.1):
        return -abs(vol) * weight

    def combined(self, pnl, vol):
        return pnl + self.volatility_penalty(vol)
