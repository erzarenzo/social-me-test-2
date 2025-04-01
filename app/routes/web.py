"""
Web routes for the SocialMe application.
"""
import sys
import os
import traceback
from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from sqlalchemy.orm import Session
import logging

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.database import get_db
from app.models.models import Source

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Redirect to the first step of the onboarding process."""
    try:
        logger.info("Accessing home route - redirecting to content sources")
        # Redirect to the first step of the onboarding flow
        return RedirectResponse(url="/onboarding/content-sources")
    except Exception as e:
        logger.error(f"Error redirecting from home page: {str(e)}")
        logger.error(traceback.format_exc())
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": f"Internal Server Error: {str(e)}"
            },
            status_code=500
        )

@router.get("/onboarding/content-sources", response_class=HTMLResponse)
async def content_sources(request: Request):
    """Render the content sources page."""
    try:
        logger.info("Accessing content sources route")
        return templates.TemplateResponse(
            "socialme_onboarding.html",
            {"request": request}
        )
    except Exception as e:
        logger.error(f"Error rendering content sources page: {str(e)}")
        logger.error(traceback.format_exc())
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": f"Internal Server Error: {str(e)}"
            },
            status_code=500
        )

@router.get("/onboarding/writing-style", response_class=HTMLResponse)
async def writing_style(request: Request):
    """Render the writing style page."""
    try:
        logger.info("Accessing writing style route")
        return templates.TemplateResponse(
            "writing_style.html",
            {"request": request}
        )
    except Exception as e:
        logger.error(f"Error rendering writing style page: {str(e)}")
        logger.error(traceback.format_exc())
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": f"Internal Server Error: {str(e)}"
            },
            status_code=500
        )

@router.post("/analyze-content", response_class=JSONResponse)
async def analyze_content(request: Request):
    """
    Analyze content using the Neural Tone Mapper.
    This is a direct port of the standalone tone analyzer that was working previously.
    """
    try:
        logger.info("Accessing analyze-content endpoint")
        form_data = await request.form()
        content = form_data.get('content', '')
        content_type = form_data.get('type', 'text')
        
        logger.info(f"Content type: {content_type}, Content length: {len(content)}")
        
        if not content:
            logger.error("No content provided for analysis")
            return JSONResponse(
                content={'status': 'error', 'message': 'No content provided for analysis'},
                status_code=400
            )
        
        try:
            # Import our neural tone mapper
            from app.neural_tone_mapper import NeuralToneMapper
            
            # Initialize the mapper
            logger.info("Initializing NeuralToneMapper")
            mapper = NeuralToneMapper()
            
            # Analyze the text directly
            logger.info(f"Analyzing content with NeuralToneMapper")
            raw_analysis = mapper.analyze_text(content)
            logger.info(f"Raw analysis obtained: {list(raw_analysis.keys())}")
            
            # Format the analysis for display using the mapper's built-in formatter
            formatted_analysis = mapper.format_analysis_for_display(raw_analysis)
            logger.info("Analysis formatted for display")
            
            # Return the formatted analysis
            return JSONResponse(content=formatted_analysis)
        
        except Exception as e:
            logger.error(f"Error analyzing content: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return JSONResponse(
                content={'status': 'error', 'message': str(e)},
                status_code=500
            )
    
    except Exception as e:
        logger.error(f"Error in analyze-content endpoint: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return JSONResponse(
            content={'status': 'error', 'message': f"Internal Server Error: {str(e)}"},
            status_code=500
        )

@router.get("/onboarding/content-strategy", response_class=HTMLResponse)
async def content_strategy(request: Request):
    """Render the content strategy page."""
    try:
        logger.info("Accessing content strategy route")
        return templates.TemplateResponse(
            "content_strategy.html",
            {"request": request}
        )
    except Exception as e:
        logger.error(f"Error rendering content strategy page: {str(e)}")
        logger.error(traceback.format_exc())
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": f"Internal Server Error: {str(e)}"
            },
            status_code=500
        )

@router.get("/onboarding/advanced-article-generator", response_class=HTMLResponse)
async def advanced_article_generator(request: Request):
    """Render the advanced article generator page."""
    try:
        logger.info("Accessing advanced article generator route")
        return templates.TemplateResponse(
            "advanced_article_generator.html",
            {"request": request}
        )
    except Exception as e:
        logger.error(f"Error rendering advanced article generator page: {str(e)}")
        logger.error(traceback.format_exc())
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": f"Internal Server Error: {str(e)}"
            },
            status_code=500
        )

@router.get("/onboarding/article-preview", response_class=HTMLResponse)
async def article_preview(request: Request):
    """Render the article preview page."""
    try:
        logger.info("Accessing article preview route")
        return templates.TemplateResponse(
            "article_preview.html",
            {"request": request}
        )
    except Exception as e:
        logger.error(f"Error rendering article preview page: {str(e)}")
        logger.error(traceback.format_exc())
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": f"Internal Server Error: {str(e)}"
            },
            status_code=500
        )

@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    """Render the login page."""
    try:
        logger.info("Accessing login route")
        return templates.TemplateResponse(
            "login.html",
            {"request": request}
        )
    except Exception as e:
        logger.error(f"Error rendering login page: {str(e)}")
        logger.error(traceback.format_exc())
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": f"Internal Server Error: {str(e)}"
            },
            status_code=500
        )

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the dashboard page."""
    try:
        logger.info("Accessing dashboard route")
        return templates.TemplateResponse(
            "dashboard.html",
            {"request": request}
        )
    except Exception as e:
        logger.error(f"Error rendering dashboard page: {str(e)}")
        logger.error(traceback.format_exc())
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": f"Internal Server Error: {str(e)}"
            },
            status_code=500
        )

@router.get("/test", response_class=HTMLResponse)
async def test_page(request: Request):
    """Render the test page."""
    try:
        logger.info("Accessing test page route")
        return templates.TemplateResponse(
            "test_page.html", 
            {"request": request}
        )
    except Exception as e:
        logger.error(f"Error rendering test page: {str(e)}")
        logger.error(traceback.format_exc())
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error_message": f"Internal Server Error: {str(e)}"
            },
            status_code=500
        )
