"""
Base Crawler Implementation

This module defines the base interface for all crawler implementations in SocialMe.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseCrawler(ABC):
    """
    Abstract base class for all crawlers in the SocialMe application.
    
    This class defines the standard interface that all crawler implementations
    must follow to ensure consistent behavior across the application.
    """
    
    def __init__(self, topic: Optional[str] = None, max_pages_per_domain: int = 5):
        """
        Initialize the crawler with optional topic and page limit.
        
        Args:
            topic: Optional topic to focus the crawler on relevant content
            max_pages_per_domain: Maximum number of pages to crawl per domain
        """
        self.topic = topic
        self.max_pages_per_domain = max_pages_per_domain
    
    @abstractmethod
    def extract_content_from_url(self, url: str) -> str:
        """
        Extract text content from a given URL.
        
        Args:
            url: The URL to extract content from
            
        Returns:
            The extracted text content
        """
        pass
    
    @abstractmethod
    def extract_insights(self, content: str) -> List[str]:
        """
        Extract key insights from the given content.
        
        Args:
            content: The text content to analyze
            
        Returns:
            List of extracted insights as strings
        """
        pass
    
    @abstractmethod
    def crawl_analyze_source(self, url: str) -> Dict[str, Any]:
        """
        Crawl a source URL and analyze its content.
        
        Args:
            url: The URL to crawl and analyze
            
        Returns:
            Dictionary containing the results of the crawl and analysis
        """
        pass
