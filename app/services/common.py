from typing import Any, Awaitable, Callable, Dict

from core.config import settings
from redis.asyncio import Redis
from services.saver import Saver
from services.stats import RedisStats, StatsService
from services.transcription import TranscriptionService

transcription_service = TranscriptionService()
saver = Saver()
redis_client = Redis.from_url(settings.REDIS_URL)
stats_service = RedisStats(redis_client)

service_getters: Dict[str, Callable[[], Awaitable[Any]]] = {}

async def get_transcription_service() -> TranscriptionService:
    return transcription_service

async def get_saver() -> Saver:
    return saver

async def get_redis_client() -> Redis:
    return redis_client

async def get_stats_service() -> StatsService:
    return stats_service

async def initialize_services():
    pass

async def close_connections():
    await redis_client.close()
    
