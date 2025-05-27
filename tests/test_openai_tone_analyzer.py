#!/usr/bin/env python3
"""
Test script for OpenAI Tone Analyzer and Style Samples

This script tests the various features of the OpenAI-based tone analysis system,
including basic tone analysis, style sample generation, and feedback processing.
"""
import sys
import os
import json
import logging
from datetime import datetime

# Add project root to Python path
sys.path.append('/root/socialme/social-me-test-2')

# Setup logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a direct path to our modules to bypass the __init__.py in tone_adaptation that tries to load spaCy
sys.path.append('/root/socialme/social-me-test-2/fastapi_app/app/tone_adaptation')

# Try direct imports of specific modules
try:
    # Direct import of the modules to avoid dependencies in __init__.py
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "openai_tone_analyzer", 
        "/root/socialme/social-me-test-2/fastapi_app/app/tone_adaptation/openai_tone_analyzer.py"
    )
    openai_tone_analyzer = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(openai_tone_analyzer)
    OpenAIToneAnalyzer = openai_tone_analyzer.OpenAIToneAnalyzer
    
    # For hybrid adapter
    spec = importlib.util.spec_from_file_location(
        "hybrid_tone_adapter", 
        "/root/socialme/social-me-test-2/fastapi_app/app/tone_adaptation/hybrid_tone_adapter.py"
    )
    hybrid_tone_adapter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(hybrid_tone_adapter)
    HybridToneAdapter = hybrid_tone_adapter.HybridToneAdapter
    
    logger.info("Successfully imported tone analyzers with direct module loading")
except Exception as e:
    logger.error(f"Failed to import tone analyzers: {e}")
    sys.exit(1)

def test_direct_text_analysis():
    """Test basic tone analysis with direct text input"""
    logger.info("Testing direct text analysis...")
    analyzer = OpenAIToneAnalyzer()
    
    # Sample formal text
    sample_text = """
    The efficacy of machine learning algorithms in natural language processing 
    has demonstrated remarkable progress in recent years. This advancement has 
    been facilitated by developments in neural network architectures and the 
    availability of substantial training datasets. Nevertheless, challenges 
    persist in areas such as contextual understanding and semantic reasoning.
    """
    
    result = analyzer.analyze_tone(sample_text=sample_text)
    logger.info(f"Analysis status: {result.get('status')}")
    
    # Print key metrics from the analysis
    if result.get('status') == 'success':
        logger.info("Analysis returned successfully")
        
        # Print formal metrics if available
        if 'FORMALITY_ANALYSIS' in result:
            formality = result['FORMALITY_ANALYSIS']
            logger.info(f"Formality score: {formality.get('overall_formality_score')}")
            logger.info(f"Formal indicators: {formality.get('formal_indicators', [])[:3]}")
        
        # Print reasoning patterns if available
        if 'REASONING_PATTERNS' in result:
            reasoning = result['REASONING_PATTERNS']
            logger.info(f"Primary reasoning style: {reasoning.get('primary_reasoning_style')}")
    
    return result

def test_url_analysis():
    """Test tone analysis with URL input"""
    logger.info("Testing URL-based tone analysis...")
    analyzer = OpenAIToneAnalyzer()
    
    # Sample URL with technical content
    url = "https://en.wikipedia.org/wiki/Natural_language_processing"
    
    result = analyzer.analyze_tone(url=url)
    logger.info(f"URL analysis status: {result.get('status')}")
    
    if result.get('status') == 'success':
        logger.info("URL analysis returned successfully")
        
        # Print domain classification if available
        if 'DOMAIN_CLASSIFICATION' in result:
            domain = result['DOMAIN_CLASSIFICATION']
            logger.info(f"Primary domain: {domain.get('primary_domain')}")
            logger.info(f"Confidence: {domain.get('confidence_score')}")
    
    return result

def test_style_samples_generation():
    """Test style samples generation"""
    logger.info("Testing style samples generation...")
    analyzer = OpenAIToneAnalyzer()
    
    # Sample casual text
    sample_text = """
    Hey, I've been thinking about how tech is changing the way we interact with each other.
    It's crazy how social media has completely transformed the way people communicate and share their lives.
    Some of it is awesome - like being able to keep in touch with friends across the world.
    But there's definitely a downside too, with privacy concerns and the weird social pressure it creates.
    What do you think? Is technology making our social lives better or worse overall?
    """
    
    result = analyzer.generate_style_samples(
        sample_text=sample_text,
        num_samples=2,
        target_length=150
    )
    
    logger.info(f"Style samples generation status: {result.get('status')}")
    
    if result.get('status') == 'success':
        logger.info("Style samples generated successfully")
        
        # Print style analysis if available
        if 'style_analysis' in result:
            style = result['style_analysis']
            logger.info(f"Key characteristics: {style.get('key_characteristics', [])}")
            logger.info(f"Distinctive patterns: {style.get('distinctive_patterns', [])}")
        
        # Print samples
        if 'samples' in result and len(result['samples']) > 0:
            logger.info(f"Generated {len(result['samples'])} samples")
            for i, sample in enumerate(result['samples']):
                logger.info(f"Sample {i+1} topic: {sample.get('topic')}")
                sample_text = sample.get('sample_text', '')
                logger.info(f"Sample {i+1} preview: {sample_text[:100]}...")
        
    return result

