from sqlalchemy.ext.asyncio import AsyncSession


class BaseDbRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
