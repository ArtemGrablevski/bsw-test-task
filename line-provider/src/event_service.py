from datetime import datetime, timezone
from uuid import UUID

from exceptions import EventDoesNotExistException, EventAlreadyExistsException, InvalidEventDeadlineException
from models import Event, EventCreate, EventStatus


class EventService:

    def __init__(self) -> None:
        # For simplicity, we store events in memory. Don't use it in production code :)
        self.__events: dict[UUID, Event] = {}

    def get_event(self, event_id: UUID) -> Event:
        if event_id not in self.__events:
            raise EventDoesNotExistException()
        return self.__events[event_id]

    def get_events(self) -> list[Event]:
        return [
            e for e in self.__events.values() if datetime.now(timezone.utc) < e.deadline
        ]

    def create_event(self, event: EventCreate) -> None:
        if event.event_id in self.__events:
            raise EventAlreadyExistsException()
        if datetime.now(timezone.utc) > event.deadline:
            raise InvalidEventDeadlineException()
        self.__events[event.event_id] = Event(
            **event.model_dump(),
            status=EventStatus.NEW,
        )

    def update_event_status(self, event_id: UUID, event_status: EventStatus) -> None:
        if event_id not in self.__events:
            raise EventDoesNotExistException()
        self.__events[event_id].status = event_status
