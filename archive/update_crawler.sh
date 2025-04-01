#!/bin/bash
echo "Making a backup of current crawler..."
cp quantum_universal_crawler.py quantum_universal_crawler.py.bak

echo "Updating topic relevance scoring, multi-URL processing, and deduplication..."

# Update the app.py file for the API endpoint
cat > app_update.py << 'APPEOF'
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import traceback
import logging
from quantum_universal_crawler import crawl_page
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

logger = logging.getLogger("api")

app = FastAPI(
    title="SocialMe API",
    description="Social media platform with advanced web crawling capabilities",
    version="2.0.0",
    openapi_version="3.1.0"
)

class CrawlRequest(BaseModel):
    topic: str
    urls: list

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/crawl")
async def crawl(request: CrawlRequest):
    try:
        # Create a list of tasks for each URL
        tasks = []
        for url in request.urls:
            # Create a task for each URL
            task = crawl_page(url, request.topic)
            tasks.append(task)
            
        # Use asyncio.gather with await to properly wait for all results
        results = await asyncio.gather(*tasks)
        
        # Return the combined results
        return {"topic": request.topic, "results": results}
    except Exception as e:
        # Improved error handling
        logger.error(f"Error processing crawl request: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
APPEOF

echo "Updated FastAPI app file created. Copy the contents to your app.py if needed."
echo "You can use: cat app_update.py > app.py"
echo "Restart your uvicorn server after making all changes."
echo 
echo "Done! Your crawler should now have improved topic relevance, multiple URL processing, and deduplication."
