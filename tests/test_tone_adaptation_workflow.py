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

# Add the fastapi_app to the path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(project_root)

# Add fastapi_app to the sys.path
sys.path.insert(0, os.path.join(project_root, 'fastapi_app'))

# Direct approach to import the modules
try:
    # Import OpenAI modules directly
    import importlib
    import importlib.util
    
    # First ensure any previously imported modules are reloaded
    if 'app.tone_adaptation.openai_tone_analyzer' in sys.modules:
        importlib.reload(sys.modules['app.tone_adaptation.openai_tone_analyzer'])
    
    # Standard import
    from app.tone_adaptation.openai_tone_analyzer import OpenAIToneAnalyzer
    
    # Also try to import the hybrid adapter
    if 'app.tone_adaptation.hybrid_tone_adapter' in sys.modules:
        importlib.reload(sys.modules['app.tone_adaptation.hybrid_tone_adapter'])
        
    from app.tone_adaptation.hybrid_tone_adapter import HybridToneAdapter
    
    logger.info("Successfully imported OpenAI tone analyzer modules")
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
    
    # Step 1: Analyze the tone of the sample text using OpenAI
    logger.info("Step 1: Analyzing tone of sample text with OpenAI...")
    
    # Initialize the OpenAI Tone Analyzer
    try:
        analyzer = OpenAIToneAnalyzer()
        logger.info("OpenAI tone analyzer initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing OpenAI tone analyzer: {e}")
        sys.exit(1)
    
    # Analyze the tone
    try:
        tone_analysis = analyzer.analyze_tone(sample_text=sample_text)
        
        if tone_analysis.get("status") == "success":
            logger.info("Tone analysis completed successfully")
            
            # Log key aspects of the analysis
            analysis_data = tone_analysis.get("analysis", {})
            logger.info(f"Formality score: {analysis_data.get('formality_score', 'N/A')}")
            logger.info(f"Primary style: {analysis_data.get('primary_style', 'N/A')}")
            logger.info(f"Dominant patterns: {', '.join(analysis_data.get('dominant_patterns', ['N/A'])[:3])}")
            
            # Step 2: Generate style samples based on the analysis
            logger.info("\nStep 2: Generating style samples...")
            style_samples = analyzer.generate_style_samples(sample_text, num_samples=2, target_length=150)
            
            if style_samples.get("status") == "success":
                logger.info("Style samples generated successfully")
                samples = style_samples.get("samples", [])
                
                for i, sample in enumerate(samples, 1):
                    logger.info(f"Sample {i} (Topic: {sample.get('topic', 'Unknown')})")
                    logger.info(f"Preview: {sample.get('sample_text', '')[:50]}...\n")
                
                # Step 3: Simulate feedback on style
                logger.info("\nStep 3: Simulating feedback on style samples...")
                feedback_response = analyzer.process_sample_feedback(
                    sample_id=1,  # First sample
                    rating="upvote",
                    comments="This style captures my writing well"
                )
                
                logger.info(f"Feedback status: {feedback_response.get('status', 'error')}")
                logger.info(f"Feedback message: {feedback_response.get('message', 'Unknown')}")
                
                # Return the analysis result for further processing
                return tone_analysis
            else:
                logger.error(f"Error generating style samples: {style_samples.get('message', 'Unknown error')}")
        else:
            logger.error(f"Error in tone analysis: {tone_analysis.get('message', 'Unknown error')}")
    except Exception as e:
        logger.error(f"Error during analysis: {e}")
    
    # Create a simple analysis as fallback
    fallback_analysis = {
        "status": "error",
        "analysis": {
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
    
    # Create results directory
    results_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(results_dir, exist_ok=True)
    
    logger.info("\n" + "=" * 80)
    logger.info("OpenAI Tone Analysis and Style Samples Integration Test")
    logger.info("=" * 80 + "\n")
    
    # Test across different writing styles
    all_results = []
    for style_name, sample_text in WRITING_SAMPLES.items():
        try:
            # Run the complete workflow test
            logger.info(f"Testing with {style_name.title()} writing style")
            analysis = test_complete_workflow(style_name, sample_text)
            all_results.append({
                "style_name": style_name,
                "status": "success" if analysis and analysis.get("status") == "success" else "error",
                "analysis": analysis
            })
        except Exception as e:
            logger.error(f"Error in workflow for {style_name} style: {e}")
            all_results.append({
                "style_name": style_name,
                "status": "error",
                "error": str(e)
            })
        logger.info("\n" + "-" * 80 + "\n")
    
    # Save combined results
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    results_file = os.path.join(results_dir, f"openai_tone_workflow_test_{timestamp}.json")
    
    with open(results_file, "w") as f:
        json.dump({
            "timestamp": timestamp,
            "test_name": "OpenAI Tone Analysis and Style Samples Integration Test",
            "results": all_results
        }, f, indent=2)
        
    logger.info(f"Test results saved to {results_file}")
    
    # Success rate
    success_count = sum(1 for r in all_results if r.get("status") == "success")
    total_count = len(all_results)
    success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
    
    logger.info("\n" + "=" * 80)
    logger.info(f"Test Results: {success_count}/{total_count} tests passed ({success_rate:.1f}%)")
    logger.info("=" * 80 + "\n")
    
    if success_count == total_count:
        logger.info("All tests completed successfully!")
    else:
        logger.info("Some tests failed. See logs above for details.")

if __name__ == "__main__":
    main()
