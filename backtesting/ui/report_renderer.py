import json

class ReportRenderer:
    def __init__(self, data):
        self.data = data

    def json(self):
        return json.dumps(self.data.snapshot())

    def html(self):
        d = self.data.snapshot()
        eq = ",".join(str(x) for x in d["equity"])
        t = json.dumps(d["trades"])
        m = json.dumps(d["metrics"])
        return f"<html><body><h1>Backtest Report</h1><div id='equity'>{eq}</div><div id='trades'>{t}</div><div id='metrics'>{m}</div></body></html>"
