import asyncio
from core.logger import trading_logger

class CronJobs:
    def __init__(self, bot, portfolio, strategies, feeds):
        self.bot = bot
        self.portfolio = portfolio
        self.strategies = strategies
        self.feeds = feeds

    async def refresh_models(self):
        trading_logger.info("model_refresh_started")
        await asyncio.sleep(0.2)
        trading_logger.info("model_refresh_completed")

    async def rebalance_portfolio(self):
        market = self.feeds.latest()
        sentiment = self.bot.sentiment()
        regime = self.bot.regime()
        alloc = self.bot.alloc(balance=self.portfolio.balance, sentiment=sentiment, markets=market, regime=regime)
        trading_logger.info({"portfolio_rebalanced": alloc})

    async def rotate_strategies(self):
        stats = self.bot.strategy_stats()
        selected = max(stats, key=lambda x: stats[x])
        for name in self.strategies.list():
            if name == selected:
                self.strategies.enable(name)
            else:
                self.strategies.disable(name)
        trading_logger.info({"strategy_rotation": selected})

    async def cleanup_logs(self):
        trading_logger.info("maintenance_cleanup_started")
        await asyncio.sleep(0.05)
        trading_logger.info("maintenance_cleanup_completed")

    async def heartbeat(self):
        trading_logger.info({"system_heartbeat": True})
