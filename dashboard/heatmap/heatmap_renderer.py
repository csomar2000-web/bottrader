import json

class HeatmapRenderer:
    def __init__(self, data):
        self.data = data

    def html(self):
        d = json.dumps(self.data.snapshot())
        return f"<html><body><h1>Risk Heatmap</h1><pre>{d}</pre></body></html>"

    def json(self):
        return self.data.snapshot()
