from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth import AuthService
from app.schemas.auth import UserCreate, LoginRequest, TokenResponse, UserResponse
import logging
from typing import Optional

security = HTTPBearer()

logger = logging.getLogger(__name__)
router = APIRouter()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Extract user ID from JWT token"""
    try:
        token = credentials.credentials
        logger.info(f"Validating token: {token[:20]}...")
        
        payload = AuthService.decode_token(token)
        if not payload:
            logger.error("Token decode failed")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        user_id = payload.get("sub")
        if not user_id:
            logger.error("No user ID in token")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        logger.info(f"User authenticated: {user_id}")
        return user_id
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authorization error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing token")

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register new user"""
    try:
        user = AuthService.register_user(db, user_data)
        token = AuthService.create_access_token({"sub": str(user.id), "email": user.email})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": UserResponse.from_orm(user)
        }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Registration failed")

@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Login user"""
    try:
        user = AuthService.authenticate_user(db, credentials.email, credentials.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        token = AuthService.create_access_token({"sub": str(user.id), "email": user.email})
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": UserResponse.from_orm(user)
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Login failed")

@router.get("/me", response_model=UserResponse)
async def get_current_user(db: Session = Depends(get_db), user_id: str = Depends(get_current_user_id)):
    """Get current user profile"""
    user = AuthService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return UserResponse.from_orm(user)
