from typing import Callable, Iterable, Type
from uuid import UUID

from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models import _Base


class ReadRepository:

    def __init__(
            self,
            session: AsyncSession,
            model: type[_Base],
            query_modifier: Callable[[select], select] | None = None,
    ) -> None:
        self._session = session
        self._model = model
        self._query_modifier = query_modifier

    def _get_query(self) -> Type[select]:
        query = select(self._model)
        if self._query_modifier:
            query = self._query_modifier(query)
        return query

    @classmethod
    def __set_filter(cls, query: select, filters: Filter = None) -> select:
        if filters:
            query = filters.filter(query)
        return query

    async def get_object_by_uuid(self, uuid: UUID) -> _Base | None:
        query = self._get_query().where(self._model.uuid == uuid)
        query = await self._session.execute(query)
        return query.unique().scalar_one_or_none()

    async def get_all_objects(self, filters: Filter = None) -> Iterable[_Base] | Iterable:
        query = self._get_query()
        query = self.__set_filter(query, filters)
        query = await self._session.execute(query)
        return query.unique().scalars().all()
