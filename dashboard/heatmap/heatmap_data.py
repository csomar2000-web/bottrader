class HeatmapData:
    def __init__(self):
        self.grid = {}

    def update(self, asset, regime, risk):
        if asset not in self.grid:
            self.grid[asset] = {}
        self.grid[asset][regime] = risk

    def snapshot(self):
        return self.grid
