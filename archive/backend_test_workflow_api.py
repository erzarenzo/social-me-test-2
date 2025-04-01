#!/usr/bin/env python3
import requests
import json
import time
import sys

# Base URL - change if needed
BASE_URL = "http://localhost:8003"

# Session to maintain cookies across requests
session = requests.Session()

def print_response(response, label=None):
    """Print API response in a readable format"""
    if label:
        print(f"\n===== {label} =====")
    
    try:
        print(f"Status Code: {response.status_code}")
        print("Response:")
        
        if response.headers.get('content-type') == 'application/json':
            print(json.dumps(response.json(), indent=2))
        else:
            print(response.text[:500] + "..." if len(response.text) > 500 else response.text)
    except Exception as e:
        print(f"Error parsing response: {e}")
        print(response.text[:200])
    
    print("=" * 50)

def test_landing_page():
    """Test the landing page"""
    response = session.get(f"{BASE_URL}/")
    print_response(response, "Landing Page")
    return response.status_code == 200

def test_step1_data_sources():
    """Test Step 1: Data Sources"""
    # First access the page to initialize session
    response = session.get(f"{BASE_URL}/onboarding/step1")
    print_response(response, "Step 1: Data Sources Page")
    
    # Add sample data sources
    sources = [
        {"url": "https://www.example.com/article1", "type": "article"},
        {"url": "https://twitter.com/example", "type": "twitter"},
        {"url": "https://www.linkedin.com/in/example", "type": "linkedin"}
    ]
    
    for source in sources:
        response = session.post(
            f"{BASE_URL}/add-source", 
            data={"source_url": source["url"], "source_type": source["type"]}
        )
        print_response(response, f"Add Source: {source['url']}")
        
        # Get a preview of the source
        response = session.post(
            f"{BASE_URL}/preview-source",
            data={"source_url": source["url"]}
        )
        print_response(response, f"Preview Source: {source['url']}")
    
    return True

def test_step2_writing_style():
    """Test Step 2: Writing Style Analysis"""
    # First access the page
    response = session.get(f"{BASE_URL}/onboarding/step2")
    print_response(response, "Step 2: Writing Style Page")
    
    # Test direct text analysis
    sample_text = """
    The integration of artificial intelligence in modern software development has 
    revolutionized how we approach problem-solving and product creation. With the 
    advent of machine learning models that can interpret complex patterns, developers 
    now have powerful tools at their disposal to create more intuitive and responsive 
    applications. This paradigm shift not only enhances user experience but also 
    streamlines the development process itself.
    """
    
    response = session.post(
        f"{BASE_URL}/analyze-content",
        data={"type": "text", "content": sample_text}
    )
    print_response(response, "Analyze Text Content")
    
    # Test URL analysis
    response = session.post(
        f"{BASE_URL}/analyze-content",
        data={"type": "url", "content": "https://www.example.com/sample-article"}
    )
    print_response(response, "Analyze URL Content")
    
    # Note: We're not testing file upload since that's more complex in requests
    
    return True

def test_step3_content_strategy():
    """Test Step 3: Content Strategy"""
    # First access the page
    response = session.get(f"{BASE_URL}/onboarding/step3")
    print_response(response, "Step 3: Content Strategy Page")
    
    # Save a content strategy
    strategy = {
        "primary_topic": "AI in Software Development",
        "content_focus": "Technical tutorials and best practices",
        "target_audience": "Software developers and technical managers",
        "content_goals": ["Educate", "Establish authority", "Drive engagement"],
        "tone_preferences": ["Professional", "Technical", "Approachable"],
        "publication_frequency": "Weekly"
    }
    
    response = session.post(
        f"{BASE_URL}/save-strategy",
        json=strategy,
        headers={"Content-Type": "application/json"}
    )
    print_response(response, "Save Content Strategy")
    
    return True

def test_step4_article_generation():
    """Test Step 4: Article Generation"""
    # First access the page
    response = session.get(f"{BASE_URL}/onboarding/step4")
    print_response(response, "Step 4: Article Generation Page")
    
    # First, crawl and analyze the sources
    response = session.post(f"{BASE_URL}/crawl-and-analyze")
    print_response(response, "Crawl and Analyze Sources")
    
    # Then generate the article
    response = session.post(
        f"{BASE_URL}/generate-article",
        data={"generator_type": "advanced"}
    )
    print_response(response, "Generate Article")
    
    # Preview the article
    if response.status_code == 200 and response.json().get('success'):
        response = session.get(f"{BASE_URL}/article-preview")
        print_response(response, "Article Preview")
    
    return True

def run_all_tests():
    """Run all tests in sequence"""
    print("TESTING COMPLETE WORKFLOW API")
    print("============================\n")
    
    tests = [
        ("Landing Page", test_landing_page),
        ("Step 1: Data Sources", test_step1_data_sources),
        ("Step 2: Writing Style", test_step2_writing_style),
        ("Step 3: Content Strategy", test_step3_content_strategy),
        ("Step 4: Article Generation", test_step4_article_generation)
    ]
    
    results = []
    
    for name, test_func in tests:
        print(f"\n\nTESTING: {name}")
        print("-" * (len(name) + 9))
        
        try:
            start_time = time.time()
            success = test_func()
            elapsed = time.time() - start_time
            
            status = "PASSED" if success else "FAILED"
            print(f"\n{name}: {status} (Time: {elapsed:.2f}s)")
            results.append((name, status, elapsed))
        except Exception as e:
            print(f"\n{name}: ERROR - {str(e)}")
            results.append((name, "ERROR", 0))
    
    print("\n\nTEST SUMMARY")
    print("============")
    for name, status, elapsed in results:
        print(f"{name:30} {status:10} {elapsed:.2f}s")

if __name__ == "__main__":
    run_all_tests()
