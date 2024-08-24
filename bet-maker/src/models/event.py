from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from constants.enums import EventStatus


class BaseEvent(BaseModel):
    event_id: UUID
    deadline: datetime
    coefficient: float
    current_status: EventStatus


class EventOut(BaseEvent):
    ...


class EventCreate(BaseEvent):
    ...


class EventStatusChange(BaseModel):
    event_id: UUID
    status: EventStatus
