from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models import Outbox


class OutboxRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._model = Outbox

    async def create_event(self, **kwargs) -> Outbox | None:
        query = insert(Outbox).values(**kwargs).returning(Outbox)
        query = await self._session.execute(query)
        return query.unique().scalar_one_or_none()
