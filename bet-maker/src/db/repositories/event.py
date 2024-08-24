from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import select, update, insert

from constants.enums import EventStatus
from db.repositories.base import BaseDbRepository
from db.models import Event


class EventRepository(BaseDbRepository):

    async def get_event_by_id(self, event_id: UUID) -> Event | None:
        return await self.session.scalar(
            select(Event)
            .where(Event.event_id == event_id)
        )

    async def get_events(self, event_status: EventStatus, time_until: datetime) -> Sequence[Event]:
        events = await self.session.scalars(
            select(Event)
            .where(Event.current_status == event_status)
            .where(Event.deadline > time_until)
        )
        return events.all()

    async def create_event(
        self,
        event_id: UUID,
        event_status: EventStatus,
        coefficient: float,
        deadline: datetime
    ) -> None:
        await self.session.execute(
            insert(Event)
            .values(
                event_id=event_id,
                current_status=event_status.value,
                coefficient=coefficient,
                deadline=deadline,
            )
        )

    async def update_event_status(self, event_id: UUID, event_status: EventStatus) -> None:
        await self.session.execute(
            update(Event)
            .where(Event.event_id == event_id)
            .values(current_status=event_status.value)
        )
