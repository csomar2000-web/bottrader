from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict


class FeedConfig(BaseModel):
    provider: str
    symbols: List[str]
    interval: str
    cache: bool = True


class StrategyConfig(BaseModel):
    name: str
    enabled: bool = True
    params: Dict[str, float] = {}


class RiskConfig(BaseModel):
    max_position_size: float
    max_leverage: float
    max_daily_loss_pct: float
    kill_switch: bool = True


class ExchangeCredentials(BaseModel):
    api_key: str = Field(..., description="Load from environment variable")
    api_secret: str = Field(...)


class ExchangeConfig(BaseModel):
    name: str
    credentials: ExchangeCredentials
    rate_limit: Optional[int]


class ExecutionConfig(BaseModel):
    mode: str  # live / paper / backtest
    slippage: float = 0.0
    order_retry: int = 3


class PortfolioConfig(BaseModel):
    rebalance_interval: str
    max_assets: int


class SentimentConfig(BaseModel):
    providers: List[str]
    enabled: bool = False


class NotificationConfig(BaseModel):
    telegram_chat_id: Optional[str]
    slack_webhook: Optional[str]


class Settings(BaseModel):
    feeds: FeedConfig
    strategies: List[StrategyConfig]
    risk: RiskConfig
    exchanges: List[ExchangeConfig]
    execution: ExecutionConfig
    portfolio: PortfolioConfig
    sentiment: SentimentConfig
    notifications: NotificationConfig
