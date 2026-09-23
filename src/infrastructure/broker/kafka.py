import logging
from asyncio import AbstractEventLoop, get_event_loop
from typing import Any, Self
from orjson import dumps

from aiokafka import AIOKafkaProducer


class KafkaProducer:
    def __init__(
        self,
        host: str,
        port: int,
        acks: str,
        transactional_id: Any,
        loop: AbstractEventLoop | None = None,
        topics: list[str] | None = None,
        logging_config: str | None = None,
    ) -> None:
        self.loop = loop if loop else get_event_loop()
        self.topics = topics if topics else []
        self.logging_config = logging_config.upper() if logging_config else logging.INFO
        self._response_queue = {}
        self.__producer = AIOKafkaProducer(
            bootstrap_servers=f"{host}:{port}",
            loop=self.loop,
            acks=acks,
            transactional_id=transactional_id,
        )

    async def __aenter__(self) -> Self:
        await self.__producer.begin_transaction()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            await self.__producer.commit_transaction()
            logging.info("Транзакция успешно зафиксирована")
        else:
            await self.__producer.abort_transaction()
            logging.error(f"Ошибка в транзакции: {exc_val}, транзакция откатана")

    async def _init_logger(self) -> None:
        logging.basicConfig(level=self.logging_config)
        logging.info("Инициализация logger прошла успешно")

    async def connect(self) -> None:
        await self._init_logger()
        await self.__producer.start()
        logging.info("Инициализация kafka прошла успешно")

    async def disconnect(self) -> None:
        await self._init_logger()
        await self.__producer.stop()
        logging.info("Отключение kafka прошла успешно")

    async def simple_send_message(self, message: dict, topic: str) -> None:
        await self._init_logger()
        await self.__producer.send_and_wait(
            topic=topic,
            value=dumps(message),
        )
        logging.info("Сообщение отправлено")

    async def transactional_send_message(self,  message: dict, topic: str) -> None:
        await self._init_logger()
        async with self:
            await self.simple_send_message(
                topic=topic,
                message=message,
            )
            logging.info("Сообщение отправлено и транзакция зафиксирована")
