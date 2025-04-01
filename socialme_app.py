from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logging
from datetime import datetime
import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add app directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import our organized modules
from app.routes.web import router as web_router
from app.routes.api import router as api_router
from app.database import init_db

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('socialme_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("api")

# Initialize FastAPI app with metadata
app = FastAPI(
    title="SocialMe",
    description="Social media platform with advanced web crawling capabilities",
    version="1.0.0",
    openapi_version="3.1.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Include routers
app.include_router(web_router)
app.include_router(api_router)

# Initialize database
init_db()

# WebSocket endpoint for chat
@app.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Echo back for now, in a real app this would process the message
            await websocket.send_text(f"You said: {data}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
    finally:
        # Clean up when the connection is closed
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "socialme_app:app", 
        host="0.0.0.0", 
        port=8003, 
        reload=True
    )
