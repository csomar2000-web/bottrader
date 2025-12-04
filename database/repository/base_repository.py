from sqlalchemy.future import select

class BaseRepository:
    def __init__(self, session):
        self.session = session
        self.model = None

    async def add(self, obj):
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def get_all(self):
        q = await self.session.execute(select(self.model))
        return q.scalars().all()

    async def get_recent(self, limit=50):
        q = await self.session.execute(select(self.model).order_by(self.model.id.desc()).limit(limit))
        return q.scalars().all()

    async def filter(self, **kwargs):
        q = await self.session.execute(select(self.model).filter_by(**kwargs))
        return q.scalars().all()
