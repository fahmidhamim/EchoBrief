from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.pool import NullPool
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Create declarative base for all models
Base = declarative_base()

# Create engine
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=NullPool if settings.environment == "testing" else None,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Event listeners
@event.listens_for(engine, "connect")
def receive_connect(dbapi_conn, connection_record):
    """Enable foreign keys on SQLite"""
    pass

@event.listens_for(engine, "engine_disposed")
def receive_engine_disposed(engine):
    """Handle engine disposal"""
    logger.info("Database engine disposed")
