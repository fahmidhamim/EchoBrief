from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime

class AudioUploadResponse(BaseModel):
    id: UUID
    meeting_id: UUID
    file_path: str
    file_size: int
    duration_seconds: Optional[int]
    format: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class TranscriptionSegment(BaseModel):
    text: str
    start_time: float
    end_time: float
    confidence: float = Field(default=0.9, ge=0.0, le=1.0)
    speaker: Optional[str] = None

class TranscriptionRequest(BaseModel):
    meeting_id: UUID
    audio_file_path: str

class TranscriptionResponse(BaseModel):
    meeting_id: UUID
    full_text: str
    segments: list
    duration_seconds: int
    word_count: int
