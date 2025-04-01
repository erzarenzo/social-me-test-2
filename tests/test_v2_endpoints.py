#!/usr/bin/env python3
"""
Test script for the v2 workflow endpoints.
This script tests the new v2 workflow endpoints in the SocialMe application.
"""

import requests
import json
import time
import sys

BASE_URL = "http://localhost:8003"

def print_response(response, label="Response"):
    """Print a formatted response"""
    print(f"\n{label}:")
    print(f"Status Code: {response.status_code}")
    try:
        print(f"Content: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Content: {response.text[:200]}...")

def test_v2_workflow():
    """Test the v2 workflow endpoints"""
    print("\n===== TESTING V2 WORKFLOW ENDPOINTS =====\n")
    
    # Step 1: Initialize v2 workflow
    print("\n1. Initializing v2 workflow...")
    response = requests.get(f"{BASE_URL}/v2/")
    print_response(response)
    
    if response.status_code != 200:
        print("ERROR: Failed to initialize v2 workflow")
        return False
    
    # Check workflow version
    print("\n2. Checking workflow version...")
    response = requests.get(f"{BASE_URL}/workflow-version")
    print_response(response)
    
    if response.status_code != 200:
        print("ERROR: Failed to get workflow version")
        return False
    
    # Step 2: Submit content strategy
    print("\n3. Submitting content strategy...")
    content_strategy = {
        "primary_topic": "Artificial Intelligence in Healthcare",
        "content_pillars": ["Medical Diagnostics", "Patient Care", "Drug Discovery"],
        "target_audience": "Healthcare professionals and technology enthusiasts",
        "publishing_frequency": "Weekly",
        "content_types": ["Articles", "Case Studies", "Research Summaries"]
    }
    
    response = requests.post(
        f"{BASE_URL}/submit-content-strategy",
        json=content_strategy
    )
    print_response(response)
    
    # Step 3: Add sources with topic relevance
    print("\n4. Adding sources with topic relevance...")
    sources = [
        {
            "source_url": "https://www.nature.com/articles/s41591-020-0791-x",
            "source_type": "research",
            "topic_relevance": "Medical Diagnostics"
        },
        {
            "source_url": "https://www.healthcareitnews.com/ai-powered-healthcare",
            "source_type": "article",
            "topic_relevance": "Patient Care"
        },
        {
            "source_url": "https://www.frontiersin.org/articles/10.3389/fphar.2020.01028/full",
            "source_type": "research",
            "topic_relevance": "Drug Discovery"
        }
    ]
    
    for source in sources:
        response = requests.post(
            f"{BASE_URL}/add-source-with-topic",
            data=source
        )
        print_response(response, f"Added source: {source['source_url']}")
    
    # Step 4: Perform topic-guided crawl
    print("\n5. Performing topic-guided crawl...")
    response = requests.post(f"{BASE_URL}/topic-guided-crawl")
    print_response(response)
    
    if response.status_code != 200:
        print("ERROR: Failed to perform topic-guided crawl")
        return False
    
    # Step 5: Submit writing style
    print("\n6. Submitting writing style...")
    writing_style = {
        "text": "Artificial intelligence (AI) is revolutionizing healthcare. From diagnostic tools to treatment planning, AI applications are enhancing clinical workflows and improving patient outcomes. Recent studies demonstrate that AI algorithms can detect patterns in medical imaging with accuracy comparable to human specialists, but at significantly faster speeds. However, challenges remain in implementation, including regulatory hurdles, integration with existing systems, and ethical considerations around patient data privacy.",
        "source_type": "direct_input"
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze-writing-style",
        json=writing_style
    )
    print_response(response)
    
    # Step 6: Generate article with v2 workflow
    print("\n7. Generating article with v2 workflow...")
    article_params = {
        "word_count": 1500,
        "include_citations": True,
        "style_emphasis": "balanced"
    }
    
    response = requests.post(
        f"{BASE_URL}/generate-article-v2",
        data=article_params
    )
    print_response(response)
    
    if response.status_code != 200:
        print("ERROR: Failed to generate article")
        return False
    
    print("\n===== V2 WORKFLOW TEST COMPLETED =====")
    return True

if __name__ == "__main__":
    print("Starting v2 workflow endpoint tests...")
    success = test_v2_workflow()
    
    if success:
        print("\nAll tests completed successfully!")
        sys.exit(0)
    else:
        print("\nSome tests failed. Check the output above for details.")
        sys.exit(1)
