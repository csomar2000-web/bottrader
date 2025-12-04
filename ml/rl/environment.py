import numpy as np

class TradingEnvironment:
    def __init__(self, price_data, cfg):
        self.data = price_data
        self.cfg = cfg
        self.i = 0
        self.position = 0
        self.entry = 0
        self.done = False

    def reset(self):
        self.i = 0
        self.position = 0
        self.entry = 0
        self.done = False
        return self._state()

    def _state(self):
        row = self.data[self.i]
        return np.array(row, dtype=float)

    def step(self, action):
        price = self.data[self.i][0]
        reward = 0

        if action == 1 and self.position == 0:
            self.position = 1
            self.entry = price
        elif action == 2 and self.position == 1:
            reward = price - self.entry
            self.position = 0

        self.i += 1
        if self.i >= len(self.data) - 1:
            self.done = True

        return self._state(), reward, self.done, {}
