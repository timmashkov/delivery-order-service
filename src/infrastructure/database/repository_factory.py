from typing import TypeVar, Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models._base import _Base
from infrastructure.database.repositories.common.read_repository import ReadRepository
from infrastructure.database.repositories.common.write_repository import WriteRepository


ModelT = TypeVar("ModelT", bound=_Base)
RepositoryT = TypeVar("RepositoryT", bound=object)


class RepositoryFactory:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def read_repository(
        self,
        model: type[ModelT],
        query_modifier: Callable[[select], select] | None = None,
    ) -> ReadRepository:
        return ReadRepository(
            session=self._session,
            model=model,
            query_modifier=query_modifier,
        )

    def write_repository(self, model: type[ModelT]) -> WriteRepository:
        return WriteRepository(session=self._session, model=model)

    def custom_repository(self, repository_type: type[RepositoryT]) -> RepositoryT:
        return repository_type(session=self._session)
