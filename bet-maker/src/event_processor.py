from faststream import FastStream
from faststream.rabbit import RabbitBroker

from config import Settings
from db.repositories import EventRepository
from db.connection.session import get_async_engine, get_sessionmaker
from models.event import EventCreate, EventStatusChange
from services.event import EventService


config = Settings()

broker = RabbitBroker(
    f"amqp://{config.rabbitmq_user}:{config.rabbitmq_password}"
    f"@{config.rabbitmq_host}:{config.rabbitmq_port}/"
)

engine = get_async_engine(postgres_dsn=config.postgres_dsn)
sessionmaker = get_sessionmaker(engine=engine)

app = FastStream(broker)


@broker.subscriber(queue=config.rabbitmq_event_status_change_queue)
async def event_status_change_listener(event: EventStatusChange) -> None:
    async with sessionmaker() as session:
        event_service = EventService(
            session=session,
            event_repository=EventRepository(session)
        )
        await event_service.update_event_status(
            event_id=event.event_id,
            event_status=event.status,
        )


@broker.subscriber(queue=config.rabbitmq_new_event_queue)
async def new_event_listener(event: EventCreate) -> None:
    async with sessionmaker() as session:
        event_service = EventService(
            session=session,
            event_repository=EventRepository(session)
        )
        await event_service.create_event(
            event_id=event.event_id,
            event_status=event.current_status,
            coefficient=event.coefficient,
            deadline=event.deadline,
        )
