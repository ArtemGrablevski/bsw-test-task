from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy.ext.asyncio import AsyncSession

from constants.enums import EventStatus
from db.repositories import BetRepository, EventRepository
from exceptions.event import EventDoesNotExistException, EventNotActiveException
from models.bet import BetOut


class BetService:

    def __init__(
        self,
        session: AsyncSession,
        bet_repository: BetRepository,
        event_repository: EventRepository
    ) -> None:
        self.session = session
        self.bet_repository = bet_repository
        self.event_repository = event_repository

    async def get_bets(self) -> list[BetOut]:
        bets = await self.bet_repository.get_bets()
        return [
            BetOut(**bet.__dict__) for bet in bets
        ]

    async def create_bet(self, event_id: UUID, bet_sum: float) -> BetOut:
        time_now = datetime.now(timezone.utc)
        event = await self.event_repository.get_event_by_id(
            event_id=event_id,
        )
        if event is None:
            raise EventDoesNotExistException()
        if event.current_status != EventStatus.NEW.value or event.deadline < time_now:
            raise EventNotActiveException()
        bet_id = uuid4()
        bet = await self.bet_repository.create_bet(
            bet_id=bet_id,
            event_id=event_id,
            bet_sum=bet_sum,
            created_at=time_now,
        )
        await self.session.commit()
        return bet
