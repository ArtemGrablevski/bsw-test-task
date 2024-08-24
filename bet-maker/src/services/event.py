from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from constants.enums import EventStatus
from db.repositories import EventRepository
from models.event import EventOut


class EventService:

    def __init__(
        self,
        session: AsyncSession,
        event_repository: EventRepository,
    ) -> None:
        self.session = session
        self.event_repository = event_repository

    async def get_active_events(self) -> list[EventOut]:
        time_now = datetime.now(timezone.utc)
        events = await self.event_repository.get_events(
            event_status=EventStatus.NEW.value,
            time_until=time_now,
        )
        return [
            EventOut(**event.__dict__) for event in events
        ]

    async def update_event_status(self, event_id: UUID, event_status: EventStatus) -> None:
        await self.event_repository.update_event_status(
            event_id=event_id,
            event_status=event_status,
        )
        await self.session.commit()

    async def create_event(
        self,
        event_id: UUID,
        event_status: EventStatus,
        coefficient: float,
        deadline: datetime
    ) -> None:
        await self.event_repository.create_event(
            event_id=event_id,
            event_status=event_status,
            coefficient=coefficient,
            deadline=deadline,
        )
        await self.session.commit()
