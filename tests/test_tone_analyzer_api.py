#!/usr/bin/env python3
"""
Test script to verify the Neural Tone Mapper API endpoint is working correctly.
This script sends a POST request to the /analyze-content endpoint with sample text.
"""

import requests
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_tone_analyzer_api():
    """Test the tone analyzer API endpoint with a sample text."""
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
    
    logger.info("Sending request to tone analyzer API...")
    
    url = "http://localhost:8003/analyze-content"
    data = {"content": sample_text, "type": "text"}
    
    try:
        response = requests.post(url, data=data)
        logger.info(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info("Analysis complete. Results:")
            print(json.dumps(result, indent=2))
            return result
        else:
            logger.error(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return None

if __name__ == "__main__":
    logger.info("Starting tone analyzer API test")
    test_result = test_tone_analyzer_api()
    logger.info("Test completed")
