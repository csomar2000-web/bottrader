import sys, os, asyncio
sys.path.insert(0, os.getcwd())

from datafeed.feed_manager import FeedManager

async def fake_callback(tick):
    print("Tick received:", tick)

async def main():
    fm = FeedManager(ws_feeds={}, rest_feeds={})
    fm.add_callback(fake_callback)
    await fake_callback({"mid": 20000, "spread": 5, "source": "test"})

asyncio.run(main())
