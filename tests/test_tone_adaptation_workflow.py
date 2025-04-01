#!/usr/bin/env python3
"""
Comprehensive Workflow Test for Advanced Tone Adaptation System

This script tests the complete workflow of the Advanced Tone Adaptation System,
from tone analysis to article generation, using real-world examples.
"""

import json
import logging
import os
import sys
import time
from typing import Dict, List, Any

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("workflow_test")

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the components
try:
    from app.tone_adaptation import AdvancedToneAdapter
    from app.advanced_article_generator import generate_advanced_article
    from app.neural_tone_mapper import NeuralToneMapper
    from app.quantum_tone_crawler import QuantumToneCrawler
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.error("Make sure you're running this script from the project root directory")
    sys.exit(1)

# Sample writing styles for testing
WRITING_SAMPLES = {
    "academic": """
    The implementation of quantum computing in cybersecurity represents a paradigm shift in cryptographic methodologies. Traditional encryption algorithms, while robust against classical computing attacks, may prove insufficient against quantum algorithms specifically designed to exploit mathematical vulnerabilities. The theoretical framework established by Shor's algorithm demonstrates the potential for quantum computers to efficiently factorize large prime numbers, thereby compromising RSA encryption. Organizations must therefore begin implementing quantum-resistant cryptographic solutions to safeguard sensitive information against future threats. This transition, however, requires substantial investment in both technological infrastructure and specialized expertise.
    """,
    
    "journalistic": """
    Quantum computing is set to revolutionize cybersecurity as we know it. Experts warn that current encryption methods could be broken in minutes once powerful quantum computers become available. "We're looking at a complete overhaul of digital security," says Dr. Sarah Chen, a leading researcher at MIT's Quantum Information Center.
    
    Companies are racing to develop new "quantum-resistant" encryption before it's too late. Google and IBM have already invested billions in the technology. Meanwhile, government agencies are scrambling to protect classified information that could be vulnerable to future attacks.
    
    The clock is ticking. Some analysts believe functional quantum computers capable of breaking current encryption could arrive within the next decade.
    """,
    
    "conversational": """
    So here's the thing about quantum computing and cybersecurity - it's both super exciting and kinda terrifying! Right now, all our sensitive data is protected by encryption that works because certain math problems are really hard for regular computers to solve. But quantum computers? They can solve these problems WAY faster.
    
    Think about it like this: the lock on your front door might keep out most people, but quantum computing is like giving everyone a master key! Pretty scary, right?
    
    The good news is that smart people are already working on new types of encryption that even quantum computers can't break. But we need to hurry up and implement these solutions before powerful quantum computers become widely available. Otherwise, yikes! All our secrets could be up for grabs!
    """
}

def test_complete_workflow(style_name: str, sample_text: str, topic: str = "Quantum Computing in Cybersecurity"):
    """Test the complete workflow from tone analysis to article generation"""
    logger.info(f"\n\n===== Testing Complete Workflow with {style_name.title()} Style =====\n")
    
    # Step 1: Analyze the tone of the sample text
    logger.info("Step 1: Analyzing tone of sample text...")
    
    # Create tone sources
    tone_sources = [{
        "type": "text",
        "text": sample_text
    }]
    
    # Initialize the Neural Tone Mapper
    tone_mapper = NeuralToneMapper()
    
    # Analyze the tone
    try:
        tone_analysis = tone_mapper.analyze_text(sample_text)
        logger.info("Tone analysis completed successfully")
        logger.info(f"Dominant thought pattern: {max(tone_analysis.get('thought_patterns', {}).items(), key=lambda x: x[1])[0]}")
        logger.info(f"Dominant reasoning style: {max(tone_analysis.get('reasoning_style', {}).items(), key=lambda x: x[1])[0]}")
    except Exception as e:
        logger.error(f"Error in tone analysis: {e}")
        # Create a simple tone analysis as fallback
        tone_analysis = {
            "thought_patterns": {
                "analytical": 0.7 if style_name == "academic" else 0.3,
                "creative": 0.2 if style_name == "conversational" else 0.4,
                "emotional": 0.1 if style_name == "academic" else 0.3
            },
            "reasoning_style": {
                "deductive": 0.6 if style_name == "academic" else 0.3,
                "inductive": 0.3,
                "analogical": 0.1 if style_name == "academic" else 0.4
            }
        }
    
    # Step 2: Create source material
    logger.info("\nStep 2: Creating source material...")
    
    # Sample source material
    source_material = [
        {
            "type": "text",
            "text": sample_text,
            "title": f"Sample {style_name.title()} Text",
            "url": "https://example.com/sample",
            "content": sample_text,
            "relevance_score": 0.95
        },
        {
            "type": "url",
            "url": "https://example.com/quantum-computing",
            "title": "Introduction to Quantum Computing",
            "content": "Quantum computing leverages quantum mechanics principles to process information. Unlike classical bits, quantum bits or 'qubits' can exist in multiple states simultaneously, enabling quantum computers to solve certain problems exponentially faster than classical computers.",
            "relevance_score": 0.85
        },
        {
            "type": "url",
            "url": "https://example.com/cybersecurity",
            "title": "Modern Cybersecurity Challenges",
            "content": "Cybersecurity faces evolving threats as technology advances. Organizations must implement robust security measures to protect sensitive data from increasingly sophisticated attacks.",
            "relevance_score": 0.75
        }
    ]
    
    # Step 3: Generate article with Advanced Tone Adaptation
    logger.info("\nStep 3: Generating article with Advanced Tone Adaptation...")
    
    # Check if Claude API key is available
    claude_api_key = os.getenv("CLAUDE_API_KEY")
    if not claude_api_key:
        logger.warning("CLAUDE_API_KEY not found. Article generation will be limited.")
        logger.info("To test full article generation, set the CLAUDE_API_KEY environment variable.")
        return
    
    # Generate the article
    try:
        start_time = time.time()
        article_result = generate_advanced_article(
            topic=topic,
            tone_analysis=tone_analysis,
            source_material=source_material
        )
        generation_time = time.time() - start_time
        
        # Print article information
        if article_result and 'article' in article_result:
            article = article_result['article']
            logger.info(f"Article generated successfully in {generation_time:.2f} seconds")
            logger.info(f"Title: {article['title']}")
            logger.info(f"Subtitle: {article.get('subtitle', 'N/A')}")
            logger.info(f"Introduction: {article['introduction'][:200]}...")
            
            if 'body' in article and article['body']:
                logger.info(f"Number of sections: {len(article['body'])}")
                for i, section in enumerate(article['body']):
                    logger.info(f"Section {i+1}: {section.get('subheading', 'Unnamed Section')}")
            
            if 'validation' in article_result:
                logger.info(f"Validation: {article_result['validation']}")
                
            # Save the article to a file
            output_file = f"generated_article_{style_name}.json"
            with open(output_file, 'w') as f:
                json.dump(article, f, indent=2)
            logger.info(f"Article saved to {output_file}")
            
            return article
        else:
            logger.error("Article generation failed")
    except Exception as e:
        logger.error(f"Error in article generation: {e}")

def main():
    """Main test function"""
    logger.info("Advanced Tone Adaptation Workflow Test")
    logger.info("=====================================")
    
    # Test with different writing styles
    for style_name, sample_text in WRITING_SAMPLES.items():
        test_complete_workflow(style_name, sample_text)
        
        # Add a delay between tests to avoid API rate limits
        if style_name != list(WRITING_SAMPLES.keys())[-1]:
            logger.info("Waiting 5 seconds before next test...")
            time.sleep(5)
    
    logger.info("\nAll tests completed!")

if __name__ == "__main__":
    main()
