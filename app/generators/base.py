"""
Base Generator Implementation

This module defines the base interface for all content generator implementations in SocialMe.
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional


class BaseGenerator(ABC):
    """
    Abstract base class for all content generators in the SocialMe application.
    
    This class defines the standard interface that all generator implementations
    must follow to ensure consistent behavior across the application.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the generator with optional API key for LLM services.
        
        Args:
            api_key: Optional API key for LLM services
        """
        self.api_key = api_key
    
    @abstractmethod
    def generate_article(self, 
                        topic: str, 
                        style_profile: Dict[str, Any],
                        source_material: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate an article based on the given parameters.
        
        Args:
            topic: The main topic of the article
            style_profile: Dictionary containing style and tone parameters
            source_material: List of dictionaries containing source content and metadata
            
        Returns:
            Dictionary containing the generated article and metadata
        """
        pass
    
    @abstractmethod
    def format_output(self, raw_content: str) -> Dict[str, Any]:
        """
        Format the raw generated content into structured output.
        
        Args:
            raw_content: The raw generated content
            
        Returns:
            Dictionary containing the formatted content and metadata
        """
        pass
