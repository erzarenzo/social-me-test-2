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
