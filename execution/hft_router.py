class HFTRouter:
    def __init__(self, feeds):
        self.feeds = feeds

    def best_tick(self):
        best = None
        best_val = -1e9
        for name, tick in self.feeds.items():
            liq = 1 / (tick["spread"] + 1e-9)
            if liq > best_val:
                best_val = liq
                best = tick
        return best