def test_hybrid_adapter():
    """Test the hybrid adapter functionality"""
    logger.info("Testing hybrid adapter...")
    adapter = HybridToneAdapter(force_openai=True)
    
    # Technical text for analysis
    sample_text = """
    Python's dynamic typing and built-in data structures make it an ideal language for rapid application development.
    The syntax emphasizes readability, making it easier to maintain. Exception handling is robust, and the language
    supports modules and packages, encouraging program modularity and code reuse.
    """
    
    result = adapter.analyze_tone(sample_text=sample_text)
    logger.info(f"Hybrid adapter analysis status: {result.get('status')}")
    
    if result.get('status') == 'success':
        logger.info("Hybrid adapter analysis returned successfully")
    
    # Now test style samples generation through the hybrid adapter
    samples_result = adapter.generate_style_samples(
        sample_text=sample_text,
        num_samples=2
    )
    
    logger.info(f"Hybrid adapter style samples status: {samples_result.get('status')}")
    
    return {
        "analysis": result,
        "samples": samples_result
    }

def simulate_feedback_workflow():
    """Simulate a complete feedback workflow with regeneration"""
    logger.info("Simulating complete feedback workflow...")
    analyzer = OpenAIToneAnalyzer()
    
    # Business text for analysis
    sample_text = """
    Our Q3 results exceeded expectations, with revenue growth of 15% year-over-year.
    The new product line contributed significantly to this performance, accounting for 
    approximately 30% of new sales. Customer acquisition costs decreased by 12%, while
    retention rates improved to 85%. Looking ahead, we're forecasting continued growth
    in Q4, with expansion into two new market segments planned for early next year.
    """
    
    # Step 1: Generate initial samples
    logger.info("Step 1: Generate initial samples")
    initial_result = analyzer.generate_style_samples(
        sample_text=sample_text,
        num_samples=3
    )
    
    if initial_result.get('status') != 'success' or 'samples' not in initial_result:
        logger.error("Failed to generate initial samples")
        return None
    
    # Step 2: Simulate upvoting sample #1
    logger.info("Step 2: Simulating upvote feedback")
    feedback = [
        {
            "sample_id": initial_result['samples'][0]['id'],
            "rating": "upvote",
            "comments": "I like this style, it sounds professional"
        }
    ]
    
    # Step 3: Simulate downvoting sample #2 and requesting regeneration
    logger.info("Step 3: Simulating downvote + regeneration feedback")
    
    # Add the feedback to our list
    feedback.append({
        "sample_id": initial_result['samples'][1]['id'],
        "rating": "downvote",
        "comments": "Too informal, not my style"
    })
    
    # Request regeneration
    regenerated_result = analyzer.regenerate_style_samples(
        previous_samples=initial_result,
        feedback=feedback,
        num_samples=2
    )
    
    if regenerated_result.get('status') == 'success':
        logger.info("Successfully regenerated samples based on feedback")
        
        # Show changes in style characteristics if available
        if 'style_analysis' in regenerated_result:
            style = regenerated_result['style_analysis']
            logger.info(f"Adjusted characteristics: {style.get('adjusted_characteristics', [])}")
            logger.info(f"Avoided patterns: {style.get('avoided_patterns', [])}")
    
    return {
        "initial_samples": initial_result,
        "feedback": feedback,
        "regenerated_samples": regenerated_result
    }

def save_test_results(results):
    """Save test results to a file for review"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/root/socialme/social-me-test-2/tests/results/openai_tone_test_{timestamp}.json"
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    logger.info(f"Test results saved to {filename}")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("OpenAI Tone Analyzer and Style Samples Test Suite")
    print("="*80 + "\n")
    
    all_results = {}
    
    try:
        # Run basic tone analysis test
        print("\n1. Testing Basic Tone Analysis")
        print("-"*40)
        all_results['direct_text'] = test_direct_text_analysis()
        
        # Run URL analysis test
        print("\n2. Testing URL Analysis")
        print("-"*40)
        all_results['url_analysis'] = test_url_analysis()
        
        # Run style samples generation test
        print("\n3. Testing Style Samples Generation")
        print("-"*40)
        all_results['style_samples'] = test_style_samples_generation()
        
        # Run hybrid adapter test
        print("\n4. Testing Hybrid Adapter")
        print("-"*40)
        all_results['hybrid_adapter'] = test_hybrid_adapter()
        
        # Run feedback workflow simulation
        print("\n5. Simulating Complete Feedback Workflow")
        print("-"*40)
        all_results['feedback_workflow'] = simulate_feedback_workflow()
        
        # Save test results for detailed review
        save_test_results(all_results)
        
        print("\n" + "="*80)
        print("All tests completed successfully!")
        print("="*80 + "\n")
        
    except Exception as e:
        import traceback
        logger.error(f"Test failed with error: {e}")
        logger.error(traceback.format_exc())
        print(f"\nERROR: {e}")
