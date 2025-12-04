import asyncio
from scripts.live_trading import LiveTradingBot
import json

async def main():
    with open("config/settings.json") as f:
        cfg = json.load(f)

    bot = LiveTradingBot(cfg)
    await bot.start()

if __name__ == "__main__":
    asyncio.run(main())
