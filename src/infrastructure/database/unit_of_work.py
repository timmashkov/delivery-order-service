from types import TracebackType
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.database_gateway import DatabaseGateway
from infrastructure.database.repository_factory import RepositoryFactory


class UnitOfWork:
    def __init__(self, database_gateway: DatabaseGateway) -> None:
        self._session_factory = database_gateway.session
        self._session: AsyncSession | None = None
        self.repositories: RepositoryFactory | None = None

    async def __aenter__(self) -> Self:
        self._session = self._session_factory()

        self.repositories = RepositoryFactory(session=self._session)

        return self

    async def __aexit__(self, exc_type: type[BaseException], exc_value: BaseException, traceback: TracebackType) -> None:
        try:
            if exc_type:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self._session.close()

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
