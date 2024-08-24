import datetime
import uuid

from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID, NUMERIC

from db.models import Base


class Event(Base):

    __tablename__ = "events"

    event_id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, index=True,
    )
    deadline: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True)
    )
    coefficient: Mapped[float] = mapped_column(
        NUMERIC(20, 2)
    )
    current_status: Mapped[str]  # TODO: вынести статусы в отдельную таблицу
