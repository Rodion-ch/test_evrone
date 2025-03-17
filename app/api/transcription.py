from typing import Union

from core.config import AppMode, settings
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from loguru import logger
from schemas.transcription import (
    TranscriptionAddedQueue,
    TranscriptionCreate,
    TranscriptionResponse,
    TranscriptionStatsResponse,
)
from services.common import (
    Saver,
    StatsService,
    get_saver,
    get_stats_service,
    get_transcription_service,
)
from services.transcription import BaseTranscriptionService

router = APIRouter()

@router.post("/transcribe/", response_model=Union[TranscriptionResponse, TranscriptionAddedQueue])
async def transcribe(
    file: UploadFile = File(...),
    saver: Saver = Depends(get_saver),
    transcribe_service: BaseTranscriptionService = Depends(get_transcription_service),
    stats_service: StatsService = Depends(get_stats_service),
):
    if settings.APP_MODE == AppMode.HTTP:
        transcribe_res: TranscriptionCreate  = await transcribe_service.process_file(file)
        await stats_service.update_stats(transcribe_res.processing_time, transcribe_res.audio_duration)
        resp = await saver.save(transcribe_res)
        return resp
    elif settings.APP_MODE == AppMode.QUEUE:
        await saver.save(file)
        return TranscriptionAddedQueue(message="File sent to Kafka queue for processing")


@router.get("/stats/", response_model=TranscriptionStatsResponse)
async def get_stats_endpoint(stats: StatsService = Depends(get_stats_service)):
    try:
        stats = await stats.get_stats()
        return TranscriptionStatsResponse(**stats)
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching stats")
