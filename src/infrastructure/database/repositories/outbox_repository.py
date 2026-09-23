from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models import Outbox


class OutboxRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._model = Outbox

    async def select_event(self, event_uuid: UUID) -> Outbox | None:
        query = select(Outbox).where(Outbox.uuid == event_uuid)
        query = await self._session.execute(query)
        return query.unique().scalar_one_or_none()

    async def create_event(self, **kwargs) -> Outbox | None:
        query = insert(Outbox).values(**kwargs).returning(Outbox)
        query = await self._session.execute(query)
        return query.unique().scalar_one_or_none()

    async def update_event(self,event_uuid: UUID, **kwargs) -> Outbox | None:
        query = update(Outbox).values(**kwargs).where(Outbox.uuid == event_uuid).returning(Outbox)
        query = await self._session.execute(query)
        return query.unique().scalar_one_or_none()
