import aiohttp
import time

class NewsScraper:
    def __init__(self, cfg):
        self.cfg = cfg
        self.key = cfg.get("api_key")
        self.url = cfg.get("endpoint")
        self.last_ts = 0
        self.cooldown = cfg.get("cooldown", 3)

    async def fetch(self):
        now = time.time()
        if now - self.last_ts < self.cooldown:
            return []
        self.last_ts = now

        params = {"q": "crypto", "apiKey": self.key, "pageSize": 20}
        async with aiohttp.ClientSession() as s:
            async with s.get(self.url, params=params) as r:
                d = await r.json()
                return d.get("articles", [])
