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
    MAGENTA = '\033[35m'  # Added for fun elements

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
    elif data_type == "FUN":
        color = Colors.MAGENTA
        prefix = "🎉 FUN FACT"
    else:
        color = Colors.BLUE
        prefix = "ℹ️ INFO"
        
    print(f"{color}{prefix}: {message}{Colors.ENDC}")

def test_step1_fun_data_sources():
    """Test Step 1: Fun and Lighthearted Data Sources"""
    print_data_flow("Starting Fun Data Sources step", "INFO")
    start_time = time.time()
    
    # First access the page to initialize session
    print_data_flow("Accessing data sources page with a smile 😊", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step1")
    print_response(response, "Step 1: Fun Data Sources Page")
    
    # Add fun and lighthearted data sources
    sources = [
        {"url": "https://www.theonion.com/", "type": "news"},
        {"url": "https://www.reddit.com/r/dadjokes/", "type": "blog"},
        {"url": "https://twitter.com/ConanOBrien", "type": "twitter"},
        {"url": "https://www.boredpanda.com/", "type": "blog"},
        {"url": "https://www.buzzfeed.com/trending", "type": "news"}
    ]
    
    print_data_flow("Adding sources that will make you smile!", "FUN")
    
    for source in sources:
        print_data_flow(f"Adding fun source: {source['url']} (Type: {source['type']})", "WRITE")
        response = session.post(
            f"{BASE_URL}/add-source", 
            data={"source_url": source["url"], "source_type": source["type"]}
        )
        print_response(response, f"Add Source: {source['url']}")
        
        # Also preview the source to ensure content extraction works
        print_data_flow(f"Peeking at the fun content from: {source['url']}", "CRAWL")
        response = session.post(
            f"{BASE_URL}/preview-source",
            data={"source_url": source["url"]}
        )
        source_data = print_response(response, f"Preview Source: {source['url']}")
        
        if source_data and 'preview' in source_data:
            word_count = source_data['preview'].get('word_count', 0)
            print_data_flow(f"Extracted {word_count} words of fun from {source['url']}", "PROCESS")
    
    elapsed = time.time() - start_time
    print_data_flow(f"Step 1: Fun Data Sources completed in {elapsed:.2f}s", "INFO")
    return True

def test_step2_fun_writing_style():
    """Test Step 2: Fun and Lighthearted Writing Style Analysis"""
    print_data_flow("Starting Fun Writing Style Analysis step", "INFO")
    start_time = time.time()
    
    # First access the page
    print_data_flow("Accessing writing style page", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step2")
    print_response(response, "Step 2: Fun Writing Style Page")
    
    # Prepare a fun writing sample
    print_data_flow("Preparing a fun writing sample for analysis", "PROCESS")
    sample_text = """
    The Ultimate Guide to Cat Logic: Understanding Your Feline Overlord
    
    If you've ever lived with a cat, you know they operate on a different plane of existence. One minute they're purring contentedly on your lap, the next they're zooming around the house at 3 AM like they're possessed. Let's decode some of this mysterious cat behavior!
    
    First, the infamous "if I fits, I sits" phenomenon. Your cat will ignore the $100 luxury bed you bought them but will immediately claim an empty Amazon box as their new kingdom. The smaller the box, the more determined they are to prove they can fit. It's like watching a liquid take the shape of its container, except the liquid is furry and occasionally bites.
    
    Then there's the classic "knocking things off surfaces" move. This isn't random destruction - it's science! Your cat is testing gravity, one glass at a time. They make direct eye contact while slowly pushing your favorite mug to the edge. It's not personal; they're just confirming that gravity still works today.
    
    The "sudden zoomies" are another cat classic. One second they're peacefully sleeping, the next they're performing parkour off your furniture. These random bursts of energy usually happen at the least convenient times, like during important Zoom calls or at 2 AM when you're trying to sleep. It's their way of staying in shape for when they need to hunt down the elusive red dot.
    
    Let's not forget the "sit on whatever you're using" behavior. Reading a book? That's now a cat seat. Working on your laptop? Sorry, that keyboard is prime napping real estate. This isn't just about seeking attention - cats are naturally drawn to warmth and your focused energy. Plus, they're helping you take much-needed breaks!
    
    Finally, there's the mysterious "cat activation sound" - that weird chirping noise they make when they see birds through the window. It's not quite a meow, not quite a chatter, but it's universally adorable. Some experts believe it's a sign of excitement or frustration when they can't reach their prey. I prefer to think they're just providing commentary: "Look at that ridiculous bird, thinking it can fly better than me!"
    
    Understanding cat logic may seem impossible, but remember: in their minds, they're not living in your house - you're living in theirs. And they're generously allowing you to serve them. The sooner you accept your role as the butler, the happier your feline overlord will be!
    """
    
    print_data_flow(f"Analyzing fun writing sample ({len(sample_text.split())} words)", "WRITE")
    # Submit the writing sample for analysis
    response = session.post(
        f"{BASE_URL}/analyze-content",
        data={"type": "text", "content": sample_text}
    )
    tone_data = print_response(response, "Fun Writing Style Analysis Results", Colors.GREEN)
    
    if tone_data:
        print_data_flow("Extracted fun tone characteristics:", "PROCESS")
        for key, value in tone_data.items():
            if isinstance(value, dict):
                print_data_flow(f"  {key}: {json.dumps(value)}", "PROCESS")
    
    print_data_flow("Did you know? Cats make over 100 different vocal sounds, while dogs only make about 10!", "FUN")
    
    elapsed = time.time() - start_time
    print_data_flow(f"Step 2: Fun Writing Style completed in {elapsed:.2f}s", "INFO")
    return True

def test_step3_fun_content_strategy():
    """Test Step 3: Fun and Lighthearted Content Strategy"""
    print_data_flow("Starting Fun Content Strategy step", "INFO")
    start_time = time.time()
    
    # First access the page
    print_data_flow("Accessing content strategy page", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step3")
    print_response(response, "Step 3: Fun Content Strategy Page")
    
    # Create a fun content strategy
    print_data_flow("Creating a fun content strategy about pets", "PROCESS")
    strategy = {
        "primary_topic": "The Secret Lives of Pets: What They Do When We're Not Home",
        "content_focus": "Humorous exploration of pet behavior, imagined pet thoughts, and funny pet scenarios",
        "target_audience": "Pet owners with a sense of humor, animal lovers, and social media scrollers looking for a laugh",
        "content_pillars": [
            "Cats vs. Furniture: An Ongoing Battle",
            "Dogs and Their Bizarre Obsessions",
            "Pet Conspiracy Theories: Are They Plotting World Domination?",
            "If Pets Could Text: Message Conversations We'd Have",
            "Ridiculous Pet Products That Actually Exist"
        ],
        "desired_word_count": 4000,
        "tone_preferences": {
            "formality": "low",
            "humor_level": "high",
            "perspective": "lighthearted"
        }
    }
    
    print_data_flow("Saving fun content strategy to system", "WRITE")
    # Submit the strategy
    response = session.post(
        f"{BASE_URL}/save-strategy",
        json=strategy,
        headers={"Content-Type": "application/json"}
    )
    print_response(response, "Save Fun Content Strategy")
    
    print_data_flow("Did you know? Studies show that looking at cute animal pictures increases productivity!", "FUN")
    
    elapsed = time.time() - start_time
    print_data_flow(f"Step 3: Fun Content Strategy completed in {elapsed:.2f}s", "INFO")
    return True

def test_step4_fun_article_generation():
    """Test Step 4: Fun and Lighthearted Article Generation"""
    print_data_flow("Starting Fun Article Generation step", "INFO")
    start_time = time.time()
    
    # First access the page
    print_data_flow("Accessing article generation page", "CRAWL")
    response = session.get(f"{BASE_URL}/onboarding/step4")
    print_response(response, "Step 4: Fun Article Generation Page")
    
    # First, crawl and analyze the sources
    print_data_flow("Crawling and analyzing all the fun sources", "CRAWL")
    response = session.post(f"{BASE_URL}/crawl-and-analyze")
    crawl_data = print_response(response, "Crawl and Analyze Fun Sources", Colors.GREEN)
    
    if crawl_data:
        print_data_flow(f"Crawled {len(crawl_data.get('sources', []))} fun sources", "PROCESS")
        for idx, source in enumerate(crawl_data.get('sources', [])[:3]):  # Show first 3 sources
            print_data_flow(f"  Source {idx+1}: {source.get('url')} - {source.get('word_count', 0)} words of fun", "PROCESS")
    
    # Then generate the article with fun settings
    print_data_flow("Generating a fun article (4000 words of pure entertainment!)", "WRITE")
    response = session.post(
        f"{BASE_URL}/generate-article",
        data={
            "generator_type": "advanced",
            "word_count": "4000",
            "include_citations": "true",
            "style_emphasis": "humorous"
        }
    )
    article_data = print_response(response, "Generate Fun Article", Colors.CYAN)
    
    # Calculate word counts if article was generated
    if article_data and article_data.get('success') and article_data.get('article'):
        article = article_data['article']
        intro_words = len(article.get('introduction', '').split())
        section_words = sum(len(section.get('content', '').split()) for section in article.get('body', []))
        conclusion_words = len(article.get('conclusion', '').split())
        total_words = intro_words + section_words + conclusion_words
        
        print_data_flow("Fun article word count analysis:", "PROCESS")
        print_data_flow(f"  Introduction: {intro_words} words of joy", "PROCESS")
        print_data_flow(f"  Body sections: {section_words} words of hilarity", "PROCESS")
        print_data_flow(f"  Conclusion: {conclusion_words} words of delight", "PROCESS")
        print_data_flow(f"  TOTAL: {total_words} words of entertainment", "PROCESS")
        
        if total_words < 3500:
            print_data_flow(f"WARNING: Fun article is shorter than target (4000 words)", "ERROR")
    
    # Preview the article
    if response.status_code == 200 and article_data.get('success'):
        print_data_flow("Accessing fun article preview", "CRAWL")
        response = session.get(f"{BASE_URL}/article-preview")
        preview_response = print_response(response, "Fun Article Preview")
        
        # Save the generated article to a file for review
        try:
            with open('fun_generated_article.html', 'w') as f:
                f.write(response.text)
            print_data_flow("Fun article saved to fun_generated_article.html for review", "WRITE")
            
            # Also save the raw JSON for analysis
            with open('fun_article_data.json', 'w') as f:
                json.dump(article_data, f, indent=2)
            print_data_flow("Raw fun article data saved to fun_article_data.json", "WRITE")
        except Exception as e:
            print_data_flow(f"Error saving fun article: {e}", "ERROR")
    
    print_data_flow("Did you know? The average person laughs about 15 times per day!", "FUN")
    
    elapsed = time.time() - start_time
    result = "PASSED" if response.status_code == 200 and article_data and article_data.get('success') else "FAILED"
    print_data_flow(f"Step 4: Fun Article Generation: {result} (Time: {elapsed:.2f}s)", "INFO")
    return result == "PASSED"

def run_fun_test():
    """Run a fun and lighthearted workflow test"""
    print(f"\n{Colors.BOLD}{Colors.MAGENTA}🎉 FUN AND LIGHTHEARTED WORKFLOW TEST 🎉{Colors.ENDC}")
    print(f"{Colors.MAGENTA}======================================\n{Colors.ENDC}")
    
    overall_start = time.time()
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}TESTING: Step 1: Fun Data Sources{Colors.ENDC}")
    print(f"{Colors.YELLOW}-----------------------------{Colors.ENDC}")
    step1_start = time.time()
    step1_result = test_step1_fun_data_sources()
    step1_time = time.time() - step1_start
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}TESTING: Step 2: Fun Writing Style{Colors.ENDC}")
    print(f"{Colors.YELLOW}-----------------------------{Colors.ENDC}")
    step2_start = time.time()
    step2_result = test_step2_fun_writing_style()
    step2_time = time.time() - step2_start
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}TESTING: Step 3: Fun Content Strategy{Colors.ENDC}")
    print(f"{Colors.YELLOW}-------------------------------{Colors.ENDC}")
    step3_start = time.time()
    step3_result = test_step3_fun_content_strategy()
    step3_time = time.time() - step3_start
    
    print(f"\n{Colors.BOLD}{Colors.YELLOW}TESTING: Step 4: Fun Article Generation{Colors.ENDC}")
    print(f"{Colors.YELLOW}----------------------------------{Colors.ENDC}")
    step4_start = time.time()
    step4_result = test_step4_fun_article_generation()
    step4_time = time.time() - step4_start
    
    # Print test summary
    print(f"\n\n{Colors.BOLD}{Colors.MAGENTA}FUN TEST SUMMARY{Colors.ENDC}")
    print(f"{Colors.MAGENTA}============{Colors.ENDC}")
    print(f"{Colors.BOLD}Step 1: Fun Data Sources           {Colors.GREEN if step1_result else Colors.RED}{'PASSED' if step1_result else 'FAILED'}{Colors.ENDC}     {step1_time:.2f}s")
    print(f"{Colors.BOLD}Step 2: Fun Writing Style          {Colors.GREEN if step2_result else Colors.RED}{'PASSED' if step2_result else 'FAILED'}{Colors.ENDC}     {step2_time:.2f}s")
    print(f"{Colors.BOLD}Step 3: Fun Content Strategy       {Colors.GREEN if step3_result else Colors.RED}{'PASSED' if step3_result else 'FAILED'}{Colors.ENDC}     {step3_time:.2f}s")
    print(f"{Colors.BOLD}Step 4: Fun Article Generation     {Colors.GREEN if step4_result else Colors.RED}{'PASSED' if step4_result else 'FAILED'}{Colors.ENDC}     {step4_time:.2f}s")
    
    # Print data flow summary
    print(f"\n{Colors.BOLD}{Colors.BLUE}FUN DATA FLOW SUMMARY{Colors.ENDC}")
    print(f"{Colors.BLUE}================={Colors.ENDC}")
    print(f"{Colors.GREEN}🔍 CRAWLING{Colors.ENDC}: Fun data collection from sources and API endpoints")
    print(f"{Colors.YELLOW}⚙️ PROCESSING{Colors.ENDC}: Analysis and transformation of fun collected data")
    print(f"{Colors.CYAN}✏️ WRITING{Colors.ENDC}: Generation of fun content and saving to storage")
    print(f"{Colors.MAGENTA}🎉 FUN FACTS{Colors.ENDC}: Random tidbits of entertainment along the way")
    
    total_time = time.time() - overall_start
    print(f"\n{Colors.BOLD}Total test time: {total_time:.2f}s{Colors.ENDC}")
    
    print(f"\n{Colors.MAGENTA}Thanks for testing! Hope you had as much fun as we did! 😄{Colors.ENDC}")

if __name__ == "__main__":
    # Check if terminal supports colors
    if os.name == 'nt':  # Windows
        os.system('color')
    
    try:
        run_fun_test()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Test interrupted by user.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error during test: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
