from dishka import Provider, Scope, provide

from application.config import Settings
from infrastructure.database import DatabaseGateway, UnitOfWork


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_database(self, settings: Settings) -> DatabaseGateway:
        return DatabaseGateway(
            host=settings.postgres_host,
            port=settings.postgres_port,
            dialect=settings.postgres_dialect,
            login=settings.postgres_login,
            password=settings.postgres_password,
            database=settings.postgres_database,
            echo=settings.postgres_echo,
        )


class UnitOfWorkProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_unit_of_work(self, database_gateway: DatabaseGateway) -> UnitOfWork:
        return UnitOfWork(database_gateway)
