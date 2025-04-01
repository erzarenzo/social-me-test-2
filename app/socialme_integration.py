#!/usr/bin/env python3
"""
SocialMe Integration System

This script integrates the three main components of the SocialMe system:
1. Source Crawler - Extract content from various web sources
2. Article Generator - Generate high-quality articles based on sources
3. Article Evaluation - Evaluate and improve article quality

It implements a workflow that combines traditional tools with LLM chain prompting.
"""

import os
import sys
import json
import time
import logging
import argparse
from datetime import datetime
from typing import List, Dict, Any, Tuple, Optional

# Import the three main components
# Make sure these modules are in the same directory or in PYTHONPATH
try:
    from socialme_app import app, db, Source
    from universal_crawler import extract_content_from_url, add_source_with_content
    from article_evaluation import evaluate_article
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Make sure your PYTHONPATH is set correctly.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    handlers=[
        logging.FileHandler("socialme.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("SocialMe")

class SocialMeSystem:
    """Main class for the SocialMe system, integrating all components."""
    
    def __init__(self, api_preference="anthropic"):
        """Initialize the SocialMe system."""
        self.api_preference = api_preference
        logger.info("SocialMe system initialized")
    
    def gather_sources(self, urls: List[str]) -> List[Dict[str, Any]]:
        """Gather content from URLs using the Source Crawler."""
        logger.info(f"Gathering sources from {len(urls)} URLs")
        sources = []
        
        with app.app_context():
            for url in urls:
                logger.info(f"Extracting content from: {url}")
                source = add_source_with_content(url)
                if source:
                    sources.append({
                        "url": source.url,
                        "content": source.full_text,
                        "wordCount": len(source.full_text.split())
                    })
                    logger.info(f"Added source: {url}")
                else:
                    logger.warning(f"Failed to extract content from: {url}")

        return sources

    def generate_article(self, topic: str, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate an article based on the sources and topic."""
        logger.info(f"Generating article for topic: {topic}")

        # Call Article Generator (to be implemented)
        article_content = f"### {topic}\n\nThis is a generated article using LLM models.\n\n"

        article = {
            "title": f"Comprehensive Guide to {topic}",
            "content": article_content,
            "wordCount": 4000,
            "sources": sources,
            "generatedDate": datetime.now().isoformat()
        }
        
        return article

    def evaluate_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate the article using the Article Evaluation component."""
        logger.info(f"Evaluating article: {article['title']}")

        evaluation_results = evaluate_article(article["content"], [s["url"] for s in article["sources"]])

        return evaluation_results

    def run_pipeline(self, topic: str, urls: List[str]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """Run the full SocialMe content generation pipeline."""
        sources = self.gather_sources(urls)
        article = self.generate_article(topic, sources)
        evaluation = self.evaluate_article(article)

        return article, evaluation

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="SocialMe AI System")
    
    parser.add_argument("--topic", type=str, required=True, help="Article topic")
    parser.add_argument("--urls", type=str, nargs="+", required=True, help="Source URLs")
    
    return parser.parse_args()

def main():
    """Main function to execute the pipeline from CLI."""
    args = parse_arguments()
    
    system = SocialMeSystem()
    article, evaluation = system.run_pipeline(args.topic, args.urls)
    
    print(f"\nGenerated Article: {article['title']}")
    print(f"Word Count: {article['wordCount']}")
    print(f"Evaluation Score: {evaluation.get('overall_score', 'N/A')}\n")

if __name__ == "__main__":
    main()
