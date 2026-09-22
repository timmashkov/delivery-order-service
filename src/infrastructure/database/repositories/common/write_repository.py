from typing import Iterable, Type, TypeVar, Any
from uuid import UUID

from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models import _Base


class WriteRepository:

    def __init__(self, session: AsyncSession, model: type[_Base]) -> None:
        self._session = session
        self._model = model

    async def _execute_query_and_get_result(self, query: Any) -> _Base | None:
        query = await self._session.execute(query)
        return query.unique().scalar_one_or_none()

    async def create_object(self, **kwargs) -> _Base | None:
        query = insert(self._model).values(**kwargs).returning(self._model)
        return await self._execute_query_and_get_result(query)

    async def update_object(self, **kwargs) -> _Base | None:
        query = (
                update(self._model)
                .where(self._model.uuid == kwargs.get("uuid"))
                .values(**kwargs)
                .returning(self._model)
        )
        return await self._execute_query_and_get_result(query)

    async def delete_object(self, uuid: UUID) -> _Base | None:
        query = (
                delete(self._model)
                .where(self._model.uuid == uuid)
                .returning(self._model)
        )
        return await self._execute_query_and_get_result(query)
