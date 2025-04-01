"""
Universal Crawler Module

This module provides a universal crawler implementation for extracting content from various sources.
It handles different content types and formats for use in the article generation workflow.
"""

import logging
import requests
import re
import json
from typing import Dict, List, Any, Optional, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from app.crawlers.base import BaseCrawler

logger = logging.getLogger(__name__)

class UniversalCrawler(BaseCrawler):
    """
    Universal Crawler implementation for extracting content from various sources.
    
    This crawler works with different content types and formats, including web pages,
    articles, blog posts, and other text-based content sources. It extracts both the
    main content and relevant metadata for use in article generation.
    """
    
    def __init__(self):
        """Initialize the UniversalCrawler with required configuration"""
        super().__init__()
        self.name = "QuantumUniversalCrawler"
        self.description = "Universal crawler for extracting content from various sources"
        logger.info(f"Initialized {self.name}")
    
    def crawl_analyze_source(self, source: str) -> Dict[str, Any]:
        """
        Analyze a source for content and insights
        
        Args:
            source (str): URL or text content to analyze
        
        Returns:
            Dict[str, Any]: Extracted content and analysis results
        """
        try:
            # Check if source is a URL
            if source.startswith(('http://', 'https://')):
                content = self.extract_content_from_url(source)
            else:
                content = source
            
            # Extract insights
            insights = self.extract_insights(content)
            
            return {
                "source": source,
                "content": content,
                "insights": insights,
                "metadata": {
                    "source_type": "url" if source.startswith(('http://', 'https://')) else "text",
                    "length": len(content)
                }
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
            # Validate URL
            if not self._validate_url(url):
                raise ValueError(f"Invalid URL: {url}")
            
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
            # Split content into sentences
            sentences = re.split(r'[.!?]', content)
            
            # Score sentences based on length and potential importance
            scored_sentences = []
            for sentence in sentences:
                sentence = sentence.strip()
                if not sentence:
                    continue
                
                # Calculate sentence score
                score = len(sentence.split())  # Longer sentences might be more informative
                
                # Bonus points for sentences with potentially important words
                important_words = {
                    'key', 'important', 'critical', 'crucial', 
                    'significant', 'fundamental', 'essential'
                }
                score += sum(1 for word in sentence.lower().split() if word in important_words)
                
                scored_sentences.append((sentence, score))
            
            # Sort by score and return top insights
            return [
                sentence for sentence, _ in 
                sorted(scored_sentences, key=lambda x: x[1], reverse=True)
            ][:num_insights]
        except Exception as e:
            logger.error(f"Error extracting insights: {e}")
            return [f"Unable to extract insights. Error: {e}"]
    
    def _validate_url(self, url: str) -> bool:
        """
        Validate the given URL
        
        Args:
            url (str): URL to validate
        
        Returns:
            bool: True if URL is valid, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception as e:
            logger.error(f"URL validation error for {url}: {e}")
            return False
    
    def _error_response(self, message: str) -> Dict[str, Any]:
        """
        Generate a standard error response
        
        Args:
            message (str): Error message
        
        Returns:
            Dict[str, Any]: Error response dictionary
        """
        return {
            "status": "error",
            "error": message
        }
    
    def crawl(self, url: str) -> Dict[str, Any]:
        """
        Crawl a URL and extract content and metadata.
        
        Args:
            url: URL to crawl
            
        Returns:
            Dictionary containing extracted content and metadata
        """
        try:
            # Validate URL
            if not self._validate_url(url):
                return self._error_response(f"Invalid URL: {url}")
            
            # Fetch content
            response = self.extract_content_from_url(url)
            if not response or response.startswith("Unable to extract content"):
                return self._error_response(f"Failed to extract content from {url}")
            
            # Extract insights
            insights = self.extract_insights(response)
            
            # Build and return the crawled data
            return {
                'status': 'success',
                'url': url,
                'content': response,
                'insights': insights,
                'metadata': {
                    'source_type': 'url',
                    'length': len(response)
                },
                'crawler': self.name
            }
            
        except Exception as e:
            logger.error(f"Error crawling {url}: {str(e)}")
            return self._error_response(f"Error crawling {url}: {str(e)}")
    
    def process_local_file(self, file_path: str, file_type: str = 'text') -> Dict[str, Any]:
        """
        Process local file content.
        
        Args:
            file_path: Path to the local file
            file_type: Type of file (text, html, etc.)
            
        Returns:
            Dictionary containing extracted content and metadata
        """
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract insights
            insights = self.extract_insights(content)
            
            # Build and return the processed data
            return {
                'status': 'success',
                'url': file_path,
                'content_type': file_type,
                'content': content,
                'insights': insights,
                'metadata': {
                    'source_type': 'local_file',
                    'length': len(content)
                },
                'crawler': self.name
            }
            
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {str(e)}")
            return self._error_response(f"Error processing file {file_path}: {str(e)}")
    
    def batch_crawl(self, urls: List[str]) -> List[Dict[str, Any]]:
        """
        Crawl multiple URLs and aggregate results.
        
        Args:
            urls: List of URLs to crawl
            
        Returns:
            List of crawled data dictionaries
        """
        results = []
        
        for url in urls:
            result = self.crawl(url)
            if result.get('status') == 'success':
                results.append(result)
            else:
                # Log the error but continue with other URLs
                logger.warning(f"Failed to crawl {url}: {result.get('message', 'Unknown error')}")
        
        return results
