#!/usr/bin/env python3
"""
Quick Test for Advanced Tone Adaptation System
"""

import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("quick_tone_test")

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def quick_test():
    """Perform a quick test of the Advanced Tone Adaptation System"""
    try:
        # Import components
        from app.tone_adaptation import AdvancedToneAdapter
        from app.neural_tone_mapper import NeuralToneMapper
        from app.advanced_article_generator import generate_advanced_article

        # Check Claude API key
        if not os.getenv("CLAUDE_API_KEY"):
            logger.warning("CLAUDE_API_KEY not set. Some tests will be limited.")

        # Prepare test data
        sample_text = """
        Quantum computing represents a paradigm shift in computational capabilities. 
        By leveraging quantum mechanical phenomena such as superposition and entanglement, 
        these advanced systems can solve complex problems exponentially faster than classical computers. 
        The potential applications span cryptography, drug discovery, climate modeling, and artificial intelligence.
        """

        # Initialize components
        tone_mapper = NeuralToneMapper()
        
        # Analyze tone
        tone_analysis = tone_mapper.analyze_text(sample_text)
        logger.info("Tone Analysis Results:")
        logger.info(f"Thought Patterns: {tone_analysis.get('thought_patterns', {})}")
        logger.info(f"Reasoning Style: {tone_analysis.get('reasoning_style', {})}")

        # Prepare source material
        source_material = [{
            "type": "text",
            "text": sample_text,
            "title": "Quantum Computing Overview",
            "content": sample_text,
            "relevance_score": 0.95
        }]

        # Try article generation if API key is available
        if os.getenv("CLAUDE_API_KEY"):
            article_result = generate_advanced_article(
                topic="Quantum Computing Advancements",
                tone_analysis=tone_analysis,
                source_material=source_material
            )
            
            if article_result and 'article' in article_result:
                article = article_result['article']
                logger.info("\nGenerated Article:")
                logger.info(f"Title: {article.get('title', 'N/A')}")
                logger.info(f"Introduction: {article.get('introduction', 'N/A')[:200]}...")
            else:
                logger.warning("Article generation failed")
        
        logger.info("\n✅ Quick test completed successfully!")

    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    quick_test()
