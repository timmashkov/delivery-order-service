from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any, Callable, TypeVar

from sqlalchemy import select

from infrastructure.database.repository_factory import RepositoryT
from infrastructure.database.unit_of_work import UnitOfWork
from infrastructure.database.repositories.common.read_repository import ReadRepository
from infrastructure.database.repositories.common.write_repository import WriteRepository
from infrastructure.database.models._base import _Base


RepositoryT = TypeVar("RepositoryT", bound=object)


class RepositoryMixin:
    _unit_of_work: UnitOfWork
    _model: type[_Base]
    _query_modifier: Callable[[select], select] | None = None
    _custom_repository: RepositoryT | None = None

    @asynccontextmanager
    async def read_repository(self) -> AsyncGenerator[ReadRepository, Any]:
        async with self._unit_of_work as uow:
            read_repository = uow.repositories.read_repository(model=self._model, query_modifier=self._query_modifier)
            yield read_repository

    @asynccontextmanager
    async def write_repository(self) -> AsyncGenerator[WriteRepository, Any]:
        async with self._unit_of_work as uow:
            write_repository = uow.repositories.write_repository(model=self._model)
            yield write_repository

    @asynccontextmanager
    async def custom_repository(self, ) -> AsyncGenerator[RepositoryT, Any]:
        async with self._unit_of_work as uow:
            custom_repository = uow.repositories.custom_repository(repository_type=self._custom_repository)
            yield custom_repository
