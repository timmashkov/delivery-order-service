from dishka import Provider, Scope, provide

from application.settings import Settings
from infrastructure.database import DatabaseGateway, UnitOfWork


class DatabaseProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_database(self, settings: Settings) -> DatabaseGateway:
        return DatabaseGateway(
            host=settings.database.host,
            port=settings.database.port,
            dialect=settings.database.dialect,
            login=settings.database.login,
            password=settings.database.password,
            database=settings.database.database,
            echo=settings.database.echo,
        )


class UnitOfWorkProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def provide_unit_of_work(self, database_gateway: DatabaseGateway) -> UnitOfWork:
        return UnitOfWork(database_gateway)
