from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from uuid import UUID
from app.database import get_db
from app.services.meeting import MeetingService
from app.services.auth import AuthService
from app.schemas.meeting import MeetingCreate, MeetingResponse, MeetingDetailResponse, JoinMeetingRequest, TranscriptResponse
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extract user ID from JWT token"""
    try:
        token = credentials.credentials
        payload = AuthService.decode_token(token)
        if not payload:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        return user_id
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authorization error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")

@router.post("/create", response_model=MeetingResponse)
async def create_meeting(meeting_data: MeetingCreate, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """Create new meeting"""
    
    try:
        meeting = MeetingService.create_meeting(db, UUID(user_id), meeting_data)
        return MeetingResponse.from_orm(meeting)
    except Exception as e:
        logger.error(f"Create meeting error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create meeting")

@router.get("/{meeting_id}", response_model=MeetingDetailResponse)
async def get_meeting(meeting_id: UUID, db: Session = Depends(get_db)):
    """Get meeting details"""
    try:
        meeting = MeetingService.get_meeting(db, meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
        
        participants_count = len(meeting.participants)
        transcript_count = len(meeting.transcripts)
        has_summary = meeting.summary is not None
        
        response = MeetingDetailResponse.from_orm(meeting)
        response.participants_count = participants_count
        response.transcript_count = transcript_count
        response.has_summary = has_summary
        response.audio_files = list(meeting.audio_files) if hasattr(meeting, "audio_files") else []
        return response
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get meeting error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get meeting")

@router.get("/user/{user_id}", response_model=List[MeetingResponse])
async def get_user_meetings(user_id: UUID, db: Session = Depends(get_db)):
    """Get all meetings for a user"""
    try:
        meetings = MeetingService.get_user_meetings(db, user_id)
        return [MeetingResponse.from_orm(m) for m in meetings]
    except Exception as e:
        logger.error(f"Get user meetings error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get meetings")

@router.post("/join", response_model=dict)
async def join_meeting(request: JoinMeetingRequest, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """Join existing meeting"""
    
    try:
        participant = MeetingService.join_meeting(db, request.meeting_id, UUID(user_id))
        return {"status": "joined", "participant_id": str(participant.id)}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Join meeting error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to join meeting")

@router.post("/{meeting_id}/leave", response_model=dict)
async def leave_meeting(meeting_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """Leave meeting"""
    
    try:
        MeetingService.leave_meeting(db, meeting_id, UUID(user_id))
        return {"status": "left"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Leave meeting error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to leave meeting")

@router.post("/{meeting_id}/end", response_model=MeetingResponse)
async def end_meeting(meeting_id: UUID, db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """End meeting"""
    try:
        meeting = MeetingService.end_meeting(db, meeting_id)
        return MeetingResponse.from_orm(meeting)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"End meeting error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to end meeting")

@router.get("/{meeting_id}/transcripts", response_model=List[TranscriptResponse])
async def get_transcripts(meeting_id: UUID, db: Session = Depends(get_db)):
    """Get meeting transcripts"""
    try:
        transcripts = MeetingService.get_meeting_transcripts(db, meeting_id)
        return [TranscriptResponse.from_orm(t) for t in transcripts]
    except Exception as e:
        logger.error(f"Get transcripts error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get transcripts")
