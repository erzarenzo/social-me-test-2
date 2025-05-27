#!/usr/bin/env python3
import requests
import json
import time
import sys
import os

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Base URL - change if needed
BASE_URL = "http://localhost:8003"

# Session to maintain cookies across requests
session = requests.Session()

def print_response(response, label=None, color=None):
    """Print API response in a readable format with optional color"""
    if not color:
        color = Colors.ENDC
        
    if label:
        print(f"\n{Colors.BOLD}{color}===== {label} ====={Colors.ENDC}")
    
    try:
        print(f"{color}Status Code: {response.status_code}{Colors.ENDC}")
        print(f"{color}Response:{Colors.ENDC}")
        
        if response.headers.get('content-type') == 'application/json':
            json_data = response.json()
            print(f"{color}{json.dumps(json_data, indent=2)}{Colors.ENDC}")
            return json_data
        else:
            print(f"{color}{response.text[:300] + '...' if len(response.text) > 300 else response.text}{Colors.ENDC}")
            return response.text
    except Exception as e:
        print(f"{Colors.RED}Error parsing response: {e}{Colors.ENDC}")
        print(f"{color}{response.text[:200]}{Colors.ENDC}")
        return None
    
    finally:
        print(f"{color}{'=' * 50}{Colors.ENDC}")

def print_data_flow(message, data_type="INFO"):
    """Print data flow information with appropriate colors"""
    if data_type == "CRAWL":
        color = Colors.GREEN
        prefix = "🔍 CRAWLING"
    elif data_type == "WRITE":
        color = Colors.CYAN
        prefix = "✏️ WRITING"
    elif data_type == "PROCESS":
        color = Colors.YELLOW
        prefix = "⚙️ PROCESSING"
    elif data_type == "ERROR":
        color = Colors.RED
        prefix = "❌ ERROR"
    else:
        color = Colors.BLUE
        prefix = "ℹ️ INFO"
        
    print(f"{color}{prefix}: {message}{Colors.ENDC}")

