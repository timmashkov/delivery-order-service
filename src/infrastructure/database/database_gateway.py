from sqlalchemy import AsyncAdaptedQueuePool, Pool
from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)


class DatabaseGateway:
    def __init__(
        self,
        host: str,
        port: int,
        dialect: str,
        login: str,
        password: str,
        database: str,
        echo: bool,
        pool_class: Pool = AsyncAdaptedQueuePool,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: int = 30,
        pool_recycle: int = 3600,
    ) -> None:
        self.dialect = dialect
        self.login = login
        self.password = password
        self.host = host
        self.port = port
        self.echo = echo
        self.database = database
        self.pool_class = pool_class
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.pool_timeout = pool_timeout
        self.pool_recycle = pool_recycle

        self._engine = create_async_engine(
            url=self._db_url,
            echo=self.echo,
            **self.pool_config,
        )

        self._session = async_sessionmaker(bind=self._engine, expire_on_commit=False)

    @property
    def _db_url(self) -> str:
        return f"postgresql+{self.dialect}://{self.login}:{self.password}@{self.host}:{self.port}/{self.database}"

    @property
    def pool_config(self) -> dict:
        return {
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "pool_timeout": self.pool_timeout,
            "pool_recycle": self.pool_recycle,
            "poolclass": self.pool_class,
        }

    @property
    def session(self) -> async_sessionmaker[AsyncSession]:
        return self._session

    async def close(self) -> None:
        await self._engine.dispose()
