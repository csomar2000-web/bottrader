from strategies.base_strategy import Strategy

class SentimentStrategy(Strategy):
    def generate_signal(self, data):
        s = data.get("sent_score", 0)
        if s >= self.config.get("bullish", 0.6):
            return {"action": "buy", "confidence": s}
        if s <= self.config.get("bearish", -0.6):
            return {"action": "sell", "confidence": abs(s)}
        return None
