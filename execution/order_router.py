import random

class OrderRouter:
    def __init__(self, exchanges, cfg):
        self.exchanges = exchanges
        self.cfg = cfg

    def select_exchange(self, order, market):
        scores = {}
        for name, ex in self.exchanges.items():
            liq = market.get(f"{name}_liq", 1)
            lat = market.get(f"{name}_latency", 1)
            score = liq - lat
            scores[name] = score
        return max(scores, key=scores.get)

    def route(self, order, market):
        ex = self.select_exchange(order, market)
        return ex, self.exchanges[ex]
