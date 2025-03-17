from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TranscriptionStats(Base):
    __tablename__ = "transcription_stats"

    id = Column(Integer, primary_key=True, index=True)
    call_count = Column(Integer, default=0)
    median_response_time = Column(Float)
    median_audio_length = Column(Float)
    last_updated = Column(DateTime)


class Transcription(Base):
    __tablename__ = "transcriptions"

    id = Column(Integer, primary_key=True, index=True)
    transcript = Column(String)
    audio_duration = Column(Float)
    processing_time = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
