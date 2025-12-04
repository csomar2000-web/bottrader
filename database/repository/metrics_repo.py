from database.repository.base_repository import BaseRepository
from database.models.performance import Performance

class MetricsRepository(BaseRepository):
    def __init__(self, session):
        super().__init__(session)
        self.model = Performance

    async def log_performance(self, realized, unrealized, equity):
        m = Performance(realized=realized, unrealized=unrealized, equity=equity)
        return await self.add(m)
