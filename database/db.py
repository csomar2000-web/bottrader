from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

class Database:
    def __init__(self, url):
        self.engine = create_async_engine(url, echo=False, future=True)
        self.Session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def session(self):
        async with self.Session() as s:
            yield s
