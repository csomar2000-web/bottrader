from strategies.ml.lstm_strategy import LSTMStrategy
from plugins.market.plugin_interface import StrategyPlugin

class Plugin(StrategyPlugin):
    def load(self):
        return {"min_conf": 0.4}

    def parameters(self):
        return {"min_conf": [0.1, 0.9]}

    def build(self):
        return LSTMStrategy("lstm_plugin", {"model": "models/lstm.pkl", "min_conf": 0.4})
