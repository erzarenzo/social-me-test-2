"""
Script to add dummy sources to the database for testing.
"""
import os
import sys
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, init_db
from app.models.models import Source, Content

def add_dummy_sources():
    """Add dummy sources to the database for testing."""
    logger.info("Adding dummy sources to the database...")
    
    # First initialize the database to create tables
    init_db()
    
    # Create a database session
    db = SessionLocal()
    
    try:
        # Check if sources already exist
        existing_sources = db.query(Source).all()
        if existing_sources:
            logger.info(f"Found {len(existing_sources)} existing sources. Skipping dummy data creation.")
            return
        
        # Create dummy sources
        dummy_sources = [
            Source(
                link="https://linkedin.com/company/acme-corp",
                source_type="linkedin",
                created_at=datetime.utcnow()
            ),
            Source(
                link="https://twitter.com/acme_official",
                source_type="twitter",
                created_at=datetime.utcnow()
            ),
            Source(
                link="https://blog.acme-corp.com",
                source_type="blog",
                created_at=datetime.utcnow()
            ),
            Source(
                link="https://news.industry.com/feed",
                source_type="rss",
                created_at=datetime.utcnow()
            ),
            Source(
                link="https://newsletter.tech.com",
                source_type="newsletter",
                created_at=datetime.utcnow()
            )
        ]
        
        # Add sources to the database
        db.add_all(dummy_sources)
        db.commit()
        
        logger.info(f"Added {len(dummy_sources)} dummy sources to the database.")
        
        # Create some dummy content for the first source
        dummy_content = Content(
            source_id=1,
            content_text="This is some sample content crawled from the dummy source.",
            word_count=10,
            confidence_score=85,
            crawled_at=datetime.utcnow()
        )
        
        db.add(dummy_content)
        db.commit()
        
        logger.info("Added dummy content to the database.")
        
    except Exception as e:
        logger.error(f"Error adding dummy sources: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_dummy_sources()
