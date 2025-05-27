"""
Test script for QuantumUniversalCrawler implementation
"""
import sys
import os
import logging
import json

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("test_crawler")

try:
    from fastapi_app.services.crawler import QuantumUniversalCrawler
    
    # Test URLs - using the same ones mentioned in memory
    test_urls = [
        "https://en.wikipedia.org/wiki/Artificial_intelligence_in_healthcare",
        "https://www.ibm.com/topics/artificial-intelligence-healthcare",
        "https://www.nvidia.com/en-us/healthcare/"
    ]
    
    logger.info(f"Testing QuantumUniversalCrawler with {len(test_urls)} URLs")
    
    # Initialize crawler
    crawler = QuantumUniversalCrawler(confidence_threshold=0.1)
    
    # Extract content
    results = crawler.extract_from_urls(test_urls)
    
    # Print results summary
    print(f"\n=== EXTRACTION RESULTS ===")
    print(f"Total word count: {results['total_word_count']}")
    print(f"Successful extractions: {results['successful_extractions']}")
    print(f"Failed extractions: {results['failed_extractions']}")
    print(f"Target achieved: {'Yes' if results['total_word_count'] >= 12000 else 'No'}")
    
    # Print details for each source
    for i, source in enumerate(results['processed_sources']):
        print(f"\nSource {i+1}: {source['url']}")
        print(f"Word count: {source['word_count']}")
        print(f"Extraction method: {source['metadata']['extraction_method']}")
        print(f"Confidence: {source['metadata']['confidence']:.2f}")
        print(f"First 150 chars: {source['content'][:150]}...")
    
    # Save results to file for inspection
    with open('crawler_test_results.json', 'w') as f:
        json.dump({
            "summary": {
                "total_word_count": results['total_word_count'],
                "successful_extractions": results['successful_extractions'],
                "failed_extractions": results['failed_extractions']
            },
            "sources": [
                {
                    "url": s["url"],
                    "word_count": s["word_count"],
                    "metadata": s["metadata"],
                    "content_preview": s["content"][:500] + "..." if len(s["content"]) > 500 else s["content"]
                }
                for s in results['processed_sources']
            ]
        }, f, indent=2)
    
    print(f"\nDetailed results saved to crawler_test_results.json")
    
except Exception as e:
    logger.error(f"Error testing crawler: {str(e)}")
    import traceback
    traceback.print_exc()
