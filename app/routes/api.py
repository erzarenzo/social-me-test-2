"""
API routes for the SocialMe application.
"""
import sys
import os
from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from pydantic import BaseModel
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import logging
from app.services.crawler import crawl_url
from app.advanced_article_generator import ArticleGenerator
from app.neural_tone_mapper import NeuralToneMapper
import numpy as np
import re
from tempfile import NamedTemporaryFile

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import get_db
from app.models.models import Source, Content

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("api")

router = APIRouter(prefix="/api", tags=["api"])

class SourceRequest(BaseModel):
    url: str
    source_type: str = "website"

class SourceResponse(BaseModel):
    id: int
    link: str
    source_type: str
    
    class Config:
        orm_mode = True

class CrawlRequest(BaseModel):
    topic: str
    urls: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "topic": "artificial intelligence",
                "urls": ["https://example.com/ai", "https://example.com/ml"]
            }
        }

class CrawlResponse(BaseModel):
    url: str
    content: str
    word_count: int
    confidence_score: float
    
    class Config:
        orm_mode = True

class StyleProfile(BaseModel):
    voice_profile: Dict[str, Any]
    linguistic_patterns: Dict[str, Any]
    content_structure: Dict[str, Any]

class SourceMaterial(BaseModel):
    url: str
    title: str
    content: str
    date: str

class ArticleGenerationRequest(BaseModel):
    topic: str
    style_profile: StyleProfile
    source_material: List[SourceMaterial]
    
    class Config:
        schema_extra = {
            "example": {
                "topic": "The Impact of Artificial Intelligence on Modern Society",
                "style_profile": {
                    "voice_profile": {
                        "formality": 0.8,
                        "technical_level": 0.7,
                        "persuasiveness": 0.6,
                        "emotional_tone": "neutral",
                        "engagement_style": "informative"
                    },
                    "linguistic_patterns": {
                        "sentence_length": "medium",
                        "vocabulary_complexity": "high",
                        "transition_phrases": ["furthermore", "however", "in addition"],
                        "rhetorical_devices": ["analogy", "rhetorical question"]
                    },
                    "content_structure": {
                        "intro_style": "question-based",
                        "paragraph_structure": "claim-evidence-explanation",
                        "conclusion_style": "summary with call to action"
                    }
                },
                "source_material": [
                    {
                        "url": "https://example.com/ai-article-1",
                        "title": "The Evolution of AI in the 21st Century",
                        "content": "Artificial Intelligence has evolved significantly in the past decade...",
                        "date": "2023-05-15"
                    }
                ]
            }
        }

class ArticleGenerationResponse(BaseModel):
    title: str
    subtitle: str
    introduction: str
    overview: str
    body: List[Dict[str, Any]]
    conclusion: str
    sources: List[Dict[str, str]]
    stats: Dict[str, Any]

class AnalysisResponse(BaseModel):
    status: str
    analysis: Dict[str, Any] = None
    message: str = None

@router.post("/sources", response_model=SourceResponse)
async def add_source(source: SourceRequest, db: Session = Depends(get_db)):
    """Add a new source to the database."""
    db_source = Source(link=source.url, source_type=source.source_type)
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

@router.get("/sources", response_model=List[SourceResponse])
async def get_sources(db: Session = Depends(get_db)):
    """Get all sources from the database."""
    sources = db.query(Source).all()
    return sources

@router.post("/crawl", response_model=List[CrawlResponse])
async def crawl(request: CrawlRequest, db: Session = Depends(get_db)):
    """Crawl the specified URLs for content related to the topic."""
    results = []
    
    for url in request.urls:
        try:
            result = await crawl_url(url, request.topic)
            results.append(result)
            
            # Save to database
            source = db.query(Source).filter(Source.link == url).first()
            if not source:
                source = Source(link=url, source_type="website")
                db.add(source)
                db.commit()
                db.refresh(source)
            
            content = Content(
                source_id=source.id,
                content_text=result.content,
                word_count=result.word_count,
                confidence_score=result.confidence_score
            )
            db.add(content)
            db.commit()
            
        except Exception as e:
            # Log the error but continue with other URLs
            print(f"Error crawling {url}: {str(e)}")
    
    return results

@router.post("/generate-article", response_model=ArticleGenerationResponse)
async def generate_article(request: ArticleGenerationRequest):
    """Generate an article using the Advanced Article Generator."""
    try:
        logger.info(f"Generating advanced article on topic: {request.topic}")
        logger.info(f"Using {len(request.source_material)} sources")
        
        # Initialize the ArticleGenerator
        generator = ArticleGenerator()
        
        # Generate the article
        article = generator.generate_article(
            topic=request.topic,
            style_profile=request.style_profile.dict(),
            source_material=request.source_material
        )
        
        logger.info(f"Generated article with title: {article.get('title', 'No title')}")
        
        # Check if there was an error
        if "error" in article:
            logger.error(f"Error in article generation: {article.get('error')}")
            raise HTTPException(status_code=500, detail=article.get("error", "Unknown error"))
        
        # Calculate stats
        word_count = sum(len(str(v).split()) for v in article.values() if isinstance(v, str))
        if isinstance(article.get("body"), list):
            for section in article.get("body", []):
                if isinstance(section, dict) and "content" in section:
                    word_count += len(section["content"].split())
                    
        reading_time = max(1, word_count // 200)  # Assume 200 words per minute
        sections_count = len(article.get("body", [])) if isinstance(article.get("body"), list) else 3
        
        # Format the response
        formatted_article = {
            "title": article.get("title", "Generated Article"),
            "subtitle": article.get("subtitle", ""),
            "introduction": article.get("introduction", ""),
            "overview": article.get("overview", ""),
            "body": article.get("body", []),
            "conclusion": article.get("conclusion", ""),
            "sources": [{"name": source.title, "url": source.url} for source in request.source_material],
            "stats": {
                "sections": sections_count,
                "words": word_count,
                "reading_time": reading_time
            }
        }
        
        return formatted_article
        
    except Exception as e:
        logger.error(f"Exception in generate_article: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-content", response_model=AnalysisResponse)
async def analyze_writing_style(
    content: str = Form(...),
    type: str = Form(...),
):
    """
    Analyze writing style from content using NeuralToneMapper
    """
    logger.info(f"Content type: {type}, Content length: {len(content)}")
    
    if not content:
        logger.error("No content provided for analysis")
        return {"status": "error", "message": "No content provided for analysis"}
    
    try:
        # Import and initialize the NeuralToneMapper
        logger.info("Initializing NeuralToneMapper")
        mapper = NeuralToneMapper()
        
        # Analyze the text directly
        raw_analysis = mapper.analyze_text(content)
        logger.info(f"Raw analysis obtained: {list(raw_analysis.keys())}")
        
        # Format the analysis for display using the mapper's built-in formatter
        formatted_analysis = mapper.format_analysis_for_display(raw_analysis)
        logger.info("Analysis formatted for display")
        
        # Return the formatted analysis
        return formatted_analysis
        
    except Exception as e:
        logger.error(f"Error in content analysis: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return {"status": "error", "message": str(e)}

@router.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "2.0.0"}
