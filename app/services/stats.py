from datetime import datetime
from typing import Protocol


class StatsStorageService(Protocol):
    async def update_stats(self, processing_time: float, audio_duration: float) -> None:
        ...

    async def get_stats(self) -> dict:
        ...

class StatsService:
    def __init__(self, stats_storage: StatsStorageService):
        self.stats_storage = stats_storage

    async def update_stats(self, processing_time: float, audio_duration: float):
        await self.stats_storage.update_stats(processing_time, audio_duration)

    async def get_stats(self) -> dict:
        return await self.stats_storage.get_stats()

class RedisStats(StatsStorageService):
    def __init__(self, redis_client):
        self.redis = redis_client

    async def update_stats(self, processing_time: float, audio_duration: float):
        async with self.redis.pipeline(transaction=True) as pipe:
            await pipe.incr('total_calls')
            await pipe.incrbyfloat('total_processing_time', processing_time)
            await pipe.incrbyfloat('total_audio_duration', audio_duration)
            await pipe.set('last_updated', datetime.utcnow().timestamp())
            await pipe.execute()

    async def get_stats(self) -> dict:
        async with self.redis.pipeline(transaction=True) as pipe:
            total_calls, total_processing_time, total_audio_duration, last_updated = await (
                pipe
                .get('total_calls')
                .get('total_processing_time')
                .get('total_audio_duration')
                .get('last_updated')
                .execute())

        total_calls = int(total_calls or 0)
        total_processing_time = float(total_processing_time or 0)
        total_audio_duration = float(total_audio_duration or 0)

        if total_calls > 0:
            median_response_time = total_processing_time / total_calls
            median_audio_length = total_audio_duration / total_calls
        else:
            median_response_time = 0
            median_audio_length = 0
            last_updated=datetime.now()

        return {
            'call_count': total_calls,
            'median_response_time': median_response_time,
            'median_audio_length': median_audio_length,
            'last_updated': last_updated,
        }
