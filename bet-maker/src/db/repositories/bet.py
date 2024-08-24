from datetime import datetime
from typing import Sequence
from uuid import UUID

from sqlalchemy import insert, select

from db.repositories.base import BaseDbRepository
from db.models import Bet


class BetRepository(BaseDbRepository):

    async def get_bets(self, **filters) -> Sequence[Bet]:
        bets = await self.session.scalars(
            select(Bet)
            .filter_by(**filters)
        )
        return bets.all()

    async def create_bet(
        self,
        bet_id: UUID,
        event_id: UUID,
        bet_sum: int,
        created_at: datetime,
    ) -> Bet:
        return await self.session.scalar(
            insert(Bet)
            .values(
                bet_id=bet_id,
                event_id=event_id,
                bet_sum=bet_sum,
                created_at=created_at,
            )
            .returning(Bet)
        )
