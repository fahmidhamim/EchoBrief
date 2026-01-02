from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.meeting import Meeting
from app.models.transcript import Participant, Transcript
from app.models.summary import Summary
from app.schemas.meeting import MeetingCreate, MeetingUpdate
from typing import List, Optional
from uuid import UUID
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MeetingService:
    @staticmethod
    def create_meeting(db: Session, host_id: UUID, meeting_data: MeetingCreate) -> Meeting:
        """Create new meeting"""
        meeting = Meeting(
            host_id=host_id,
            meeting_title=meeting_data.meeting_title,
            description=meeting_data.description,
            max_participants=meeting_data.max_participants,
            status="scheduled"
        )
        db.add(meeting)
        db.commit()
        db.refresh(meeting)
        logger.info(f"Meeting created: {meeting.id}")
        return meeting
    
    @staticmethod
    def get_meeting(db: Session, meeting_id: UUID) -> Optional[Meeting]:
        """Get meeting by ID"""
        return db.query(Meeting).filter(Meeting.id == meeting_id).first()
    
    @staticmethod
    def get_user_meetings(db: Session, user_id: UUID, limit: int = 50) -> List[Meeting]:
        """Get all meetings for a user"""
        return db.query(Meeting).filter(
            Meeting.host_id == user_id
        ).order_by(Meeting.created_at.desc()).limit(limit).all()
    
    @staticmethod
    def join_meeting(db: Session, meeting_id: UUID, user_id: UUID) -> Participant:
        """Add participant to meeting"""
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            raise ValueError("Meeting not found")
        
        # Check participant limit
        participant_count = db.query(func.count(Participant.id)).filter(
            Participant.meeting_id == meeting_id,
            Participant.left_at.is_(None)
        ).scalar()
        
        if participant_count >= meeting.max_participants:
            raise ValueError("Meeting is full")
        
        # Check if already joined
        existing = db.query(Participant).filter(
            Participant.meeting_id == meeting_id,
            Participant.user_id == user_id,
            Participant.left_at.is_(None)
        ).first()
        
        if existing:
            return existing
        
        # Create participant
        participant = Participant(
            meeting_id=meeting_id,
            user_id=user_id
        )
        db.add(participant)
        db.commit()
        db.refresh(participant)
        logger.info(f"User {user_id} joined meeting {meeting_id}")
        return participant
    
    @staticmethod
    def leave_meeting(db: Session, meeting_id: UUID, user_id: UUID) -> Participant:
        """Remove participant from meeting"""
        participant = db.query(Participant).filter(
            Participant.meeting_id == meeting_id,
            Participant.user_id == user_id,
            Participant.left_at.is_(None)
        ).first()
        
        if not participant:
            raise ValueError("Participant not found")
        
        participant.left_at = datetime.utcnow()
        participant.duration_seconds = int(
            (participant.left_at - participant.joined_at).total_seconds()
        )
        db.commit()
        db.refresh(participant)
        logger.info(f"User {user_id} left meeting {meeting_id}")
        return participant
    
    @staticmethod
    def end_meeting(db: Session, meeting_id: UUID) -> Meeting:
        """End meeting"""
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            raise ValueError("Meeting not found")
        
        meeting.status = "completed"
        meeting.ended_at = datetime.utcnow()
        
        # Mark all active participants as left
        active_participants = db.query(Participant).filter(
            Participant.meeting_id == meeting_id,
            Participant.left_at.is_(None)
        ).all()
        
        for participant in active_participants:
            participant.left_at = datetime.utcnow()
            participant.duration_seconds = int(
                (participant.left_at - participant.joined_at).total_seconds()
            )
        
        db.commit()
        db.refresh(meeting)
        logger.info(f"Meeting {meeting_id} ended")
        return meeting
    
    @staticmethod
    def get_meeting_participants(db: Session, meeting_id: UUID) -> List[Participant]:
        """Get all participants in a meeting"""
        return db.query(Participant).filter(
            Participant.meeting_id == meeting_id
        ).all()
    
    @staticmethod
    def get_meeting_transcripts(db: Session, meeting_id: UUID) -> List[Transcript]:
        """Get all transcripts for a meeting"""
        return db.query(Transcript).filter(
            Transcript.meeting_id == meeting_id
        ).order_by(Transcript.created_at.asc()).all()
    
    @staticmethod
    def add_transcript(db: Session, meeting_id: UUID, speaker_name: str, text: str, timestamp: int = 0) -> Transcript:
        """Add transcript segment"""
        transcript = Transcript(
            meeting_id=meeting_id,
            speaker_name=speaker_name,
            transcript_text=text,
            timestamp_seconds=timestamp
        )
        db.add(transcript)
        db.commit()
        db.refresh(transcript)
        return transcript
    
    @staticmethod
    def delete_meeting(db: Session, meeting_id: UUID) -> bool:
        """Delete meeting"""
        meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
        if not meeting:
            raise ValueError("Meeting not found")
        
        db.delete(meeting)
        db.commit()
        logger.info(f"Meeting {meeting_id} deleted")
        return True
