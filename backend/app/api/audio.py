from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from uuid import UUID
import os
from app.database import get_db
from app.config import settings
from app.services.ai import AIService
from app.services.meeting import MeetingService
from app.schemas.audio import AudioUploadResponse
from app.models.summary import AudioFile
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/upload", response_model=dict)
async def upload_audio(
    meeting_id: UUID,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: str = None
):
    """Upload audio file for meeting"""
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # Validate file size
        contents = await file.read()
        if len(contents) > settings.max_file_size:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File too large"
            )
        # Ensure meeting exists
        meeting = MeetingService.get_meeting(db, meeting_id)
        if not meeting:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Meeting not found")
        
        # Save file
        filename = f"{meeting_id}_{file.filename}"
        file_path = os.path.join(settings.upload_dir, filename)
        with open(file_path, "wb") as f:
            f.write(contents)

        audio_url = f"/uploads/{filename}"

        # Save audio file record
        audio_file = AudioFile(
            meeting_id=meeting_id,
            file_path=audio_url,
            file_size=len(contents),
            format=file.content_type or "audio",
            duration_seconds=transcription.get("duration")
        )
        db.add(audio_file)
        db.commit()
        db.refresh(audio_file)
        
        # Transcribe and store transcript rows so /api/ai/summarize can work
        transcription = AIService.transcribe_audio(file_path)
        segments = transcription.get("segments", [])
        for segment in segments:
            MeetingService.add_transcript(
                db=db,
                meeting_id=meeting_id,
                speaker_name=segment.get("speaker") or "Speaker",
                text=segment.get("text", ""),
                timestamp=int(segment.get("start", 0))
            )
        
        return {
            "status": "uploaded",
            "file_path": audio_url,
            "file_size": len(contents),
            "filename": file.filename,
            "transcript_text": transcription.get("text", ""),
            "segments_saved": len(segments)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Upload failed")
