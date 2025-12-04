import aiohttp
import asyncio

class TelegramNotifier:
    def __init__(self, cfg):
        self.token = cfg["token"]
        self.chat_id = cfg["chat_id"]
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        self.cooldown = cfg.get("cooldown", 0.5)
        self.last_ts = 0

    async def send(self, msg):
        now = asyncio.get_event_loop().time()
        if now - self.last_ts < self.cooldown:
            await asyncio.sleep(self.cooldown)
        self.last_ts = now

        payload = {"chat_id": self.chat_id, "text": msg}
        async with aiohttp.ClientSession() as s:
            await s.post(self.url, json=payload)

    async def alert_trade(self, trade):
        text = f"Trade: {trade['side']} | Size: {trade['size']} | Price: {trade['price']}"
        await self.send(text)

    async def alert_signal(self, signal):
        text = f"Signal: {signal['action']} | Conf: {signal.get('confidence', 0)}"
        await self.send(text)

    async def alert_error(self, error):
        text = f"Error: {error}"
        await self.send(text)

    async def heartbeat(self):
        await self.send("System heartbeat OK")
