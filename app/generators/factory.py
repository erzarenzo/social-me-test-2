"""
Article Generator Factory

This module provides a factory pattern for article generators, allowing
the application to easily switch between different article generator
implementations while maintaining a consistent interface.
"""

import logging
import os
from typing import Dict, List, Any, Optional, Type, Union

logger = logging.getLogger(__name__)

class ArticleGeneratorFactory:
    """
    Factory for creating article generator instances.
    
    This factory provides a way to get the appropriate article generator
    implementation based on configuration or availability of dependencies.
    """
    
    @staticmethod
    def get_article_generator(generator_type: str = "standard", api_key: Optional[str] = None) -> Any:
        """
        Get an article generator instance based on type.
        
        Args:
            generator_type: Type of generator to use ("standard", "advanced", or "auto")
            api_key: Optional API key to use with the generator
            
        Returns:
            An article generator instance
        """
        try:
            # Use environment variable if no API key provided
            if not api_key:
                api_key = os.environ.get('ANTHROPIC_API_KEY') or os.environ.get('CLAUDE_API_KEY')
            
            if generator_type == "auto":
                # Auto-detect based on available dependencies and API key
                if not api_key:
                    logger.warning("No API key available, falling back to standard generator")
                    generator_type = "standard"
                else:
                    try:
                        import anthropic
                        generator_type = "advanced"
                    except ImportError:
                        logger.warning("Anthropic library not available, using standard generator")
                        generator_type = "standard"
            
            if generator_type == "advanced":
                # Import here to prevent circular imports
                try:
                    from app.advanced_article_generator import ArticleGenerator as AdvancedArticleGenerator
                    logger.info("Using advanced article generator")
                    return AdvancedArticleGenerator(api_key=api_key)
                except ImportError:
                    logger.warning("Advanced article generator not available, falling back to standard")
                    generator_type = "standard"
            
            # Default to standard generator
            if generator_type == "standard":
                from app.generators.article import ArticleGenerator
                logger.info("Using standard article generator")
                return ArticleGenerator(api_key=api_key)
            
            # If we somehow get here with an unknown type
            logger.error(f"Unknown generator type: {generator_type}")
            from app.generators.article import ArticleGenerator
            return ArticleGenerator(api_key=api_key)
            
        except Exception as e:
            logger.error(f"Error creating article generator: {str(e)}")
            # Fallback to standard generator in case of any errors
            from app.generators.article import ArticleGenerator
            return ArticleGenerator(api_key=api_key)

# Convenience function to get an article generator
def get_article_generator(generator_type: str = "auto", api_key: Optional[str] = None) -> Any:
    """
    Convenience function to get an article generator instance.
    
    Args:
        generator_type: Type of generator to use ("standard", "advanced", or "auto")
        api_key: Optional API key to use with the generator
        
    Returns:
        An article generator instance
    """
    return ArticleGeneratorFactory.get_article_generator(generator_type, api_key)
