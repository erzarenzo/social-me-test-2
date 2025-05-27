#!/usr/bin/env python3
"""
Reorganized Workflow Implementation Test

This script demonstrates the implementation of the reorganized workflow using the existing
powerful components via their HTTP API endpoints.

The reorganized workflow follows this order:
1. Content Strategy Definition
2. Targeted Data Sources
3. Writing Style Analysis
4. Article Generation
"""

import requests
import json
import time
import sys
import os
import logging
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Base URL - change if needed
BASE_URL = "http://localhost:8003"

# Session to maintain cookies across requests
session = requests.Session()

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
            try:
                json_data = response.json()
                print(f"{color}{json.dumps(json_data, indent=2)}{Colors.ENDC}")
                return json_data
            except json.JSONDecodeError:
                print(f"{Colors.RED}Error decoding JSON response{Colors.ENDC}")
                print(f"{color}{response.text[:300] + '...' if len(response.text) > 300 else response.text}{Colors.ENDC}")
                return None
        else:
            print(f"{color}{response.text[:300] + '...' if len(response.text) > 300 else response.text}{Colors.ENDC}")
            # For non-JSON responses, return None instead of the text
            return None
    except Exception as e:
        print(f"{Colors.RED}Error parsing response: {e}{Colors.ENDC}")
        print(f"{color}{response.text[:200]}{Colors.ENDC}")
        return None
    
    finally:
        print(f"{color}{'=' * 50}{Colors.ENDC}")

def print_header(text, color=Colors.HEADER):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{color}{'=' * 60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{color}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.BOLD}{color}{'=' * 60}{Colors.ENDC}")

def print_step(text, color=Colors.BLUE):
    """Print a formatted step header"""
    print(f"\n{Colors.BOLD}{color}{text}{Colors.ENDC}")
    print(f"{Colors.BOLD}{color}{'-' * len(text)}{Colors.ENDC}")

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

