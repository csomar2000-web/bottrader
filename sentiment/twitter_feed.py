import aiohttp
import time

class TwitterFeed:
    def __init__(self, cfg):
        self.cfg = cfg
        self.token = cfg.get("bearer")
        self.url = "https://api.twitter.com/2/tweets/search/recent"
        self.last_ts = 0
        self.cooldown = cfg.get("cooldown", 1)

    async def fetch(self):
        now = time.time()
        if now - self.last_ts < self.cooldown:
            return []
        self.last_ts = now

        headers = {"Authorization": f"Bearer {self.token}"}
        params = {"query": "(bitcoin OR crypto OR ethereum)", "max_results": 20}

        async with aiohttp.ClientSession() as s:
            async with s.get(self.url, headers=headers, params=params) as r:
                d = await r.json()
                return d.get("data", [])
