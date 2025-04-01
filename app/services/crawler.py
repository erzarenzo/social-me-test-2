"""
Crawler service for the SocialMe application.
"""
import logging
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime
import sys
import os

# Add the parent directory to the path to import quantum_universal_crawler
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from quantum_universal_crawler import crawl_page, CrawlResult

logger = logging.getLogger(__name__)

async def crawl_url(url: str, topic: str) -> CrawlResult:
    """
    Crawl a URL for content related to the topic.
    
    Args:
        url: The URL to crawl
        topic: The topic to focus on
        
    Returns:
        CrawlResult: The result of the crawl
    """
    try:
        logger.info(f"Crawling {url} for topic: {topic}")
        result = await crawl_page(url, topic)
        return result
    except Exception as e:
        logger.error(f"Error crawling {url}: {str(e)}")
        # Return an empty result with error status
        return CrawlResult(
            url=url,
            content="",
            status="error",
            word_count=0,
            source="direct_crawl",
            error_reason=str(e),
            confidence_score=0.0
        )

async def crawl_multiple_urls(urls: List[str], topic: str) -> List[CrawlResult]:
    """
    Crawl multiple URLs concurrently.
    
    Args:
        urls: List of URLs to crawl
        topic: The topic to focus on
        
    Returns:
        List[CrawlResult]: The results of the crawls
    """
    tasks = [crawl_url(url, topic) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Process results to handle any exceptions
    processed_results = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            # Create an error result
            processed_results.append(CrawlResult(
                url=urls[i],
                content="",
                status="error",
                word_count=0,
                source="direct_crawl",
                error_reason=str(result),
                confidence_score=0.0
            ))
        else:
            processed_results.append(result)
    
    return processed_results
