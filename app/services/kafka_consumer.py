import asyncio
import io

from aiokafka import AIOKafkaConsumer
from core.config import settings
from fastapi import UploadFile
from loguru import logger
from services.common import get_stats_service
from services.saver import DB_Saver
from services.transcription import TranscriptionService


class KafkaConsumer:
    def __init__(self):
        self.consumer = None
        self.transcriber = TranscriptionService()
        self.saver = DB_Saver()

    async def start(self):
        self.stats = await get_stats_service()
        self.consumer = AIOKafkaConsumer(
            settings.KAFKA_TOPIC,
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
        )
        await self.consumer.start()
        logger.info(f"Kafka consumer started. Listening to topic: {settings.KAFKA_TOPIC}")

    async def consume(self):
        try:
            async for msg in self.consumer:
                logger.info(f"Received message from Kafka: {msg.topic}, {msg.partition}, {msg.offset}")
                await self.process_message(msg.value)
        finally:
            await self.consumer.stop()

    async def process_message(self, audio_data):
        try:
            audio_file = UploadFile(filename="audio.wav", file=io.BytesIO(audio_data))
            transcription = await self.transcriber.process_file(audio_file)
            await self.saver.save(transcription)
            await self.stats.update_stats(transcription.processing_time, transcription.audio_duration)

            logger.info("Transcription saved to database")
        except Exception as e:
            raise e
            logger.error(f"Error processing message: {str(e)}")

async def run_kafka_consumer():
    consumer = KafkaConsumer()
    await consumer.start()
    await consumer.consume()

if __name__ == "__main__":
    asyncio.run(run_kafka_consumer())
