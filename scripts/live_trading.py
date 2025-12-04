import asyncio
from core.logger import trading_logger
from strategies.strategy_loader import StrategyLoader
from datafeed.feed_manager import FeedManager
from risk.risk_manager import RiskManager
from execution.trade_manager import TradeManager
from portfolio.portfolio_manager import PortfolioManager
from sentiment.sentiment_manager import SentimentManager
from scheduler.task_scheduler import TaskScheduler
from database.db import Database
from database.repository.trade_repo import TradeRepository
from database.repository.metrics_repo import MetricsRepository
from notifications.telegram_notifier import TelegramNotifier
from notifications.discord_notifier import DiscordNotifier

class LiveTradingBot:
    def __init__(self, cfg):
        self.cfg = cfg

        self.db = Database(cfg["db"])
        self.ws_feeds = cfg["feeds"]["ws"]
        self.rest_feeds = cfg["feeds"]["rest"]
        self.feed_manager = FeedManager(self.ws_feeds, self.rest_feeds)

        self.strategy_loader = StrategyLoader()
        self.strategy_loader.load(cfg["strategies"])

        self.risk = RiskManager(cfg["risk"])
        self.execution = TradeManager(cfg["exchanges"], cfg["execution"])
        self.portfolio = PortfolioManager(cfg["portfolio"])

        self.sentiment_model = cfg["sentiment"]["model"]
        self.sentiment = SentimentManager(
            cfg["sentiment"],
            self.sentiment_model,
            cfg["sentiment"]["news"],
            cfg["sentiment"]["twitter"],
            cfg["sentiment"]["reddit"],
        )

        self.telegram = TelegramNotifier(cfg["notify"]["telegram"])
        self.discord = DiscordNotifier(cfg["notify"]["discord"])

        self.scheduler = TaskScheduler()

    async def on_tick(self, tick):
        sentiment = await self.sentiment.update()
        strategies = self.strategy_loader.run_all({**tick, **sentiment})
        for signal in strategies:
            decision = self.risk.evaluate(signal, tick, {"balance": self.portfolio.balance})
            if decision:
                fill = self.execution.process(decision, tick)
                hedge = self.portfolio.process_fill(fill, tick)
                await self.store_fill(fill)
                await self.send_alert(fill)
        equity = self.portfolio.metrics.equity(self.portfolio.balance)
        await self.store_metrics(equity)

    async def store_fill(self, fill):
        async for s in self.db.session():
            repo = TradeRepository(s)
            await repo.log_trade(
                symbol=fill["exchange"],
                side=fill["side"],
                size=fill["size"],
                entry=fill["price"],
                exit=fill["price"],
                pnl=0
            )

    async def store_metrics(self, equity):
        async for s in self.db.session():
            repo = MetricsRepository(s)
            await repo.log_performance(
                realized=self.portfolio.metrics.realized_pnl,
                unrealized=self.portfolio.metrics.unrealized_pnl,
                equity=equity
            )

    async def send_alert(self, fill):
        await self.telegram.alert_trade(fill)
        await self.discord.alert_trade(fill)

    async def start(self):
        await self.db.create_all()

        self.feed_manager.add_callback(self.on_tick)
        asyncio.create_task(self.feed_manager.start())

        await self.scheduler.start()
