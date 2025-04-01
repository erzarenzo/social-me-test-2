#!/usr/bin/env python3
"""
Test script for the Neural Tone Mapper functionality.
This script directly tests the NeuralToneMapper class without requiring the web interface.
"""

import logging
import json
from app.neural_tone_mapper import NeuralToneMapper

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_neural_tone_mapper():
    """Test the Neural Tone Mapper with a sample text."""
    sample_text = """
    The integration of artificial intelligence in content creation represents a significant 
    paradigm shift in how we approach digital marketing. While traditional methods relied 
    heavily on human intuition and experience, AI-driven approaches leverage data analytics 
    and pattern recognition to optimize content for specific audiences. This transformation 
    is not merely technological but fundamentally alters the creative process itself.
    
    However, we must acknowledge that AI tools are supplements to human creativity, not 
    replacements. The most effective content strategies combine algorithmic precision with 
    human empathy and cultural understanding - elements that remain challenging for machines 
    to fully replicate. As we move forward, the balance between automation and authentic 
    human expression will define successful digital communication.
    """
    
    logger.info("Initializing Neural Tone Mapper...")
    mapper = NeuralToneMapper()
    
    logger.info("Analyzing sample text...")
    analysis_result = mapper.analyze_text(sample_text)
    
    logger.info("Analysis complete. Results:")
    print(json.dumps(analysis_result, indent=2))
    
    return analysis_result

if __name__ == "__main__":
    logger.info("Starting Neural Tone Mapper test")
    test_result = test_neural_tone_mapper()
    logger.info("Test completed successfully")
