import contextlib
from uuid import UUID

from fastapi import FastAPI, Depends, HTTPException
from faststream.rabbit import RabbitBroker, RabbitQueue
from starlette import status

from config import Settings
from exceptions import EventDoesNotExistException, EventAlreadyExistsException, InvalidEventDeadlineException
from event_service import EventService
from models import EventCreate, EventStatus, EventStatusChange, EventStatusUpdate, EventCreateMessage
from stubs import get_message_broker, get_event_service


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    message_broker = RabbitBroker(
        f"amqp://{config.rabbitmq_user}:{config.rabbitmq_password}"
        f"@{config.rabbitmq_host}:{config.rabbitmq_port}/"
    )
    event_service = EventService()
    app.dependency_overrides[get_message_broker] = lambda: message_broker
    app.dependency_overrides[get_event_service] = lambda: event_service
    await message_broker.connect()
    yield
    await message_broker.close()


config = Settings()


rabbitmq_new_event_queue = RabbitQueue(name=config.rabbitmq_new_event_queue)
rabbitmq_event_status_change_queue = RabbitQueue(name=config.rabbitmq_event_status_change_queue)


app = FastAPI(
    lifespan=lifespan,
    title="Line-provider API",
)


@app.get("/events/{event_id}", status_code=status.HTTP_200_OK)
async def get_event(
    event_id: UUID,
    event_service: EventService = Depends(get_event_service),
):
    try:
        return event_service.get_event(event_id=event_id)
    except EventDoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )


@app.get("/events", status_code=status.HTTP_200_OK)
async def get_events(
    event_service: EventService = Depends(get_event_service),
):
    return event_service.get_events()


@app.post("/events", status_code=status.HTTP_201_CREATED)
async def create_event(
    event: EventCreate,
    broker: RabbitBroker = Depends(get_message_broker),
    event_service: EventService = Depends(get_event_service),
):
    try:
        event_service.create_event(event)
    except EventAlreadyExistsException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Event already exists"
        )
    except InvalidEventDeadlineException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid event deadline"
        )

    await broker.publish(
        message=EventCreateMessage(
            event_id=event.event_id,
            coefficient=event.coefficient,
            deadline=event.deadline,
            current_status=EventStatus.NEW,
        ),
        queue=rabbitmq_new_event_queue,
    )

    return {"success": True}


@app.put("/events/{event_id}", status_code=status.HTTP_200_OK)
async def update_event_status(
    event_id: UUID,
    event_status: EventStatusUpdate,
    event_service: EventService = Depends(get_event_service),
    broker: RabbitBroker = Depends(get_message_broker),
):
    try:
        event_service.update_event_status(
            event_id=event_id,
            event_status=event_status,
        )
    except EventDoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event does not exist",
        )

    await broker.publish(
        message=EventStatusChange(
            event_id=event_id,
            status=event_status.status,
        ),
        queue=rabbitmq_event_status_change_queue,
    )

    return {"success": True}
