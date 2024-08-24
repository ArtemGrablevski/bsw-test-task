import datetime
import uuid

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID, NUMERIC

from db.models import Base


class Bet(Base):

    __tablename__ = "bets"

    bet_id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, index=True,
    )
    event_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("events.event_id", ondelete="cascade"),
    )
    bet_sum: Mapped[float] = mapped_column(
        NUMERIC(20, 2)
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True)
    )
