class OnChainTriggerEngine:
    def __init__(self, cfg, provider):
        self.cfg = cfg
        self.provider = provider
        self.handlers = []

    def add(self, fn):
        self.handlers.append(fn)

    async def check(self):
        for w in self.cfg["whales"]:
            b = await self.provider.balance(w)
            if b["usd"] > self.cfg["threshold"]:
                for h in self.handlers:
                    await h({"type": "whale_move", "wallet": w, "balance": b})

        for t in self.cfg["tokens"]:
            tr = await self.provider.transfers(t)
            if tr["count"] > self.cfg["transfer_threshold"]:
                for h in self.handlers:
                    await h({"type": "token_spike", "token": t, "transfers": tr})
