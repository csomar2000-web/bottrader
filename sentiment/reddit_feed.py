import aiohttp
import time

class RedditFeed:
    def __init__(self, cfg):
        self.cfg = cfg
        self.url = "https://www.reddit.com/r/CryptoCurrency/new.json"
        self.last_ts = 0
        self.cooldown = cfg.get("cooldown", 2)

    async def fetch(self):
        now = time.time()
        if now - self.last_ts < self.cooldown:
            return []
        self.last_ts = now

        headers = {"User-Agent": "sentiment-bot"}
        async with aiohttp.ClientSession() as s:
            async with s.get(self.url, headers=headers) as r:
                d = await r.json()
                return [c["data"] for c in d["data"]["children"]]
