import tempfile
import time
from abc import ABC, abstractmethod
from pathlib import Path

from fastapi import UploadFile
from faster_whisper import WhisperModel
from schemas.transcription import TranscriptionCreate

model_path = str(Path(__file__).absolute().parent / "ml_model")

class BaseTranscriptionService(ABC):
    @abstractmethod
    async def process_file(self, file, *args, **kwargs):
        pass

class TranscriptionService(BaseTranscriptionService):
    def __init__(self):
        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8",
            download_root=model_path,
        )

    async def process_file(self, file: UploadFile) -> TranscriptionCreate:
        start_time = time.time()

        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
            segments, info = self.model.transcribe(temp_file_path)

        transcript = " ".join([segment.text for segment in segments])

        processing_time = time.time() - start_time

        return TranscriptionCreate(
            transcript=transcript,
            audio_duration=info.duration,
            processing_time=processing_time,
        )
