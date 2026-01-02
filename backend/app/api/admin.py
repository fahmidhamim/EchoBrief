from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.user import User
from app.models.meeting import Meeting
from app.models.transcript import Participant
from app.models.summary import Summary
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/metrics")
async def get_metrics(db: Session = Depends(get_db), user_id: str = None):
    """Get system metrics"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        # Check if user is admin
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
        
        # Get metrics
        total_users = db.query(func.count(User.id)).scalar()
        total_meetings = db.query(func.count(Meeting.id)).scalar()
        completed_meetings = db.query(func.count(Meeting.id)).filter(Meeting.status == "completed").scalar()
        total_participants = db.query(func.count(Participant.id)).scalar()
        total_summaries = db.query(func.count(Summary.id)).scalar()
        
        return {
            "total_users": total_users,
            "total_meetings": total_meetings,
            "completed_meetings": completed_meetings,
            "total_participants": total_participants,
            "total_summaries": total_summaries,
            "active_meetings": total_meetings - completed_meetings
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Metrics error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get metrics")

@router.get("/users")
async def get_users(limit: int = 100, offset: int = 0, db: Session = Depends(get_db), user_id: str = None):
    """Get all users"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        # Check if user is admin
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
        
        users = db.query(User).offset(offset).limit(limit).all()
        return [
            {
                "id": str(u.id),
                "name": u.name,
                "email": u.email,
                "is_admin": u.is_admin,
                "created_at": u.created_at
            }
            for u in users
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get users error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get users")

@router.get("/meetings")
async def get_all_meetings(limit: int = 100, offset: int = 0, db: Session = Depends(get_db), user_id: str = None):
    """Get all meetings"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        # Check if user is admin
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_admin:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
        
        meetings = db.query(Meeting).offset(offset).limit(limit).all()
        return [
            {
                "id": str(m.id),
                "title": m.meeting_title,
                "host_id": str(m.host_id),
                "status": m.status,
                "participants_count": len(m.participants),
                "created_at": m.created_at,
                "ended_at": m.ended_at
            }
            for m in meetings
        ]
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get meetings error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to get meetings")
