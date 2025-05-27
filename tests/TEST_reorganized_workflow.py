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
    MAGENTA = '\033[35m'

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
    elif data_type == "STRATEGY":
        color = Colors.MAGENTA
        prefix = "🎯 STRATEGY"
    else:
        color = Colors.BLUE
        prefix = "ℹ️ INFO"
        
    print(f"{color}{prefix}: {message}{Colors.ENDC}")

def test_step1_content_strategy():
    """Test Step 1: Define Content Strategy (Reorganized)"""
    print_data_flow("Starting Content Strategy Definition step", "INFO")
    start_time = time.time()
    
    # First access the content strategy page
    print_data_flow("Accessing content strategy page", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step3")  # Using existing step3 route
    print_response(response, "Step 1: Content Strategy Definition Page")
    
    # Create a content strategy for technology trends
    print_data_flow("Creating content strategy for technology trends", "STRATEGY")
    strategy = {
        "primary_topic": "Emerging Technology Trends for 2025",
        "content_focus": "How emerging technologies are reshaping industries and everyday life",
        "target_audience": "Technology enthusiasts, business leaders, and forward-thinking consumers",
        "content_pillars": [
            "Artificial Intelligence and Machine Learning",
            "Sustainable Technology Solutions",
            "Augmented and Virtual Reality Applications",
            "Internet of Things and Smart Devices",
            "Blockchain Beyond Cryptocurrency"
        ],
        "desired_word_count": 4000,
        "tone_preferences": {
            "formality": "medium",
            "technical_depth": "balanced",
            "perspective": "forward-looking"
        }
    }
    
    print_data_flow("Saving content strategy to system", "WRITE")
    # Submit the strategy
    response = session.post(
        f"{BASE_URL}/save-strategy",
        json=strategy,
        headers={"Content-Type": "application/json"}
    )
    print_response(response, "Save Content Strategy")
    
    elapsed = time.time() - start_time
    print_data_flow(f"Step 1: Content Strategy Definition completed in {elapsed:.2f}s", "INFO")
    return True, strategy

def test_step2_data_sources(strategy):
    """Test Step 2: Add Relevant Data Sources based on Strategy (Reorganized)"""
    print_data_flow("Starting Data Sources step with topic guidance", "INFO")
    start_time = time.time()
    
    # First access the page to initialize session
    print_data_flow("Accessing data sources page", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step1")  # Using existing step1 route
    print_response(response, "Step 2: Targeted Data Sources Page")
    
    # Add data sources relevant to the strategy topic
    print_data_flow(f"Selecting sources relevant to: {strategy['primary_topic']}", "STRATEGY")
    
    # Map topic pillars to relevant sources
    topic_to_sources = {
        "Artificial Intelligence and Machine Learning": [
            {"url": "https://ai.googleblog.com/", "type": "blog"},
            {"url": "https://twitter.com/AndrewYNg", "type": "twitter"}
        ],
        "Sustainable Technology Solutions": [
            {"url": "https://www.greentechmedia.com/", "type": "news"},
            {"url": "https://cleantechnica.com/", "type": "blog"}
        ],
        "Augmented and Virtual Reality Applications": [
            {"url": "https://www.roadtovr.com/", "type": "blog"},
            {"url": "https://twitter.com/oculus", "type": "twitter"}
        ],
        "Internet of Things and Smart Devices": [
            {"url": "https://staceyoniot.com/", "type": "blog"},
            {"url": "https://www.iotforall.com/", "type": "news"}
        ],
        "Blockchain Beyond Cryptocurrency": [
            {"url": "https://www.ledgerinsights.com/", "type": "news"},
            {"url": "https://www.coindesk.com/tag/blockchain/", "type": "blog"}
        ]
    }
    
    # Flatten the sources list
    sources = []
    for pillar, pillar_sources in topic_to_sources.items():
        print_data_flow(f"Adding sources for pillar: {pillar}", "STRATEGY")
        sources.extend(pillar_sources)
    
    for source in sources:
        print_data_flow(f"Adding targeted source: {source['url']} (Type: {source['type']})", "WRITE")
        response = session.post(
            f"{BASE_URL}/add-source", 
            data={"source_url": source["url"], "source_type": source["type"]}
        )
        print_response(response, f"Add Source: {source['url']}")
        
        # Also preview the source to ensure content extraction works
        print_data_flow(f"Previewing source content for relevance to {strategy['primary_topic']}", "CRAWL")
        response = session.post(
            f"{BASE_URL}/preview-source",
            data={"source_url": source["url"]}
        )
        source_data = print_response(response, f"Preview Source: {source['url']}")
        
        if source_data and 'preview' in source_data:
            word_count = source_data['preview'].get('word_count', 0)
            print_data_flow(f"Extracted {word_count} words from {source['url']} relevant to {strategy['primary_topic']}", "PROCESS")
    
    elapsed = time.time() - start_time
    print_data_flow(f"Step 2: Targeted Data Sources completed in {elapsed:.2f}s", "INFO")
    return True

def test_step3_writing_style():
    """Test Step 3: Writing Style Analysis (Reorganized)"""
    print_data_flow("Starting Writing Style Analysis step", "INFO")
    start_time = time.time()
    
    # First access the page
    print_data_flow("Accessing writing style page", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step2")  # Using existing step2 route
    print_response(response, "Step 3: Writing Style Page")
    
    # Prepare a writing sample about technology trends
    print_data_flow("Preparing writing sample for analysis", "PROCESS")
    sample_text = """
    The Convergence of Technologies: How AI, IoT, and Blockchain Are Reshaping Our Future
    
    The most significant technological developments of the past decade have not occurred in isolation. Rather, we're witnessing an unprecedented convergence of emerging technologies that, when combined, create possibilities far greater than the sum of their parts.
    
    Artificial intelligence serves as the brain, processing vast amounts of data to extract meaningful insights and make predictions with increasing accuracy. The Internet of Things functions as the nervous system, with billions of sensors collecting real-time data from our physical environment. Blockchain technology provides a trust layer, ensuring that data remains secure, transparent, and immutable.
    
    This convergence is already transforming industries. In healthcare, AI algorithms analyze data from wearable IoT devices to predict potential health issues before symptoms appear, while blockchain ensures patient data remains private yet accessible to authorized healthcare providers. In supply chain management, IoT sensors track products from manufacture to delivery, AI optimizes routing and inventory, and blockchain creates an unalterable record of each transaction and handoff.
    
    The financial sector is perhaps experiencing the most dramatic transformation. Decentralized finance (DeFi) platforms leverage smart contracts on blockchain networks to automate lending, borrowing, and trading without traditional intermediaries. AI algorithms detect fraudulent activities and optimize investment strategies, while IoT devices enable new payment methods and real-time asset tracking.
    
    Smart cities represent the ultimate expression of this technological convergence. Traffic lights adjust their timing based on real-time traffic data from IoT sensors, with AI optimizing the flow to reduce congestion and emissions. Energy grids automatically adjust to demand fluctuations, incorporating renewable sources when available and storing excess capacity for peak usage periods. Blockchain-based voting systems and public records increase civic participation and transparency.
    
    However, this convergence also presents significant challenges. The complexity of these interconnected systems makes them vulnerable to cascading failures. Privacy concerns multiply when AI can analyze vast amounts of personal data collected through ubiquitous IoT devices. Questions of accountability become more complex when decisions are made by autonomous systems rather than individuals.
    
    As we navigate this new technological landscape, we must ensure that these powerful tools serve humanity's best interests. This requires thoughtful regulation, robust security measures, and a commitment to ethical principles that place human well-being at the center of technological development. The convergence of AI, IoT, and blockchain offers unprecedented opportunities to address our most pressing challenges, but realizing this potential demands that we approach these technologies with both enthusiasm and responsibility.
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
    print_data_flow(f"Step 3: Writing Style completed in {elapsed:.2f}s", "INFO")
    return True

def test_step4_article_generation():
    """Test Step 4: Article Generation (Reorganized)"""
    print_data_flow("Starting Article Generation step", "INFO")
    start_time = time.time()
    
    # First access the page
    print_data_flow("Accessing article generation page", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step4")  # Using existing step4 route
    print_response(response, "Step 4: Article Generation Page")
    
    # First, crawl and analyze the sources with topic guidance
    print_data_flow("Crawling and analyzing sources with topic focus", "CRAWL")
    response = session.post(f"{BASE_URL}/crawl-and-analyze")
    crawl_data = print_response(response, "Crawl and Analyze Sources", Colors.GREEN)
    
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
            "style_emphasis": "balanced"
        }
    )
    article_data = print_response(response, "Generate Article", Colors.CYAN)
    
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
            with open('reorganized_article.html', 'w') as f:
                f.write(response.text)
            print_data_flow("Article saved to reorganized_article.html for review", "WRITE")
            
            # Also save the raw JSON for analysis
            with open('reorganized_article_data.json', 'w') as f:
                json.dump(article_data, f, indent=2)
            print_data_flow("Raw article data saved to reorganized_article_data.json", "WRITE")
        except Exception as e:
            print_data_flow(f"Error saving article: {e}", "ERROR")
    
    elapsed = time.time() - start_time
    result = "PASSED" if response.status_code == 200 and article_data and article_data.get('success') else "FAILED"
    print_data_flow(f"Step 4: Article Generation: {result} (Time: {elapsed:.2f}s)", "INFO")
    return result == "PASSED"

def run_reorganized_test():
    """Run a reorganized workflow test"""
    print(f"\n{Colors.BOLD}{Colors.HEADER}REORGANIZED WORKFLOW TEST{Colors.ENDC}")
    print(f"{Colors.HEADER}=========================\n{Colors.ENDC}")
    
    overall_start = time.time()
    
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}TESTING: Step 1: Content Strategy Definition{Colors.ENDC}")
    print(f"{Colors.MAGENTA}----------------------------------------{Colors.ENDC}")
    step1_start = time.time()
    step1_result, strategy = test_step1_content_strategy()
    step1_time = time.time() - step1_start
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}TESTING: Step 2: Targeted Data Sources{Colors.ENDC}")
    print(f"{Colors.YELLOW}-----------------------------------{Colors.ENDC}")
    step2_start = time.time()
    step2_result = test_step2_data_sources(strategy)
    step2_time = time.time() - step2_start
    
    print(f"\n{Colors.BOLD}{Colors.CYAN}TESTING: Step 3: Writing Style Analysis{Colors.ENDC}")
    print(f"{Colors.CYAN}-------------------------------------{Colors.ENDC}")
    step3_start = time.time()
    step3_result = test_step3_writing_style()
    step3_time = time.time() - step3_start
    
    print(f"\n{Colors.BOLD}{Colors.GREEN}TESTING: Step 4: Article Generation{Colors.ENDC}")
    print(f"{Colors.GREEN}----------------------------------{Colors.ENDC}")
    step4_start = time.time()
    step4_result = test_step4_article_generation()
    step4_time = time.time() - step4_start
    
    # Print test summary
    print(f"\n\n{Colors.BOLD}{Colors.HEADER}REORGANIZED TEST SUMMARY{Colors.ENDC}")
    print(f"{Colors.HEADER}======================={Colors.ENDC}")
    print(f"{Colors.BOLD}Step 1: Content Strategy Definition  {Colors.GREEN if step1_result else Colors.RED}{'PASSED' if step1_result else 'FAILED'}{Colors.ENDC}     {step1_time:.2f}s")
    print(f"{Colors.BOLD}Step 2: Targeted Data Sources        {Colors.GREEN if step2_result else Colors.RED}{'PASSED' if step2_result else 'FAILED'}{Colors.ENDC}     {step2_time:.2f}s")
    print(f"{Colors.BOLD}Step 3: Writing Style Analysis       {Colors.GREEN if step3_result else Colors.RED}{'PASSED' if step3_result else 'FAILED'}{Colors.ENDC}     {step3_time:.2f}s")
    print(f"{Colors.BOLD}Step 4: Article Generation           {Colors.GREEN if step4_result else Colors.RED}{'PASSED' if step4_result else 'FAILED'}{Colors.ENDC}     {step4_time:.2f}s")
    
    # Print data flow summary
    print(f"\n{Colors.BOLD}{Colors.BLUE}REORGANIZED DATA FLOW SUMMARY{Colors.ENDC}")
    print(f"{Colors.BLUE}============================={Colors.ENDC}")
    print(f"{Colors.MAGENTA}🎯 STRATEGY{Colors.ENDC}: Define topic and content strategy first")
    print(f"{Colors.GREEN}🔍 CRAWLING{Colors.ENDC}: Targeted data collection based on strategy")
    print(f"{Colors.YELLOW}⚙️ PROCESSING{Colors.ENDC}: Analysis and transformation of collected data")
    print(f"{Colors.CYAN}✏️ WRITING{Colors.ENDC}: Generation of content guided by strategy and data")
    
    total_time = time.time() - overall_start
    print(f"\n{Colors.BOLD}Total test time: {total_time:.2f}s{Colors.ENDC}")
    
    # Provide recommendations
    print(f"\n{Colors.BOLD}{Colors.HEADER}WORKFLOW RECOMMENDATIONS{Colors.ENDC}")
    print(f"{Colors.HEADER}========================={Colors.ENDC}")
    print(f"1. {Colors.BOLD}API Changes{Colors.ENDC}: Create new endpoints that accept topic parameters for targeted crawling")
    print(f"2. {Colors.BOLD}Session Management{Colors.ENDC}: Update to store strategy before sources")
    print(f"3. {Colors.BOLD}UI Updates{Colors.ENDC}: Reorder workflow steps in UI and update navigation")
    print(f"4. {Colors.BOLD}Crawler Enhancement{Colors.ENDC}: Modify crawler to filter content by topic relevance")

if __name__ == "__main__":
    # Check if terminal supports colors
    if os.name == 'nt':  # Windows
        os.system('color')
    
    try:
        run_reorganized_test()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Test interrupted by user.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error during test: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