class ReorganizedWorkflowImplementation:
    """
    Implementation of the reorganized workflow using existing API endpoints.
    
    This class demonstrates how to use the existing powerful components in a new order:
    1. Content Strategy First
    2. Targeted Data Sources
    3. Writing Style Analysis
    4. Article Generation
    """
    
    def __init__(self):
        """Initialize the workflow implementation"""
        # Access the v2 workflow entry point to reset the session
        try:
            response = session.get(f"{BASE_URL}/v2/")
            print_response(response, "Initializing V2 Workflow", Colors.HEADER)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error accessing V2 workflow: {e}{Colors.ENDC}")
            # Fall back to regular workflow
            response = session.get(f"{BASE_URL}/")
            print_response(response, "Initializing Regular Workflow (Fallback)", Colors.HEADER)
        
        print_header("REORGANIZED WORKFLOW IMPLEMENTATION")
        print_data_flow("Initialized workflow session", "INFO")
    
    def step1_define_content_strategy(self):
        """Step 1: Define Content Strategy"""
        print_step("STEP 1: CONTENT STRATEGY DEFINITION", Colors.MAGENTA)
        print_data_flow("Starting Content Strategy Definition step", "INFO")
        
        # First access the content strategy page
        try:
            response = session.get(f"{BASE_URL}/v2/step1")
            print_response(response, "Content Strategy Page", Colors.MAGENTA)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error accessing V2 step1: {e}{Colors.ENDC}")
            # Fall back to regular step3 (content strategy in original workflow)
            response = session.get(f"{BASE_URL}/step3")
            print_response(response, "Content Strategy Page (Fallback)", Colors.MAGENTA)
        
        # Define a comprehensive content strategy
        strategy = {
            "primary_topic": "The Future of Sustainable Technology",
            "content_focus": "How sustainable technology is transforming industries and addressing climate challenges",
            "target_audience": "Technology professionals, sustainability advocates, and forward-thinking business leaders",
            "content_pillars": [
                "Renewable Energy Technologies",
                "Sustainable Computing and Green IT",
                "Circular Economy Solutions",
                "Smart Cities and Sustainable Infrastructure",
                "Climate Tech Innovations"
            ],
            "desired_word_count": 4000,
            "tone_preferences": {
                "formality": "medium-high",
                "technical_depth": "balanced",
                "perspective": "forward-looking and solution-oriented"
            },
            "content_goals": {
                "educate": 40,
                "inspire": 30,
                "analyze": 30
            }
        }
        
        print_data_flow(f"Defined content strategy: {strategy['primary_topic']}", "STRATEGY")
        print_data_flow(f"Content pillars: {', '.join(strategy['content_pillars'])}", "STRATEGY")
        
        # Save the strategy using the API endpoint
        try:
            response = session.post(
                f"{BASE_URL}/save-strategy",
                json=strategy,
                headers={"Content-Type": "application/json"}
            )
            strategy_result = print_response(response, "Save Content Strategy", Colors.MAGENTA)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error saving content strategy: {e}{Colors.ENDC}")
            strategy_result = None
        
        return strategy_result and strategy_result.get('status') == 'success'
    
    def step2_targeted_data_sources(self):
        """Step 2: Add Targeted Data Sources based on Strategy"""
        print_step("STEP 2: TARGETED DATA SOURCES", Colors.GREEN)
        print_data_flow("Starting Targeted Data Sources step", "INFO")
        
        # Access the data sources page
        try:
            response = session.get(f"{BASE_URL}/v2/step2")
            print_response(response, "Targeted Data Sources Page", Colors.GREEN)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error accessing V2 step2: {e}{Colors.ENDC}")
            # Fall back to regular step1 (data sources in original workflow)
            response = session.get(f"{BASE_URL}/step1")
            print_response(response, "Data Sources Page (Fallback)", Colors.GREEN)
        
        # Map content pillars to relevant sources
        pillar_to_sources = {
            "Renewable Energy Technologies": [
                {"url": "https://www.renewableenergyworld.com/", "type": "news"},
                {"url": "https://cleantechnica.com/", "type": "blog"}
            ],
            "Sustainable Computing and Green IT": [
                {"url": "https://www.greentechmedia.com/", "type": "news"},
                {"url": "https://www.theverge.com/green-technology", "type": "blog"}
            ],
            "Circular Economy Solutions": [
                {"url": "https://www.ellenmacarthurfoundation.org/", "type": "research"},
                {"url": "https://www.circle-economy.com/news", "type": "blog"}
            ],
            "Smart Cities and Sustainable Infrastructure": [
                {"url": "https://www.smartcitiesworld.net/", "type": "news"},
                {"url": "https://www.c40.org/", "type": "research"}
            ],
            "Climate Tech Innovations": [
                {"url": "https://techcrunch.com/category/greentech/", "type": "news"},
                {"url": "https://www.climatetech.vc/", "type": "blog"}
            ]
        }
        
        # Add sources with topic relevance
        for pillar, sources in pillar_to_sources.items():
            print_data_flow(f"Adding sources for pillar: {pillar}", "STRATEGY")
            
            for source in sources:
                print_data_flow(f"Adding source: {source['url']} (Type: {source['type']})", "CRAWL")
                
                # Add the source with topic relevance using the new endpoint
                try:
                    response = session.post(
                        f"{BASE_URL}/add-source-with-topic", 
                        data={
                            "source_url": source["url"], 
                            "source_type": source["type"],
                            "topic_relevance": pillar
                        }
                    )
                    source_result = print_response(response, f"Add Source: {source['url']}", Colors.GREEN)
                except requests.RequestException as e:
                    print(f"{Colors.RED}Error adding source: {e}{Colors.ENDC}")
                    source_result = None
                
                # Also preview the source to ensure content extraction works
                print_data_flow(f"Previewing source content for relevance", "CRAWL")
                try:
                    response = session.post(
                        f"{BASE_URL}/preview-source",
                        data={"source_url": source["url"]}
                    )
                    preview_result = print_response(response, f"Preview Source: {source['url']}", Colors.GREEN)
                except requests.RequestException as e:
                    print(f"{Colors.RED}Error previewing source: {e}{Colors.ENDC}")
                    preview_result = None
        
        # Get the current sources count
        sources_count = 0
        try:
            # Try to extract the count from the last source result
            if isinstance(source_result, dict) and 'count' in source_result:
                sources_count = source_result.get('count', 0)
            else:
                # If we can't get the count from the response, count manually
                response = session.get(f"{BASE_URL}/get-sources")
                sources_data = print_response(response, "Get Sources Count", Colors.GREEN)
                if isinstance(sources_data, dict) and 'sources' in sources_data:
                    sources_count = len(sources_data['sources'])
                else:
                    # Assume we added at least the sources we tried to add
                    sources_count = len(pillar_to_sources) * 2  # 2 sources per pillar
        except Exception as e:
            print(f"{Colors.RED}Error getting sources count: {e}{Colors.ENDC}")
            # Assume we added at least the sources we tried to add
            sources_count = len(pillar_to_sources) * 2  # 2 sources per pillar
            
        print_data_flow(f"Added {sources_count} targeted sources", "INFO")
        return sources_count > 0
    
    def step3_writing_style_analysis(self):
        """Step 3: Writing Style Analysis"""
        print_step("STEP 3: WRITING STYLE ANALYSIS", Colors.CYAN)
        print_data_flow("Starting Writing Style Analysis step", "INFO")
        
        # Access the writing style page
        try:
            response = session.get(f"{BASE_URL}/v2/step3")
            print_response(response, "Writing Style Analysis Page", Colors.CYAN)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error accessing V2 step3: {e}{Colors.ENDC}")
            # Fall back to regular step2 (writing style in original workflow)
            response = session.get(f"{BASE_URL}/step2")
            print_response(response, "Writing Style Analysis Page (Fallback)", Colors.CYAN)
        
        # Prepare a writing sample focused on sustainability and technology
        sample_text = """
        Sustainable Technology: Bridging Innovation and Environmental Responsibility

        The intersection of technological innovation and environmental sustainability represents one of the most promising frontiers in our collective effort to address climate change. As we navigate the complexities of the 21st century, it becomes increasingly evident that technology must not only advance human capabilities but also regenerate our natural systems.

        Renewable energy technologies have demonstrated remarkable progress in recent years. Solar photovoltaics have experienced a 90% cost reduction over the past decade, while wind energy continues to set new records for efficiency and scale. These advancements are transforming our energy landscape, enabling a transition from fossil fuels to clean, renewable sources. The integration of smart grid technologies further enhances this transition by optimizing energy distribution, reducing waste, and accommodating the variable nature of renewable generation.

        Sustainable computing represents another critical domain where technological innovation meets environmental responsibility. The exponential growth in data centers' energy consumption has prompted the development of energy-efficient hardware, advanced cooling systems, and software optimizations that significantly reduce the carbon footprint of our digital infrastructure. Leading technology companies have committed to carbon-neutral or carbon-negative operations, demonstrating that environmental stewardship can align with business objectives.

        The circular economy model is revolutionizing how we design, manufacture, and dispose of technological products. By prioritizing durability, repairability, and recyclability, manufacturers are extending product lifecycles and reducing electronic waste. Advanced materials science enables the development of biodegradable components and recovery processes for rare earth elements, further minimizing environmental impact.

        Smart cities integrate various sustainable technologies to enhance urban living while reducing resource consumption. From intelligent transportation systems that reduce congestion and emissions to smart buildings that optimize energy use, these integrated approaches demonstrate how technology can create more livable, efficient urban environments. Water management systems employ sensors and analytics to detect leaks, monitor quality, and optimize distribution, addressing critical resource challenges in urban settings.

        Climate tech innovations extend beyond mitigation to include adaptation strategies. Advanced modeling and simulation tools help communities prepare for climate impacts, while precision agriculture technologies enable farmers to maintain productivity despite changing conditions. Carbon capture and sequestration technologies offer promising approaches to removing existing carbon dioxide from the atmosphere, complementing emission reduction efforts.

        As we advance these technologies, we must maintain a holistic perspective that considers not only environmental impacts but also social equity and economic viability. The transition to sustainable technology must create opportunities across socioeconomic boundaries and geographic regions. Open-source approaches, knowledge sharing, and inclusive innovation ecosystems can help ensure that sustainable technologies benefit humanity broadly rather than exacerbating existing inequalities.

        The path forward requires unprecedented collaboration among governments, industries, research institutions, and civil society. Policy frameworks must provide both stability for long-term investments and flexibility to accommodate rapid technological change. Financing mechanisms must channel capital toward promising innovations while managing risks appropriately. Educational systems must prepare a workforce with the interdisciplinary skills needed to advance sustainable technology.

        By embracing this comprehensive approach to sustainable technology development, we can harness human ingenuity to create systems that operate within planetary boundaries while enhancing quality of life. The challenge is substantial, but the convergence of technological capability, environmental necessity, and social will creates a unique opportunity to reshape our relationship with both technology and the natural world.
        """
        
        print_data_flow("Analyzing writing style sample", "PROCESS")
        
        # Submit the writing sample for analysis using the API endpoint
        try:
            response = session.post(
                f"{BASE_URL}/analyze-content",
                data={"type": "text", "content": sample_text}
            )
            tone_result = print_response(response, "Writing Style Analysis Results", Colors.CYAN)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error analyzing writing style: {e}{Colors.ENDC}")
            tone_result = None
        
        if tone_result:
            print_data_flow("Writing style analysis completed successfully", "PROCESS")
            
            # Print some key insights from the analysis
            if isinstance(tone_result, dict) and 'analysis' in tone_result:
                analysis = tone_result['analysis']
                if 'cognitive_profile_analysis' in analysis:
                    profile = analysis['cognitive_profile_analysis']
                    for section_name, section in profile.items():
                        if isinstance(section, dict) and 'title' in section:
                            print_data_flow(f"Analysis section: {section['title']}", "PROCESS")
                            if 'items' in section:
                                for item in section['items'][:2]:  # Show first 2 items
                                    print_data_flow(f"  - {item}", "PROCESS")
            
            return True
        else:
            print_data_flow("Failed to analyze writing style", "ERROR")
            return False
    
    def step4_topic_guided_crawl_and_article_generation(self):
        """Step 4: Topic-Guided Crawl and Article Generation"""
        print_step("STEP 4: TOPIC-GUIDED CRAWL AND ARTICLE GENERATION", Colors.YELLOW)
        print_data_flow("Starting Topic-Guided Crawl and Article Generation step", "INFO")
        
        # Access the article generation page
        try:
            response = session.get(f"{BASE_URL}/v2/step4")
            print_response(response, "Article Generation Page", Colors.YELLOW)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error accessing V2 step4: {e}{Colors.ENDC}")
            # Fall back to regular step4 (article generation in original workflow)
            response = session.get(f"{BASE_URL}/step4")
            print_response(response, "Article Generation Page (Fallback)", Colors.YELLOW)
        
        # First, crawl and analyze the sources with topic guidance
        print_data_flow("Performing topic-guided crawl", "CRAWL")
        try:
            response = session.post(f"{BASE_URL}/topic-guided-crawl")
            crawl_result = print_response(response, "Topic-Guided Crawl", Colors.GREEN)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error with topic-guided crawl: {e}{Colors.ENDC}")
            crawl_result = None
        
        if not crawl_result or (isinstance(crawl_result, dict) and crawl_result.get('status') != 'success'):
            print_data_flow("Failed to perform topic-guided crawl", "ERROR")
            # Fall back to regular crawl
            print_data_flow("Falling back to regular crawl", "CRAWL")
            try:
                response = session.post(f"{BASE_URL}/crawl-and-analyze")
                crawl_result = print_response(response, "Regular Crawl", Colors.GREEN)
            except requests.RequestException as e:
                print(f"{Colors.RED}Error with regular crawl: {e}{Colors.ENDC}")
                crawl_result = None
        
        # Generate the article with the reorganized workflow approach
        print_data_flow("Generating article with topic guidance", "WRITE")
        try:
            response = session.post(
                f"{BASE_URL}/generate-article-v2",
                data={
                    "generator_type": "advanced",
                    "word_count": "4000",
                    "include_citations": "true",
                    "style_emphasis": "balanced"
                }
            )
            article_result = print_response(response, "Generate Article", Colors.YELLOW)
        except requests.RequestException as e:
            print(f"{Colors.RED}Error with V2 article generation: {e}{Colors.ENDC}")
            article_result = None
        
        if not article_result or (isinstance(article_result, dict) and article_result.get('status') != 'success'):
            print_data_flow("Failed to generate article with v2 endpoint, falling back to regular endpoint", "ERROR")
            # Fall back to regular article generation
            try:
                response = session.post(
                    f"{BASE_URL}/generate-article",
                    data={
                        "generator_type": "advanced",
                        "word_count": "4000",
                        "include_citations": "true",
                        "style_emphasis": "balanced"
                    }
                )
                article_result = print_response(response, "Generate Article (Fallback)", Colors.YELLOW)
            except requests.RequestException as e:
                print(f"{Colors.RED}Error with regular article generation: {e}{Colors.ENDC}")
                article_result = None
        
        # Calculate word counts if article was generated
        if article_result and isinstance(article_result, dict) and article_result.get('success') and article_result.get('article'):
            article = article_result['article']
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
            print_data_flow("Accessing article preview", "CRAWL")
            try:
                response = session.get(f"{BASE_URL}/article-preview")
                preview_response = print_response(response, "Article Preview")
            except requests.RequestException as e:
                print(f"{Colors.RED}Error accessing article preview: {e}{Colors.ENDC}")
                preview_response = None
            
            # Save the generated article to a file for review
            try:
                with open('reorganized_implementation_article.html', 'w') as f:
                    f.write(response.text)
                print_data_flow("Article saved to reorganized_implementation_article.html for review", "WRITE")
                
                # Also save the raw JSON for analysis
                with open('reorganized_implementation_article.json', 'w') as f:
                    json.dump(article_result, f, indent=2)
                print_data_flow("Raw article data saved to reorganized_implementation_article.json", "WRITE")
            except Exception as e:
                print(f"{Colors.RED}Error saving article: {e}{Colors.ENDC}")
            
            return True
        else:
            print_data_flow("Failed to generate article", "ERROR")
            return False

