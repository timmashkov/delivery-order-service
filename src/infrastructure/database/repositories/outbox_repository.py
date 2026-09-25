from datetime import datetime
from typing import Iterable
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from domain import EventStatusEnum
from infrastructure.database.models import Outbox


class OutboxRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._model = Outbox

    async def get_pending_events(self, events_quant: int) -> Iterable[Outbox]:
        query = (
            select(self._model)
            .where(
                self._model.status == EventStatusEnum.CREATED,
            )
            .limit(events_quant)
            .order_by(self._model.created_at)
            .with_for_update(skip_locked=True)
        )

        result = await self._session.execute(query)

        return result.scalars().all()

    async def update_event_status(self, event: Outbox, event_status: EventStatusEnum) -> None:
        query = update(self._model).where(self._model.uuid == event.uuid).values(status=event_status, sent_at=datetime.now())
        await self._session.execute(query)

    async def create_event(self, **kwargs) -> Outbox | None:
        query = insert(self._model).values(**kwargs).returning(self._model)
        result = await self._session.execute(query)
        return result.unique().scalar_one_or_none()