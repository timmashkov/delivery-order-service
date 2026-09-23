from dishka import Provider, Scope, provide

from application.settings import Settings
from infrastructure.broker.kafka import KafkaProducer


class KafkaProvider(Provider):
    @provide(scope=Scope.APP)
    def provide_kafka_producer(self, settings: Settings) -> KafkaProducer:
        return KafkaProducer(
            host=settings.kafka.bootstrap_servers.split(",")[0],
            acks=settings.kafka.acks,
            transactional_id=settings.kafka.transactional_id,
        )
