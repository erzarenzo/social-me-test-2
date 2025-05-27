"""
Tone Crawler Module

This module provides a crawler implementation for analyzing tone from content sources.
It extracts text from various sources and prepares it for tone analysis.
"""

import logging
import requests
from typing import Dict, List, Any, Optional
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from app.crawlers.base import BaseCrawler

# Import the QuantumToneCrawler
try:
    from app.quantum_tone_crawler import QuantumToneCrawler
except ImportError:
    # Try alternate path
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    try:
        from quantum_tone_crawler import QuantumToneCrawler
    except ImportError:
        from app.standalone_tone_analyzer import QuantumToneCrawler

logger = logging.getLogger(__name__)

class ToneCrawler(BaseCrawler):
    """
    Tone Crawler implementation that wraps the QuantumToneCrawler.
    
    This crawler focuses on content that is particularly relevant for tone and style analysis,
    extracting paragraphs, sentences, and other text elements that reveal writing style.
    """
    
    def __init__(self):
        """Initialize the ToneCrawler with required configuration"""
        super().__init__()
        self.name = "ToneCrawler"
        self.description = "Specialized crawler for tone and style analysis"
        self.quantum_crawler = QuantumToneCrawler()
        logger.info(f"Initialized {self.name} with QuantumToneCrawler backend")
    
    def crawl_analyze_source(self, source: str) -> Dict[str, Any]:
        """
        Analyze a source for tone and style characteristics
        
        Args:
            source (str): URL or text content to analyze
        
        Returns:
            Dict[str, Any]: Tone and style analysis results
        """
        try:
            # Check if source is a URL
            if source.startswith(('http://', 'https://')):
                content = self.extract_content_from_url(source)
            else:
                content = source
            
            # Perform quantum tone analysis
            tone_analysis = self.quantum_crawler.analyze_tone(content)
            
            return {
                "source": source,
                "tone_analysis": tone_analysis,
                "content": content
            }
        except Exception as e:
            logger.error(f"Error analyzing source {source}: {e}")
            return {
                "source": source,
                "error": str(e)
            }
    
    def extract_content_from_url(self, url: str) -> str:
        """
        Extract text content from a given URL
        
        Args:
            url (str): URL to extract content from
        
        Returns:
            str: Extracted text content
        """
        try:
            # Use requests to fetch the URL content
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Use BeautifulSoup to parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text from main content areas
            main_content = soup.find(['article', 'main', 'div', 'body'])
            
            # If no main content found, use the entire body
            if not main_content:
                main_content = soup.body
            
            # Extract text, removing script and style tags
            for script_or_style in main_content(['script', 'style']):
                script_or_style.decompose()
            
            # Get text and clean it up
            text = main_content.get_text(separator=' ', strip=True)
            
            return text
        except Exception as e:
            logger.error(f"Error extracting content from {url}: {e}")
            return f"Unable to extract content from {url}. Error: {e}"
    
    def extract_insights(self, content: str, num_insights: int = 3) -> List[str]:
        """
        Extract key insights from the given content
        
        Args:
            content (str): Text content to extract insights from
            num_insights (int): Number of insights to extract
        
        Returns:
            List[str]: List of extracted insights
        """
        try:
            # Use quantum crawler's insight extraction
            return self.quantum_crawler.extract_key_insights(content, num_insights)
        except Exception as e:
            logger.error(f"Error extracting insights: {e}")
            return [f"Unable to extract insights. Error: {e}"]
