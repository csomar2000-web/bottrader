import asyncio
import sys

from core.env import load_environment
from core.config import get_config
from core.log import setup_logging, get_logger
import core.errors  

from scripts.live_trading import LiveTradingBot


async def main():
    setup_logging()
    log = get_logger("main")

    load_environment()
    log.info("Environment loaded")

    try:
        cfg = get_config()
        log.info("Configuration loaded", context={"execution_mode": cfg.execution.mode})
    except Exception as e:
        log.error("Failed to load configuration", context={"error": str(e)})
        sys.exit(1)

    try:
        bot = LiveTradingBot(cfg)
        log.info("Starting live trading bot...")
        await bot.start()
    except Exception as e:
        log.error("Fatal error during bot startup", context={"error": str(e)})
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
