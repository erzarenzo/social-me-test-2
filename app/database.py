"""
Database connection and session management for the SocialMe application.
"""
import sys
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Get database URI from environment variable or use default
DB_URI = os.getenv("DB_URI", "sqlite:///instance/socialme.db")
logger.info(f"Using database URI: {DB_URI}")

# Create database directory if it doesn't exist
if DB_URI.startswith("sqlite:///"):
    db_path = DB_URI.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)

# Create database engine
engine = create_engine(DB_URI, connect_args={"check_same_thread": False})

# Create session factory
session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = scoped_session(session_factory)

# Base class for all models
Base = declarative_base()

def get_db():
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables."""
    # Import all models here to ensure they are registered with Base
    # We need to import them here to avoid circular imports
    from app.models.models import Source, Content
    
    logger.info("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise
