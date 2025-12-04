from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import Database
from database.repository.trade_repo import TradeRepository

db = Database("sqlite+aiosqlite:///bot.db")
trades_router = APIRouter()

async def session():
    async for s in db.session():
        yield s

@trades_router.get("/")
async def get_trades(s: AsyncSession = Depends(session)):
    repo = TradeRepository(s)
    return await repo.get_recent(200)

@trades_router.get("/latest")
async def latest_trade(s: AsyncSession = Depends(session)):
    repo = TradeRepository(s)
    rows = await repo.get_recent(1)
    return rows[0] if rows else {}
