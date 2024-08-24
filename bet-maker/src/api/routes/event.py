from fastapi import APIRouter, Depends
from starlette import status

from api.dependencies.db import get_event_service
from services.event import EventService


router = APIRouter(
    tags=["Events"], prefix="/api/events"
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_active_events(
    event_service: EventService = Depends(get_event_service),
):
    return await event_service.get_active_events()