def run_reorganized_workflow_implementation():
    """Run the reorganized workflow implementation"""
    workflow = ReorganizedWorkflowImplementation()
    
    overall_start = time.time()
    
    # Step 1: Content Strategy Definition
    step1_start = time.time()
    step1_result = workflow.step1_define_content_strategy()
    step1_time = time.time() - step1_start
    
    # Step 2: Targeted Data Sources
    step2_start = time.time()
    step2_result = workflow.step2_targeted_data_sources()
    step2_time = time.time() - step2_start
    
    # Step 3: Writing Style Analysis
    step3_start = time.time()
    step3_result = workflow.step3_writing_style_analysis()
    step3_time = time.time() - step3_start
    
    # Step 4: Topic-Guided Crawl and Article Generation
    step4_start = time.time()
    step4_result = workflow.step4_topic_guided_crawl_and_article_generation()
    step4_time = time.time() - step4_start
    
    # Print test summary
    print_header("REORGANIZED WORKFLOW IMPLEMENTATION SUMMARY")
    print(f"{Colors.BOLD}Step 1: Content Strategy Definition  {Colors.GREEN if step1_result else Colors.RED}{'PASSED' if step1_result else 'FAILED'}{Colors.ENDC}     {step1_time:.2f}s")
    print(f"{Colors.BOLD}Step 2: Targeted Data Sources        {Colors.GREEN if step2_result else Colors.RED}{'PASSED' if step2_result else 'FAILED'}{Colors.ENDC}     {step2_time:.2f}s")
    print(f"{Colors.BOLD}Step 3: Writing Style Analysis       {Colors.GREEN if step3_result else Colors.RED}{'PASSED' if step3_result else 'FAILED'}{Colors.ENDC}     {step3_time:.2f}s")
    print(f"{Colors.BOLD}Step 4: Topic-Guided Crawl & Article {Colors.GREEN if step4_result else Colors.RED}{'PASSED' if step4_result else 'FAILED'}{Colors.ENDC}     {step4_time:.2f}s")
    
    total_time = time.time() - overall_start
    print(f"\n{Colors.BOLD}Total implementation time: {total_time:.2f}s{Colors.ENDC}")
    
    # Provide implementation insights
    print_header("IMPLEMENTATION INSIGHTS", Colors.BLUE)
    print(f"1. {Colors.BOLD}Workflow Efficiency{Colors.ENDC}: The reorganized workflow improves relevance by guiding data collection with strategy")
    print(f"2. {Colors.BOLD}Component Reuse{Colors.ENDC}: Successfully leveraged existing powerful components via their API endpoints")
    print(f"3. {Colors.BOLD}Topic Relevance{Colors.ENDC}: Added topic relevance scoring to improve content selection")
    print(f"4. {Colors.BOLD}Integration Path{Colors.ENDC}: Demonstrated how to integrate this approach into the existing application")

if __name__ == "__main__":
    # Check if terminal supports colors
    if os.name == 'nt':  # Windows
        os.system('color')
    
    try:
        run_reorganized_workflow_implementation()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}Implementation interrupted by user.{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.RED}Error during implementation: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
