from dishka import Provider, Scope, provide

from application.settings import Settings
from application.server import APIServer
from infrastructure.broker.kafka import KafkaProducer
from infrastructure.database import OutboxPublisher, UnitOfWork
from presentation.routers import order_router, order_item_router


class ServerProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_api_server(self, settings: Settings, kafka_producer: KafkaProducer, outbox_publisher: OutboxPublisher) -> APIServer:
        """Создаёт экземпляр APIServer с инжектированными settings."""
        return APIServer(
            settings=settings,
            routers=[order_router, order_item_router],
            start_callbacks=[kafka_producer.connect, outbox_publisher.start],
            stop_callbacks=[kafka_producer.disconnect, outbox_publisher.stop]
        )

    @provide(scope=Scope.APP)
    def provide_outbox_publisher(
        self,
        unit_of_work: UnitOfWork,
        kafka_producer: KafkaProducer,
    ) -> OutboxPublisher:
        return OutboxPublisher(
            unit_of_work=unit_of_work,
            kafka_producer=kafka_producer,
        )
