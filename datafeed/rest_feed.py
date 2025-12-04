import aiohttp
import time

class RestFeed:
    def __init__(self, base_url, symbol):
        self.base_url = base_url
        self.symbol = symbol
        self.session = None
        self.cache = {}
        self.last_call = 0
        self.cooldown = 0.2

    async def _ensure(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def get(self, endpoint, params=None):
        await self._ensure()
        now = time.time()
        if now - self.last_call < self.cooldown:
            await asyncio.sleep(self.cooldown)
        self.last_call = time.time()

        url = f"{self.base_url}/{endpoint}"
        async with self.session.get(url, params=params) as r:
            return await r.json()

    async def ohlcv(self, timeframe="1m", limit=200):
        key = (timeframe, limit)
        if key in self.cache:
            return self.cache[key]
        data = await self.get("ohlcv", {"symbol": self.symbol, "tf": timeframe, "limit": limit})
        self.cache[key] = data
        return data

    async def ticker(self):
        return await self.get("ticker", {"symbol": self.symbol})
