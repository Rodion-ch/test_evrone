import asyncio

import asyncpg
from aiokafka import AIOKafkaProducer
from core.config import settings
from loguru import logger
from redis.asyncio import Redis


async def wait_for_postgres():
    max_retries = 30
    retry_interval = 2

    for _ in range(max_retries):
        try:
            conn = await asyncpg.connect(settings.DATABASE_URL.replace('postgresql+asyncpg://', 'postgresql://'))
            await conn.close()
            logger.success("Successfully connected to PostgreSQL")
            return
        except asyncpg.exceptions.CannotConnectNowError:
            logger.warning("Waiting for PostgreSQL...")
            await asyncio.sleep(retry_interval)

    raise Exception("Unable to connect to PostgreSQL")

async def wait_for_kafka():
    max_retries = 30
    retry_interval = 2

    for _ in range(max_retries):
        try:
            producer = AIOKafkaProducer(bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS)
            await producer.start()
            await producer.stop()
            logger.success("Successfully connected to Kafka")
            return
        except Exception as e:
            logger.warning(f"Waiting for Kafka... Error: {e}")
            await asyncio.sleep(retry_interval)

    raise Exception("Unable to connect to Kafka")

async def wait_for_redis():
    max_retries = 30
    retry_interval = 2

    for _ in range(max_retries):
        try:
            redis = Redis.from_url(settings.REDIS_URL)
            await redis.ping()
            await redis.close()
            logger.success("Successfully connected to Redis")
            return
        except Exception as e:
            logger.warning(f"Waiting for Redis... Error: {e}")
            await asyncio.sleep(retry_interval)

    raise Exception("Unable to connect to Redis")

async def wait_for_services():
    await asyncio.gather(
        wait_for_postgres(),
        wait_for_kafka(),
        wait_for_redis()
    )

if __name__ == "__main__":
    asyncio.run(wait_for_services())
