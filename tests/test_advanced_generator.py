#!/usr/bin/env python3
"""
Test script for Advanced Article Generator
"""

import os
import json
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("test_script")

# Load environment variables
load_dotenv()

# Check required environment variables
claude_api_key = os.getenv("CLAUDE_API_KEY")
if not claude_api_key:
    logger.warning("CLAUDE_API_KEY not found in environment variables!")
else:
    logger.info("CLAUDE_API_KEY found in environment")

# Check for the Advanced Article Generator module
try:
    from app.advanced_article_generator import ArticleGenerator
    logger.info("Successfully imported ArticleGenerator class")
    
    # Initialize the generator
    generator = ArticleGenerator(api_key=claude_api_key)
    logger.info("Successfully initialized ArticleGenerator")
    
    # Check if Claude client is available
    if generator.client:
        logger.info("Claude client successfully initialized")
    else:
        logger.warning("Claude client not available, will use fallback methods")
    
except ImportError as e:
    logger.error(f"Failed to import ArticleGenerator: {e}")
    exit(1)

# Test the article generation with minimal inputs
logger.info("Testing article generation with minimal inputs...")

# Sample test data
topic = "Artificial Intelligence"
style_profile = {
    "thought_patterns": ["Analytical", "Strategic"],
    "reasoning_architecture": ["Logical", "Evidence-based"],
    "communication_framework": ["Technical", "Educational"]
}
source_material = [
    {
        "title": "Test Source 1",
        "url": "https://example.com/1",
        "content": "AI is transforming how businesses operate in the digital age.",
        "relevance_score": 0.9
    },
    {
        "title": "Test Source 2",
        "url": "https://example.com/2",
        "content": "Neural networks are a key component of modern AI systems.",
        "relevance_score": 0.8
    }
]

# Generate a test article
try:
    article = generator.generate_article(
        topic=topic,
        style_profile=style_profile,
        source_material=source_material
    )
    
    logger.info(f"Article generation successful! Title: {article.get('title', 'No title')}")
    logger.info(f"Article structure: {json.dumps(article.keys(), indent=2)}")
    
    print("\nArticle Preview:")
    print(f"Title: {article.get('title', 'No title')}")
    print(f"Introduction: {article.get('introduction', 'No introduction')[:100]}...")
    
    if article.get('error'):
        logger.warning(f"Article generated with error flag: {article.get('error')}")
    
except Exception as e:
    logger.error(f"Error generating test article: {e}")
    import traceback
    logger.error(traceback.format_exc())

logger.info("Test completed")
