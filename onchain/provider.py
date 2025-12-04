import aiohttp

class ChainProvider:
    def __init__(self, cfg):
        self.url = cfg["rpc"]
        self.api = cfg["api"]

    async def get(self, endpoint, params=None):
        async with aiohttp.ClientSession() as s:
            async with s.get(self.api + endpoint, params=params) as r:
                return await r.json()

    async def balance(self, wallet):
        return await self.get("/balance", {"address": wallet})

    async def transfers(self, token):
        return await self.get("/transfers", {"token": token})
