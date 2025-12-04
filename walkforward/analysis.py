import numpy as np
from backtesting.backtester import Backtester

class WalkForwardAnalysis:
    def __init__(self, cfg, data, windows=5):
        self.cfg = cfg
        self.data = data
        self.windows = windows

    def run(self):
        size = len(self.data) // self.windows
        out = []
        for i in range(self.windows):
            start = i * size
            end = start + size
            train = self.data[max(0, start-size):start]
            test = self.data[start:end]
            if len(train) == 0:
                continue
            bt = Backtester(self.cfg, train)
            bt.run()
            bt2 = Backtester(self.cfg, test)
            r = bt2.run()
            out.append(r[-1])
        return out
