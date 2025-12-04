from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import Database
from database.repository.metrics_repo import MetricsRepository

db = Database("sqlite+aiosqlite:///bot.db")
metrics_router = APIRouter()

async def session():
    async for s in db.session():
        yield s

@metrics_router.get("/equity")
async def get_equity(s: AsyncSession = Depends(session)):
    repo = MetricsRepository(s)
    rows = await repo.get_recent(1)
    return rows[0] if rows else {}

@metrics_router.get("/history")
async def perf_history(s: AsyncSession = Depends(session)):
    repo = MetricsRepository(s)
    return await repo.get_recent(300)
