import aiohttp
import asyncio

class DiscordNotifier:
    def __init__(self, cfg):
        self.webhook = cfg["webhook"]
        self.cooldown = cfg.get("cooldown", 0.5)
        self.last_ts = 0

    async def send(self, msg):
        now = asyncio.get_event_loop().time()
        if now - self.last_ts < self.cooldown:
            await asyncio.sleep(self.cooldown)
        self.last_ts = now

        payload = {"content": msg}
        async with aiohttp.ClientSession() as s:
            await s.post(self.webhook, json=payload)

    async def alert_trade(self, trade):
        text = f"**TRADE EXECUTED**\nSide: {trade['side']}\nSize: {trade['size']}\nPrice: {trade['price']}"
        await self.send(text)

    async def alert_signal(self, signal):
        text = f"**SIGNAL**\nAction: {signal['action']}\nConfidence: {signal.get('confidence', 0)}"
        await self.send(text)

    async def alert_error(self, error):
        await self.send(f"**ERROR** {error}")

    async def heartbeat(self):
        await self.send("💠 Bot Heartbeat OK")
