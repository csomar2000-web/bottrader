class AssetAllocator:
    def __init__(self, cfg):
        self.cfg = cfg

    def allocate(self, balance, markets, sentiment, regime):
        weights = {}

        for sym, m in markets.items():
            base = self.cfg.get("base_weight", 0.1)
            sent = sentiment.get(sym, 0)
            reg_mult = self._regime_mult(regime)
            adj = base * (1 + sent) * reg_mult
            weights[sym] = max(0, adj)

        total = sum(weights.values()) + 1e-12
        for sym in weights:
            weights[sym] /= total

        alloc = {sym: balance * w for sym, w in weights.items()}
        return alloc

    def _regime_mult(self, regime):
        if regime == "high_volatility":
            return 0.7
        if regime == "low_volatility":
            return 1.3
        if regime == "trend":
            return 1.5
        return 1.0
