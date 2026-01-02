from sqlalchemy.orm import Session
from app.models.summary import Summary
from app.models.meeting import Meeting
from app.models.transcript import Transcript
from app.config import settings
from typing import List, Optional, Dict
from datetime import datetime
from uuid import UUID
import logging
import json

logger = logging.getLogger(__name__)

class AIService:
    @staticmethod
    def transcribe_audio(audio_path: str) -> Dict:
        """
        Transcribe audio using Faster-Whisper
        Returns: {"text": str, "segments": list}
        """
        try:
            from faster_whisper import WhisperModel
            
            model = WhisperModel("base", device="cpu", compute_type="int8")
            segments, info = model.transcribe(audio_path, language="en")
            
            full_text = ""
            segments_list = []
            
            for segment in segments:
                full_text += segment.text + " "
                # faster-whisper segments may not expose `confidence`; fall back to avg_logprob
                confidence = getattr(segment, "confidence", None)
                if confidence is None:
                    confidence = getattr(segment, "avg_logprob", None)
                segments_list.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text,
                    "confidence": confidence
                })
            
            return {
                "text": full_text.strip(),
                "segments": segments_list,
                "duration": info.duration
            }
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            raise
    
    @staticmethod
    def generate_summary(transcript_text: str, max_length: int = 500) -> Dict:
        """
        Generate summary using Groq or OpenAI
        Returns: {"summary": str, "action_items": list, "keywords": list}
        """
        summary_data: Dict = {}
        try:
            # Try OpenAI first since Groq has compatibility issues
            if settings.openai_api_key:
                summary_data = AIService._summarize_with_openai(transcript_text, max_length)
            elif settings.groq_api_key and AIService._groq_supported():
                summary_data = AIService._summarize_with_groq(transcript_text, max_length)
            else:
                raise ValueError("No AI service configured")
        except Exception as e:
            logger.error(f"AI service failed, using fallback: {str(e)}")
            # Fallback to basic summary
            summary_data = AIService._generate_basic_summary(transcript_text, max_length)

        # Always attach basic metadata so response validation does not fail
        word_count = summary_data.get("word_count")
        if word_count is None and transcript_text:
            word_count = len(transcript_text.split())
        summary_data["word_count"] = word_count
        summary_data.setdefault("duration_seconds", None)

        return summary_data
    
    @staticmethod
    def _summarize_with_groq(transcript_text: str, max_length: int) -> Dict:
        """Summarize using Groq API"""
        try:
            import os
            from groq import Groq

            logger.info("Initializing Groq client")
            # Set API key via environment variable to avoid initialization issues
            os.environ['GROQ_API_KEY'] = settings.groq_api_key
            client = Groq()

            prompt = f"""Analyze this meeting transcript and provide:
1. A concise summary (max {max_length} words)
2. Key action items (as a list)
3. Important keywords (as a list)

Transcript:
{transcript_text}

Provide response in JSON format with keys: summary, action_items, keywords"""

            logger.info(f"Sending request to Groq API, prompt length: {len(prompt)}")
            # mixtral-8x7b-32768 was decommissioned; use a current supported model
            completion = client.chat.completions.create(
                model="llama-3.1-70b-versatile",
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            response_text = completion.choices[0].message.content
            logger.info(f"Groq response received, length: {len(response_text)}, content: {response_text[:200]}...")

            result = json.loads(response_text)

            return {
                "summary": result.get("summary", ""),
                "action_items": result.get("action_items", []),
                "keywords": result.get("keywords", [])
            }
        except json.JSONDecodeError as e:
            logger.error(f"Groq JSON decode error: {str(e)}, response: {response_text}")
            # Return a default response if JSON parsing fails
            return {
                "summary": "Summary generation in progress",
                "action_items": [],
                "keywords": []
            }
        except Exception as e:
            logger.error(f"Groq summarization error: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def _summarize_with_openai(transcript_text: str, max_length: int) -> Dict:
        """Summarize using OpenAI API"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=settings.openai_api_key)
            
            prompt = f"""Analyze this meeting transcript and provide:
1. A concise summary (max {max_length} words)
2. Key action items (as a list)
3. Important keywords (as a list)

Transcript:
{transcript_text}

Provide response in JSON format with keys: summary, action_items, keywords"""
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            
            response_text = response.choices[0].message.content
            result = json.loads(response_text)
            
            return {
                "summary": result.get("summary", ""),
                "action_items": result.get("action_items", []),
                "keywords": result.get("keywords", [])
            }
        except Exception as e:
            logger.error(f"OpenAI summarization error: {str(e)}")
            raise
    
    @staticmethod
    def save_summary(db: Session, meeting_id: UUID, summary_data: Dict) -> Summary:
        """Save summary to database"""
        word_count = summary_data.get("word_count")
        if word_count is None and summary_data.get("summary"):
            word_count = len(summary_data["summary"].split())

        # Upsert to avoid unique constraint errors on repeat summarization
        summary = db.query(Summary).filter(Summary.meeting_id == meeting_id).first()
        if summary:
            summary.summary_text = summary_data.get("summary", "")
            summary.action_items = summary_data.get("action_items", [])
            summary.keywords = summary_data.get("keywords", [])
            summary.duration_seconds = summary_data.get("duration_seconds")
            summary.word_count = word_count
            summary.generated_at = datetime.utcnow()
        else:
            summary = Summary(
                meeting_id=meeting_id,
                summary_text=summary_data.get("summary", ""),
                action_items=summary_data.get("action_items", []),
                keywords=summary_data.get("keywords", []),
                duration_seconds=summary_data.get("duration_seconds"),
                word_count=word_count,
                generated_at=datetime.utcnow()
            )
            db.add(summary)
        db.commit()
        db.refresh(summary)
        logger.info(f"Summary saved for meeting {meeting_id}")
        return summary
    
    @staticmethod
    def _generate_basic_summary(transcript_text: str, max_length: int = 500) -> Dict:
        """Generate a basic summary without AI"""
        try:
            import re
            from collections import Counter
            
            # Extract basic summary
            words = transcript_text.split()
            if len(words) > max_length:
                summary = " ".join(words[:max_length]) + "..."
            else:
                summary = transcript_text
            
            # Extract potential action items (sentences with action words)
            action_words = ['will', 'should', 'need to', 'going to', 'plan to', 'decided to']
            action_items = []
            sentences = re.split(r'[.!?]+', transcript_text)
            for sentence in sentences:
                sentence = sentence.strip()
                if any(word in sentence.lower() for word in action_words) and len(sentence) > 10:
                    action_items.append(sentence)
            
            # Extract keywords (most common words)
            common_words = set(['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'])
            word_count = Counter(word.lower().strip('.,!?') for word in words if word.lower() not in common_words and len(word) > 3)
            keywords = [word for word, count in word_count.most_common(10)]
            
            return {
                "summary": summary,
                "action_items": action_items[:5],  # Limit to 5 action items
                "keywords": keywords,
                "word_count": len(words),
                "duration_seconds": None
            }
        except Exception as e:
            logger.error(f"Basic summary error: {str(e)}")
            return {
                "summary": transcript_text[:max_length] + "..." if len(transcript_text) > max_length else transcript_text,
                "action_items": [],
                "keywords": [],
                "word_count": len(transcript_text.split()) if transcript_text else 0,
                "duration_seconds": None
            }

    @staticmethod
    def _groq_supported() -> bool:
        """
        Groq client currently breaks with httpx 0.28+ (proxies arg removed).
        Skip Groq if an incompatible httpx version is installed.
        """
        try:
            import httpx

            parts = httpx.__version__.split(".")
            major = int(parts[0]) if parts else 0
            minor = int(parts[1]) if len(parts) > 1 else 0
            if major > 0:
                return False
            if minor >= 28:
                logger.warning("Skipping Groq: httpx %s is incompatible; use httpx<0.28", httpx.__version__)
                return False
            return True
        except Exception as e:
            logger.warning(f"Unable to determine Groq compatibility: {e}")
            return False

    @staticmethod
    def get_summary(db: Session, meeting_id: UUID) -> Optional[Summary]:
        """Get summary for a meeting"""
        return db.query(Summary).filter(Summary.meeting_id == meeting_id).first()
