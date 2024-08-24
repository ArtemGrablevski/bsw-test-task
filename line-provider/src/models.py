from datetime import datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, PositiveFloat, field_validator


class EventStatus(str, Enum):
    NEW = "new"
    FIRST_TEAM_WON = "first_team_won"
    SECOND_TEAM_WON = "second_team_won"


class EventCreate(BaseModel):
    event_id: UUID
    coefficient: PositiveFloat
    deadline: datetime

    @field_validator("coefficient")
    @classmethod
    def validate_coefficient(cls, value):
        str_value = str(value)
        if "." in str_value:
            decimal_part = str_value.split(".")[1].rstrip("0")
            if len(decimal_part) > 2:
                raise ValueError("Coefficient must have no more than 2 decimal places")
        return value


class EventCreateMessage(EventCreate):  # sent to the rabbitmq queue
    current_status: EventStatus


class Event(BaseModel):
    event_id: UUID
    coefficient: Decimal
    deadline: datetime
    status: EventStatus


class EventStatusChange(BaseModel):
    event_id: UUID
    status: EventStatus


class EventStatusUpdate(BaseModel):  # for validation PUT /api/events
    status: EventStatus
