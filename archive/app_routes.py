from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
from quantum_universal_crawler import crawl_page
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

app = FastAPI(
    title="SocialMe API",
    description="Social media platform with advanced web crawling capabilities",
    version="2.0.0",
    openapi_version="3.1.0"
)

class CrawlRequest(BaseModel):
    topic: str
    urls: list[str]

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/crawl")
async def crawl(request: CrawlRequest):
    try:
        # Pass both url and topic to crawl_page
        results = await asyncio.gather(*[crawl_page(url, request.topic) for url in request.urls])
        return {"topic": request.topic, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
