from dishka import Provider, Scope, provide

# from infrastructure.database import OutboxRepository, UnitOfWork
#
#
# class RepositoryProvider(Provider):
#     @provide(scope=Scope.REQUEST)
#     def provide_repository(self, unit_of_work: UnitOfWork) -> OutboxRepository:
#         return OutboxRepository(unit_of_work._session)
