import asyncio
import logging
from typing import Iterable

from domain import EventStatusEnum
from infrastructure.broker import KafkaProducer
from infrastructure.database import UnitOfWork, OutboxRepository
from infrastructure.database.models import Outbox


class OutboxPublisher:
    _task_name: str = "outbox-publisher"

    def __init__(
        self,
        unit_of_work: UnitOfWork,
        kafka_producer: KafkaProducer,
        batch_size: int = 100,
        poll_interval: float = 1.0,
    ) -> None:
        self._unit_of_work = unit_of_work
        self._kafka_producer = kafka_producer
        self._batch_size = batch_size
        self._poll_interval = poll_interval

        self._running = False
        self._task: asyncio.Task | None = None

    async def start(self) -> None:
        if self._running:
            return

        self._running = True
        self._task = asyncio.create_task(
            self._run(),
            name=self._task_name,
        )

        logging.info("Outbox publisher запущен")

    async def stop(self) -> None:
        if not self._running:
            return

        self._running = False

        if self._task is not None:
            self._task.cancel()

            try:
                await self._task
            except asyncio.CancelledError:
                pass

            self._task = None

        logging.info("Outbox publisher остановлен")

    async def _run(self) -> None:
        while self._running:
            try:
                processed = await self._process_batch()

                if processed == 0:
                    await asyncio.sleep(self._poll_interval)

            except asyncio.CancelledError:
                raise

            except Exception:
                logging.exception("Ошибка в Outbox publisher")
                await asyncio.sleep(self._poll_interval)

    async def _publish_events(self, events: Iterable[Outbox]) -> None:
        for event in events:
            await self._kafka_producer.send_message(
                    message=event.as_dict(),
                    topic=event.event_type,
            )
        else:
            await self._mark_event_as_sent(events)

    async def _process_batch(self) -> int:
        async with self._unit_of_work as unit_of_work:
            repository = unit_of_work.repositories.custom_repository(OutboxRepository)
            events = await repository.get_pending_events(events_quant=self._batch_size)

            if not events:
                return 0

        await self._publish_events(events)

        return len(events)

    async def _mark_event_as_sent(self, events: Iterable[Outbox]) -> None:
        async with self._unit_of_work as unit_of_work:
            repository = unit_of_work.repositories.custom_repository(OutboxRepository)
            await asyncio.gather(*[repository.update_event_status(event, EventStatusEnum.SENT) for event in events])


    # async def _mark_event_for_retry(
    #     self,
    #     event: Outbox,
    # ) -> None:
    #     async with self._session_factory() as session:
    #         repository = OutboxRepository(session)
    #
    #         db_event = await session.get(
    #             Outbox,
    #             event.uuid,
    #         )
    #
    #         if db_event is None:
    #             logging.error(
    #                 "Outbox event %s не найден",
    #                 event.uuid,
    #             )
    #             return
    #
    #         await repository.mark_created(db_event)
    #
    #         await session.commit()
    #
    #         logging.info(
    #             "Outbox event %s возвращён в CREATED",
    #             event.uuid,
    #         )