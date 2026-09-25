import asyncio
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
        topics: list[str] | None = None,
        logging_config: str | None = None,
    ) -> None:
        self.host = host
        self.port = port
        self.acks = acks
        self.transactional_id = transactional_id
        self.topics = topics if topics else []
        self.logging_config = logging_config.upper() if logging_config else logging.INFO
        self._response_queue = {}
        self.__producer: AIOKafkaProducer | None = None

    async def __aenter__(self) -> Self:
        await self.__producer.begin_transaction()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            await self.__producer.commit_transaction()
        else:
            await self.__producer.abort_transaction()
            logging.error(f"Ошибка в транзакции: {exc_val}, транзакция откатана")

    async def _init_logger(self) -> None:
        logging.basicConfig(level=self.logging_config)
        logging.info("Инициализация logger прошла успешно")

    async def connect(self) -> None:
        self.__producer = AIOKafkaProducer(
            bootstrap_servers=f"{self.host}:{self.port}",
            acks=self.acks,
            transactional_id=self.transactional_id,
        )
        await self._init_logger()
        await self.__producer.start()
        logging.info("Инициализация kafka прошла успешно")

    async def disconnect(self) -> None:
        await self.__producer.stop()
        logging.info("Отключение kafka прошла успешно")

    async def send_message(self, message: dict, topic: str) -> None:
        async with self:
            await self.__producer.send_and_wait(
            topic=topic,
            value=dumps(message),
        )
