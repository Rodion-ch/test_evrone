
from aiokafka import AIOKafkaProducer
from core.config import AppMode, settings
from db.models import Transcription
from db.session import get_db
from fastapi import UploadFile
from loguru import logger
from schemas.transcription import TranscriptionAddedQueue, TranscriptionCreate, TranscriptionResponse


class DB_Saver:
    async def save(self, transcription: TranscriptionCreate) -> None:
        async for session in get_db():
            db_transcription = Transcription(
                transcript=transcription.transcript,
                audio_duration=transcription.audio_duration,
                processing_time=transcription.processing_time,
            )
            session.add(db_transcription)
            await session.commit()
            await session.refresh(db_transcription)
            return TranscriptionResponse(id=db_transcription.id, created_at=db_transcription.created_at, **transcription.dict())


class Kafka_Saver:
    def __init__(self, *args, **kwargs):
        self.producer = None
        logger.info("Kafka saver initialized")

    async def start(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
        await self.producer.start()
        logger.info("Kafka producer started")

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            logger.info("Kafka producer stopped")

    async def save(self, file: UploadFile) -> dict:
        if not self.producer:
            await self.start()

        data = await file.read()
        await self.producer.send_and_wait(settings.KAFKA_TOPIC, data)
        
        logger.info(f"Transcription sent to Kafka topic: {settings.KAFKA_TOPIC}")
        return TranscriptionAddedQueue(message="Transcription sent to Kafka queue for processing")


class Saver:
    def __init__(self):
        if settings.APP_MODE == AppMode.QUEUE:
            self.saver = Kafka_Saver()
        else:
            self.saver = DB_Saver()
    async def save(self, transcription: TranscriptionCreate) -> dict:
        return await self.saver.save(transcription)

    async def start(self):
        if isinstance(self.saver, Kafka_Saver):
            await self.saver.start()

    async def stop(self):
        if isinstance(self.saver, Kafka_Saver):
            await self.saver.stop()


