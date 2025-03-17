from datetime import datetime

from pydantic import BaseModel


class TranscriptionBase(BaseModel):
    transcript: str
    audio_duration: float
    processing_time: float

class TranscriptionCreate(TranscriptionBase):
    pass

class TranscriptionResponse(TranscriptionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class TranscriptionAddedQueue(BaseModel):
    message: str

class TranscriptionStatsResponse(BaseModel):
    call_count: int
    median_response_time: float
    median_audio_length: float
    last_updated: datetime

    class Config:
        from_attributes = True
