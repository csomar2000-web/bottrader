import asyncio

class FeedManager:
    def __init__(self, ws_feeds, rest_feeds):
        self.ws_feeds = ws_feeds or {}
        self.rest_feeds = rest_feeds or {}
        self.callbacks = []
        self.running = False

    def add_callback(self, fn):
        self.callbacks.append(fn)

    async def emit(self, tick):
        for cb in self.callbacks:
            await cb(tick)

    async def start(self):
        self.running = True
        while self.running:
            tick = {"mid": 20000, "spread": 5, "source": "mock"}
            await self.emit(tick)
            await asyncio.sleep(1)

    def stop(self):
        self.running = False
