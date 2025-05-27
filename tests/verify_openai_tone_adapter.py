#!/usr/bin/env python3
"""
Verification script for the OpenAI Tone Analysis implementation
This directly tests the process_sample_feedback method functionality
"""

import sys
import os
import json
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("openai_verify")

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.join(project_root, 'fastapi_app'))

try:
    # Direct import by loading module from file
    import importlib.util
    
    analyzer_path = os.path.join(project_root, 'fastapi_app/app/tone_adaptation/openai_tone_analyzer.py')
    spec = importlib.util.spec_from_file_location("openai_tone_analyzer", analyzer_path)
    openai_tone_analyzer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(openai_tone_analyzer)
    OpenAIToneAnalyzer = openai_tone_analyzer.OpenAIToneAnalyzer
    
    logger.info("Successfully imported OpenAIToneAnalyzer using direct file load")
except Exception as e:
    logger.error(f"Import error: {e}")
    sys.exit(1)

def verify_process_sample_feedback():
    """Verify that the process_sample_feedback method works correctly"""
    
    # Initialize the analyzer
    analyzer = OpenAIToneAnalyzer()
    
    # Check if the method exists
    if not hasattr(analyzer, 'process_sample_feedback'):
        logger.error("Method 'process_sample_feedback' does not exist in OpenAIToneAnalyzer")
        # Print dir of the analyzer to see available methods
        logger.info(f"Available methods: {[m for m in dir(analyzer) if not m.startswith('_')]}")
        return False
    
    # Test simple feedback (no regeneration)
    logger.info("Testing feedback without regeneration...")
    try:
        response = analyzer.process_sample_feedback(
            sample_id=1,
            rating="upvote",
            comments="Great sample!"
        )
        logger.info(f"Response status: {response.get('status')}")
        logger.info(f"Response message: {response.get('message')}")
        
        if response.get('status') == 'success':
            logger.info("✅ Basic feedback test passed")
        else:
            logger.error("❌ Basic feedback test failed")
            return False
    except Exception as e:
        logger.error(f"Error testing feedback: {e}")
        return False
    
    # Save results
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    with open(os.path.join(results_dir, "verify_openai_feedback.json"), "w") as f:
        json.dump({
            "status": "success",
            "message": "OpenAIToneAnalyzer.process_sample_feedback verified",
            "response": response
        }, f, indent=2)
    
    logger.info("✅ Verification completed successfully")
    return True

if __name__ == "__main__":
    logger.info("=== Verifying OpenAI Tone Analyzer Implementation ===")
    if verify_process_sample_feedback():
        logger.info("🎉 All verification tests passed")
        sys.exit(0)
    else:
        logger.error("❌ Verification failed")
        sys.exit(1)
