from dishka import Provider, Scope, provide

from infrastructure.broker.kafka import KafkaProducer
from infrastructure.database import UnitOfWork, OutboxRepository
from application.use_cases import OrderUseCase, OrderItemUseCase


class UseCaseProvider(Provider):

    @provide(scope=Scope.REQUEST)
    def provide_order_use_cases(self, unit_of_work: UnitOfWork) -> OrderUseCase:
        return OrderUseCase(unit_of_work)

    @provide(scope=Scope.REQUEST)
    def provide_order_item_use_cases(self, unit_of_work: UnitOfWork) -> OrderItemUseCase:
        return OrderItemUseCase(unit_of_work)
