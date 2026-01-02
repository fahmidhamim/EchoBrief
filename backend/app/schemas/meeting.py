from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class AudioFileResponse(BaseModel):
    id: UUID
    meeting_id: UUID
    file_path: str
    file_size: Optional[int]
    duration_seconds: Optional[int]
    format: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class MeetingCreate(BaseModel):
    meeting_title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    max_participants: int = Field(default=20, ge=2, le=20)

class MeetingUpdate(BaseModel):
    meeting_title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[str] = None

class MeetingResponse(BaseModel):
    id: UUID
    host_id: UUID
    meeting_title: str
    description: Optional[str]
    status: str
    max_participants: int
    created_at: datetime
    started_at: Optional[datetime]
    ended_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class MeetingDetailResponse(MeetingResponse):
    participants_count: int = 0
    transcript_count: int = 0
    has_summary: bool = False
    audio_files: List[AudioFileResponse] = []

class JoinMeetingRequest(BaseModel):
    meeting_id: UUID

class ParticipantResponse(BaseModel):
    id: UUID
    user_id: UUID
    meeting_id: UUID
    joined_at: datetime
    left_at: Optional[datetime]
    duration_seconds: int
    
    class Config:
        from_attributes = True

class TranscriptResponse(BaseModel):
    id: UUID
    meeting_id: UUID
    speaker_name: Optional[str]
    transcript_text: str
    timestamp_seconds: Optional[int]
    confidence: float
    created_at: datetime
    
    class Config:
        from_attributes = True

class SummaryResponse(BaseModel):
    id: UUID
    meeting_id: UUID
    summary_text: str
    action_items: Optional[List[str]]
    keywords: Optional[List[str]]
    duration_seconds: Optional[int]
    word_count: Optional[int]
    generated_at: datetime
    
    class Config:
        from_attributes = True
