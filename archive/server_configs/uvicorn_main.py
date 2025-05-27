"""
Main entry point for the SocialMe application.
"""
import uvicorn
from config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "socialme_app:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
