from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.services.ai import AIService
from app.services.meeting import MeetingService
from app.schemas.ai import SummarizeRequest, SummarizeResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/summarize", response_model=SummarizeResponse)
async def summarize_meeting(
    request: SummarizeRequest,
    db: Session = Depends(get_db),
    user_id: str = None
):
    """Generate AI summary for meeting"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        # Get meeting
        meeting = MeetingService.get_meeting(db, request.meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
        
        # Get transcript if not provided
        if not request.transcript_text:
            transcripts = MeetingService.get_meeting_transcripts(db, request.meeting_id)
            request.transcript_text = " ".join([t.transcript_text for t in transcripts])
        
        if not request.transcript_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No transcript available for summarization"
            )
        
        # Generate summary
        summary_data = AIService.generate_summary(request.transcript_text, request.max_length)
        
        # Save summary
        summary = AIService.save_summary(db, request.meeting_id, summary_data)
        
        return SummarizeResponse.from_orm(summary)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Summarization error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Summarization failed")

@router.get("/summary/{meeting_id}", response_model=SummarizeResponse)
async def get_summary(meeting_id: UUID, db: Session = Depends(get_db)):
    """Get meeting summary"""
    try:
        summary = AIService.get_summary(db, meeting_id)
        if not summary:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found")
        
        return SummarizeResponse.from_orm(summary)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get summary error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get summary")
