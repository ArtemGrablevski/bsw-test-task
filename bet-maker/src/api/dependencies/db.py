from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from api.dependencies.stubs import get_sessionmaker
from db.repositories import BetRepository, EventRepository
from services.bet import BetService
from services.event import EventService


async def get_bet_service(
    sessionmaker: async_sessionmaker[AsyncSession] = Depends(get_sessionmaker),
):
    async with sessionmaker() as session:
        yield BetService(
            session=session,
            bet_repository=BetRepository(session),
            event_repository=EventRepository(session),
        )


async def get_event_service(
    sessionmaker: async_sessionmaker[AsyncSession] = Depends(get_sessionmaker),
):
    async with sessionmaker() as session:
        yield EventService(
            session=session,
            event_repository=EventRepository(session),
        )
