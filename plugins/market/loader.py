import importlib
import os

class MarketPluginLoader:
    def __init__(self, path="plugins/market"):
        self.path = path
        self.plugins = {}

    def discover(self):
        out = []
        for f in os.listdir(self.path):
            if f.endswith(".py") and not f.startswith("_"):
                name = f[:-3]
                out.append(name)
        return out

    def load(self):
        mods = self.discover()
        for m in mods:
            mod = importlib.import_module(f"plugins.market.{m}")
            cls = getattr(mod, "Plugin")
            self.plugins[m] = cls()

    def build_strategies(self):
        out = {}
        for name, p in self.plugins.items():
            out[name] = p.build()
        return out
