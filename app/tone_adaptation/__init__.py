"""
Tone Adaptation Module Initialization

This module provides a flexible and robust initialization mechanism
for tone adaptation components, with dynamic import and fallback strategies.
"""

import logging
import importlib
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def _lazy_import(module_name, class_name):
    """
    Dynamically import a class with robust error handling
    
    Args:
        module_name (str): Full module path
        class_name (str): Name of the class to import
    
    Returns:
        Imported class or fallback class
    """
    try:
        module = importlib.import_module(module_name)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        logger.warning(f"Could not import {module_name}.{class_name}: {e}")
        return None

class FallbackAdvancedToneAdapter:
    """
    Fallback Tone Adapter for scenarios where advanced NLP libraries are unavailable
    """
    def __init__(self):
        logger.warning("Using Fallback Advanced Tone Adapter")
    
    def process_tone_sources(self, sources):
        """
        Provide basic tone analysis metrics
        
        Args:
            sources (List[Dict]): List of source content
        
        Returns:
            Dict with basic tone metrics
        """
        return {
            'formality': 0.5,
            'complexity': 0.5,
            'sentiment': 0.0
        }

def get_advanced_tone_adapter():
    """
    Dynamically retrieve the Advanced Tone Adapter with fallback
    
    Returns:
        AdvancedToneAdapter or FallbackAdvancedToneAdapter
    """
    # Try to import the advanced tone adapter
    AdvancedToneAdapter = _lazy_import(
        'app.tone_adaptation.tone_adapter', 
        'AdvancedToneAdapter'
    )
    
    # Return the imported class or fallback
    if AdvancedToneAdapter:
        try:
            return AdvancedToneAdapter()
        except Exception as e:
            logger.error(f"Failed to initialize AdvancedToneAdapter: {e}")
    
    return FallbackAdvancedToneAdapter()

# Dynamically check and warn about missing dependencies
def _check_dependencies():
    """
    Check and log availability of tone adaptation dependencies
    """
    dependencies = [
        ('spacy', 'Advanced NLP processing'),
        ('numpy', 'Numerical computations'),
    ]
    
    for module_name, description in dependencies:
        try:
            importlib.import_module(module_name)
        except ImportError:
            logger.warning(f"{description} library '{module_name}' not found. Some advanced features will be limited.")

# Run dependency check on module import
_check_dependencies()

# Expose key components
__all__ = [
    'get_advanced_tone_adapter',
    'FallbackAdvancedToneAdapter'
]
