from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, PositiveFloat, field_validator


class BaseBet(BaseModel):
    event_id: UUID
    bet_sum: PositiveFloat

    @field_validator("bet_sum")
    @classmethod
    def validate_bet_sum(cls, value):
        str_value = str(value)
        if "." in str_value:
            decimal_part = str_value.split(".")[1].rstrip("0")
            if len(decimal_part) > 2:
                raise ValueError("Sum of the bet must have no more than 2 decimal places")
        return value


class BetCreate(BaseBet):
    ...


class BetOut(BaseBet):
    bet_id: UUID
    created_at: datetime
