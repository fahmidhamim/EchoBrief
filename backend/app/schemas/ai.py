from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID
from datetime import datetime

class SummarizeRequest(BaseModel):
    meeting_id: UUID
    transcript_text: Optional[str] = None
    max_length: int = Field(default=500, ge=100, le=2000)

class SummarizeResponse(BaseModel):
    meeting_id: UUID
    summary_text: str
    action_items: List[str]
    keywords: List[str]
    duration_seconds: Optional[int]
    word_count: Optional[int] = None
    generated_at: datetime
    
    class Config:
        from_attributes = True

class AIMetricsResponse(BaseModel):
    total_meetings_summarized: int
    total_transcripts_processed: int
    average_summary_length: float
    average_action_items_per_meeting: float
