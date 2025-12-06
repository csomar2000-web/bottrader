import asyncio
import yaml
import sys
from pathlib import Path
from core.env import load_environment
from scripts.live_trading import LiveTradingBot

CONFIG_PATH = Path("config/settings.yaml")


async def main():
    load_environment()
    try:
        if not CONFIG_PATH.exists():
            print(f"Error: Config file not found at {CONFIG_PATH}")
            sys.exit(1)
        
        # Load configuration
        with open(CONFIG_PATH, "r") as f:
            cfg = yaml.safe_load(f)
        
        bot = LiveTradingBot(cfg)
        await bot.start()
    
    except yaml.YAMLError as e:
        print(f"Error parsing YAML config: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())