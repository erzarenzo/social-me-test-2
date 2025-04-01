"""
Database models for the SocialMe application.
"""
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

# Import Base from database module
from app.database import Base

class Source(Base):
    """Source model for storing web sources to crawl."""
    __tablename__ = 'sources'
    
    id = Column(Integer, primary_key=True)
    link = Column(String(500), nullable=False)
    source_type = Column(String(50), nullable=False, default='website')
    created_at = Column(DateTime, default=datetime.utcnow)
    last_crawled = Column(DateTime, nullable=True)
    
    # Relationships
    contents = relationship("Content", back_populates="source", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Source(id={self.id}, link='{self.link}', type='{self.source_type}')>"

class Content(Base):
    """Content model for storing crawled content."""
    __tablename__ = 'contents'
    
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('sources.id'), nullable=False)
    content_text = Column(Text, nullable=False)
    word_count = Column(Integer, default=0)
    confidence_score = Column(Integer, default=0)
    crawled_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    source = relationship("Source", back_populates="contents")
    
    def __repr__(self):
        return f"<Content(id={self.id}, source_id={self.source_id}, words={self.word_count})>"
