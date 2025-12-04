from database.repository.base_repository import BaseRepository
from database.models.trade import Trade

class TradeRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.model = Trade

    async def log_trade(self, symbol, side, size, entry, exit, pnl):
        t = Trade(symbol=symbol, side=side, size=size, entry=entry, exit=exit, pnl=pnl)
        return await self.add(t)
