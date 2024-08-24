from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from api.dependencies.db import get_bet_service
from exceptions.event import EventDoesNotExistException, EventNotActiveException
from services.bet import BetService
from models.bet import BetCreate


router = APIRouter(
    tags=["Bets"], prefix="/api/bets"
)


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_bets(
    bet_service: BetService = Depends(get_bet_service),
):
    return await bet_service.get_bets()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_bet(
    bet: BetCreate,
    bet_service: BetService = Depends(get_bet_service),
):
    try:
        return await bet_service.create_bet(
            event_id=bet.event_id,
            bet_sum=bet.bet_sum,
        )
    except EventDoesNotExistException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with specified id does not exist",
        )
    except EventNotActiveException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event is not active anymore",
        )