def test_step1_data_sources():
    """Test Step 1: Data Sources with real sources"""
    print_data_flow("Starting Data Sources step", "INFO")
    start_time = time.time()
    
    # First access the page to initialize session
    print_data_flow("Accessing data sources page", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step1")
    print_response(response, "Step 1: Data Sources Page")
    
    # Add real data sources
    sources = [
        {"url": "https://techcrunch.com/category/artificial-intelligence/", "type": "news"},
        {"url": "https://www.linkedin.com/in/andrew-ng-stanford/", "type": "linkedin"},
        {"url": "https://twitter.com/ylecun", "type": "twitter"},
        {"url": "https://openai.com/blog/", "type": "blog"},
        {"url": "https://www.deeplearning.ai/blog/", "type": "blog"}
    ]
    
    for source in sources:
        print_data_flow(f"Adding source: {source['url']} (Type: {source['type']})", "WRITE")
        response = session.post(
            f"{BASE_URL}/add-source", 
            data={"source_url": source["url"], "source_type": source["type"]}
        )
        print_response(response, f"Add Source: {source['url']}")
        
        # Also preview the source to ensure content extraction works
        print_data_flow(f"Previewing source content: {source['url']}", "CRAWL")
        response = session.post(
            f"{BASE_URL}/preview-source",
            data={"source_url": source["url"]}
        )
        source_data = print_response(response, f"Preview Source: {source['url']}")
        
        if source_data and 'preview' in source_data:
            word_count = source_data['preview'].get('word_count', 0)
            print_data_flow(f"Extracted {word_count} words from {source['url']}", "PROCESS")
    
    elapsed = time.time() - start_time
    print_data_flow(f"Step 1: Data Sources completed in {elapsed:.2f}s", "INFO")
    return True

def test_step2_writing_style():
    """Test Step 2: Writing Style Analysis with real text"""
    print_data_flow("Starting Writing Style Analysis step", "INFO")
    start_time = time.time()
    
    # First access the page
    print_data_flow("Accessing writing style page", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step2")
    print_response(response, "Step 2: Writing Style Page")
    
    # Prepare a real writing sample about AI
    print_data_flow("Preparing writing sample for analysis", "PROCESS")
    sample_text = """
    The Evolution of Artificial Intelligence: From Rule-Based Systems to Deep Learning
    
    Artificial intelligence has undergone a remarkable transformation over the past few decades. What began as simple rule-based expert systems has evolved into sophisticated neural networks capable of recognizing patterns, understanding natural language, and even generating creative content.
    
    The early days of AI were characterized by symbolic approaches, where human experts would encode knowledge as explicit rules. These systems excelled at well-defined tasks but struggled with ambiguity and couldn't learn from experience. The limitations became apparent in the 1980s, leading to what's known as the "AI winter" - a period of reduced funding and interest.
    
    The renaissance of AI began with the resurgence of machine learning in the 1990s and early 2000s. Rather than hard-coding rules, these systems learned patterns from data. Support Vector Machines and Random Forests became popular for classification tasks, while recommendation systems began to appear in e-commerce platforms.
    
    The true breakthrough came with deep learning, particularly after 2012 when AlexNet demonstrated the power of convolutional neural networks for image recognition. Suddenly, AI systems could outperform humans at specific perceptual tasks. The development of architectures like recurrent neural networks and transformers further expanded capabilities into language processing, leading to models like GPT and BERT.
    
    Today, we're witnessing the emergence of multimodal AI systems that can process and generate content across different formats - text, images, audio, and video. These systems are increasingly integrated into our daily lives, from voice assistants to content recommendation engines.
    
    The future of AI likely involves more sophisticated reasoning capabilities, better alignment with human values, and increased transparency in how decisions are made. As these systems become more powerful, ensuring they remain beneficial, safe, and accessible becomes a critical societal challenge.
    """
    
    print_data_flow(f"Analyzing writing sample ({len(sample_text.split())} words)", "WRITE")
    # Submit the writing sample for analysis
    response = session.post(
        f"{BASE_URL}/analyze-content",
        data={"type": "text", "content": sample_text}
    )
    tone_data = print_response(response, "Writing Style Analysis Results", Colors.GREEN)
    
    if tone_data:
        print_data_flow("Extracted tone characteristics:", "PROCESS")
        for key, value in tone_data.items():
            if isinstance(value, dict):
                print_data_flow(f"  {key}: {json.dumps(value)}", "PROCESS")
    
    elapsed = time.time() - start_time
    print_data_flow(f"Step 2: Writing Style completed in {elapsed:.2f}s", "INFO")
    return True

def test_step3_content_strategy():
    """Test Step 3: Content Strategy with real strategy"""
    print_data_flow("Starting Content Strategy step", "INFO")
    start_time = time.time()
    
    # First access the page
    print_data_flow("Accessing content strategy page", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step3")
    print_response(response, "Step 3: Content Strategy Page")
    
    # Create a real content strategy for AI in healthcare
    print_data_flow("Creating content strategy for AI in healthcare", "PROCESS")
    strategy = {
        "primary_topic": "The Future of AI in Healthcare",
        "content_focus": "How AI is transforming medical diagnostics, treatment planning, and patient care",
        "target_audience": "Healthcare professionals, technology leaders, and policy makers",
        "content_pillars": [
            "AI-powered diagnostic imaging",
            "Predictive analytics for patient outcomes",
            "Personalized treatment planning",
            "Ethical considerations and patient privacy",
            "Healthcare workflow automation"
        ],
        "desired_word_count": 4000,
        "tone_preferences": {
            "formality": "high",
            "technical_depth": "expert",
            "perspective": "balanced"
        }
    }
    
    print_data_flow("Saving content strategy to system", "WRITE")
    # Submit the strategy
    response = session.post(
        f"{BASE_URL}/save-strategy",
        json=strategy,
        headers={"Content-Type": "application/json"}
    )
    print_response(response, "Save Real Content Strategy")
    
    elapsed = time.time() - start_time
    print_data_flow(f"Step 3: Content Strategy completed in {elapsed:.2f}s", "INFO")
    return True

def test_step4_article_generation():
    """Test Step 4: Article Generation with real parameters"""
    print_data_flow("Starting Article Generation step", "INFO")
    start_time = time.time()
    
    # First access the page
    print_data_flow("Accessing article generation page", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step4")
    print_response(response, "Step 4: Article Generation Page")
    
    # First, crawl and analyze the sources
    print_data_flow("Crawling and analyzing all sources", "CRAWL")
    response = session.post(f"{BASE_URL}/crawl-and-analyze")
    crawl_data = print_response(response, "Crawl and Analyze Real Sources", Colors.GREEN)
    
    if crawl_data:
        print_data_flow(f"Crawled {len(crawl_data.get('sources', []))} sources", "PROCESS")
        for idx, source in enumerate(crawl_data.get('sources', [])[:3]):  # Show first 3 sources
            print_data_flow(f"  Source {idx+1}: {source.get('url')} - {source.get('word_count', 0)} words", "PROCESS")
    
    # Then generate the article with advanced settings
    print_data_flow("Generating article with advanced settings (4000 words)", "WRITE")
    response = session.post(
        f"{BASE_URL}/generate-article",
        data={
            "generator_type": "advanced",
            "word_count": "4000",
            "include_citations": "true",
            "style_emphasis": "analytical"
        }
    )
    article_data = print_response(response, "Generate Real Article", Colors.CYAN)
    
    # Calculate word counts if article was generated
    if article_data and article_data.get('success') and article_data.get('article'):
        article = article_data['article']
        intro_words = len(article.get('introduction', '').split())
        section_words = sum(len(section.get('content', '').split()) for section in article.get('body', []))
        conclusion_words = len(article.get('conclusion', '').split())
        total_words = intro_words + section_words + conclusion_words
        
        print_data_flow("Article word count analysis:", "PROCESS")
        print_data_flow(f"  Introduction: {intro_words} words", "PROCESS")
        print_data_flow(f"  Body sections: {section_words} words", "PROCESS")
        print_data_flow(f"  Conclusion: {conclusion_words} words", "PROCESS")
        print_data_flow(f"  TOTAL: {total_words} words", "PROCESS")
        
        if total_words < 3500:
            print_data_flow(f"WARNING: Article is shorter than target (4000 words)", "ERROR")
    
    # Preview the article
    if response.status_code == 200 and article_data.get('success'):
        print_data_flow("Accessing article preview", "CRAWL")
        response = session.get(f"{BASE_URL}/article-preview")
        preview_response = print_response(response, "Article Preview")
        
        # Save the generated article to a file for review
        try:
            with open('generated_article.html', 'w') as f:
                f.write(response.text)
            print_data_flow("Article saved to generated_article.html for review", "WRITE")
            
            # Also save the raw JSON for analysis
            with open('article_data.json', 'w') as f:
                json.dump(article_data, f, indent=2)
            print_data_flow("Raw article data saved to article_data.json", "WRITE")
        except Exception as e:
            print_data_flow(f"Error saving article: {e}", "ERROR")
    
    elapsed = time.time() - start_time
    result = "PASSED" if response.status_code == 200 and article_data and article_data.get('success') else "FAILED"
    print_data_flow(f"Step 4: Article Generation: {result} (Time: {elapsed:.2f}s)", "INFO")
    return result == "PASSED"

def run_realistic_test():
    """Run a realistic workflow test with real data"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}REALISTIC WORKFLOW TEST{Colors.ENDC}")
    print(f"{Colors.HEADER}======================\n{Colors.ENDC}")
    
    overall_start = time.time()
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}TESTING: Step 1: Data Sources{Colors.ENDC}")
    print(f"{Colors.YELLOW}-----------------------------{Colors.ENDC}")
    step1_start = time.time()
    step1_result = test_step1_data_sources()
    step1_time = time.time() - step1_start
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}TESTING: Step 2: Writing Style{Colors.ENDC}")
    print(f"{Colors.YELLOW}-----------------------------{Colors.ENDC}")
    step2_start = time.time()
    step2_result = test_step2_writing_style()
    step2_time = time.time() - step2_start
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}TESTING: Step 3: Content Strategy{Colors.ENDC}")
    print(f"{Colors.YELLOW}-------------------------------{Colors.ENDC}")
    step3_start = time.time()
    step3_result = test_step3_content_strategy()
    step3_time = time.time() - step3_start
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}TESTING: Step 4: Article Generation{Colors.ENDC}")
    print(f"{Colors.YELLOW}---------------------------------{Colors.ENDC}")
    step4_start = time.time()
    step4_result = test_step4_article_generation()
    step4_time = time.time() - step4_start
    
    # Print summary
    print(f"\n\n{Colors.BOLD}{Colors.HEADER}TEST SUMMARY{Colors.ENDC}")
    print(f"{Colors.HEADER}============{Colors.ENDC}")
    print(f"{Colors.BOLD}Step 1: Data Sources           {Colors.GREEN if step1_result else Colors.RED}{'PASSED' if step1_result else 'FAILED'}{Colors.ENDC}     {step1_time:.2f}s")
    print(f"{Colors.BOLD}Step 2: Writing Style          {Colors.GREEN if step2_result else Colors.RED}{'PASSED' if step2_result else 'FAILED'}{Colors.ENDC}     {step2_time:.2f}s")
    print(f"{Colors.BOLD}Step 3: Content Strategy       {Colors.GREEN if step3_result else Colors.RED}{'PASSED' if step3_result else 'FAILED'}{Colors.ENDC}     {step3_time:.2f}s")
    print(f"{Colors.BOLD}Step 4: Article Generation     {Colors.GREEN if step4_result else Colors.RED}{'PASSED' if step4_result else 'FAILED'}{Colors.ENDC}     {step4_time:.2f}s")
    
    # Data flow summary
    print(f"\n{Colors.BOLD}{Colors.BLUE}DATA FLOW SUMMARY{Colors.ENDC}")
    print(f"{Colors.BLUE}================={Colors.ENDC}")
    print(f"{Colors.GREEN}🔍 CRAWLING{Colors.ENDC}: Data collection from sources and API endpoints")
    print(f"{Colors.YELLOW}⚙️ PROCESSING{Colors.ENDC}: Analysis and transformation of collected data")
    print(f"{Colors.CYAN}✏️ WRITING{Colors.ENDC}: Generation of content and saving to storage")
    
    total_time = time.time() - overall_start
    print(f"\n{Colors.BOLD}Total test time: {total_time:.2f}s{Colors.ENDC}")

if __name__ == "__main__":
    # Check if terminal supports colors
    if os.name == 'nt':  # Windows
        os.system('color')
    
    try:
        run_realistic_test()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Test interrupted by user{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}Error running test: {e}{Colors.ENDC}")
        import traceback
        print(f"{Colors.RED}{traceback.format_exc()}{Colors.ENDC}")
        sys.exit(1)
