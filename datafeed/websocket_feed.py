import asyncio
import json
import websockets
import time

class WebSocketFeed:
    def __init__(self, url, symbol, callbacks=None):
        self.url = url
        self.symbol = symbol
        self.callbacks = callbacks or []
        self.ws = None
        self.running = False
        self.last_msg = None
        self.latency = 0

    async def connect(self):
        while True:
            try:
                self.ws = await websockets.connect(self.url)
                return
            except:
                await asyncio.sleep(1)

    async def start(self):
        self.running = True
        await self.connect()
        await self.subscribe()

        while self.running:
            try:
                msg = await self.ws.recv()
                t = time.time()
                data = json.loads(msg)
                self.latency = time.time() - t
                self.last_msg = data
                for cb in self.callbacks:
                    await cb(data)
            except:
                await asyncio.sleep(0.5)
                await self.connect()
                await self.subscribe()

    async def subscribe(self):
        sub = json.dumps({"method": "subscribe", "params": {"symbol": self.symbol}})
        await self.ws.send(sub)

    def stop(self):
        self.running = False
