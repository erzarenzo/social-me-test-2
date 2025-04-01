#!/usr/bin/env python3
"""
Complete Workflow Test for SocialMe Application:
1. User inputs sources for data points
2. User inputs sources for tone and writing style analysis
3. User sets content strategy and timing schedules
4. App generates content by:
   a) Crawling the first URL for data points using the quantum universal crawler
   b) Analyzing the tone using the quantum tone analyzer
   c) Writing a detailed article combining data points and adapting to user's tone
"""

import os
import json
import logging
import datetime
import random
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from dotenv import load_dotenv
import threading
import socket
import uuid
from flask import Blueprint

# Load environment variables first
load_dotenv()

# Import standardized configuration
from app.utils.config import config

# Configure logging
logging.basicConfig(
    level=logging.INFO if not config.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("workflow_test.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("workflow_test")

# Initialize the components we need from the standardized structure
from app.generators.factory import get_article_generator
from app.neural_tone_mapper import NeuralToneMapper
from app.crawlers.tone import ToneCrawler 
from app.crawlers.universal import UniversalCrawler
from app.utils.helpers import extract_topics, extract_key_insights, extract_supporting_data
from app.routes.onboarding import onboarding_bp  # Import the onboarding blueprint

def find_free_port():
    """
    Find a free port for the Flask application
    
    Returns:
        int: A free port number
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def run_flask_server(app, port):
    """
    Run Flask server in a separate thread
    
    Args:
        app (Flask): Flask application instance
        port (int): Port to run the server on
    """
    app.run(host='0.0.0.0', port=port, debug=config.debug, use_reloader=False)

class EnhancedWorkflowTest:
    def __init__(self, test_mode=False):
        """
        Initialize the Enhanced Workflow Test
        
        Args:
            test_mode (bool): If True, use predefined or default values
        """
        # Logging setup
        logging.basicConfig(
            level=logging.INFO, 
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("enhanced_workflow_test")
        self.logger.info("Enhanced workflow tester initialized with Advanced Tone Adaptation support")
        
        # Initialize advanced tone analysis components
        self.tone_mapper = NeuralToneMapper(debug=config.debug)
        self.tone_crawler = ToneCrawler()
        self.universal_crawler = UniversalCrawler()
        
        # Test mode flag
        self.test_mode = test_mode
        
        # Initialize workflow components
        self.content_strategy = {}
        self.data_sources = []
        self.tone_sources = []
        self.crawled_data = []
        self.tone_analysis = {}
        self.generated_article = {}
        
        # Add Flask server configuration
        self.flask_port = find_free_port()
        self.flask_thread = None
    
    def start_flask_server(self):
        """
        Start the Flask server in a background thread
        """
        try:
            self.flask_thread = threading.Thread(
                target=run_flask_server, 
                args=(app, self.flask_port), 
                daemon=True
            )
            self.flask_thread.start()
            self.logger.info(f"Flask server started on port {self.flask_port}")
            
            # Small delay to ensure server is up
            import time
            time.sleep(2)
        except Exception as e:
            self.logger.error(f"Failed to start Flask server: {e}")
    
    def process_tone_sources(self):
        """
        Process tone sources for advanced style analysis with robust input handling
        
        Returns:
            Dict[str, Any]: Comprehensive tone analysis results
        """
        # Prompt for tone sources with multiple input methods
        print("\n================================================================================")
        print("STEP 2: WRITING STYLE ANALYSIS")
        print("================================================================================")
        
        # Collect tone sources
        while True:
            source_input = input("Enter a URL, text, or file path for tone analysis (or 'done' to finish): ").strip()
            
            if source_input.lower() == 'done':
                break
            
            # Validate and add source
            if source_input:
                self.tone_sources.append(source_input)
        
        # Perform comprehensive tone analysis
        try:
            # Use NeuralToneMapper for advanced analysis
            self.tone_analysis = self.tone_mapper.analyze_tone(self.tone_sources)
            
            # Generate a style prompt for article generation
            self.style_prompt = self.tone_mapper.generate_style_prompt(self.tone_analysis)
            
            # Pretty print the tone analysis results
            print("\nTone Analysis Results:")
            print(json.dumps(self.tone_analysis, indent=2))
            
            # Optional: Display style prompt
            print("\nGenerated Style Prompt:")
            print(self.style_prompt)
            
            return self.tone_analysis
        
        except Exception as e:
            self.logger.error(f"Error in tone analysis: {e}")
            # Fallback mechanism
            return {
                "error": "Tone analysis failed",
                "details": str(e)
            }
    
    def generate_advanced_article(self):
        """
        Generate an advanced article using the Enhanced Tone Adaptation System
        
        Returns:
            Dict[str, Any]: Generated article with style-matched content
        """
        print("\n================================================================================")
        print("STEP 3: GENERATE ARTICLE")
        print("================================================================================")
        
        try:
            # Get article generator with Claude API integration
            article_generator = get_article_generator()
            
            # Prepare topic and sources
            topic = input("Enter the main topic for your article: ")
            
            # Crawl supporting data sources
            supporting_sources = self.data_sources + self.tone_sources
            crawled_content = [
                self.universal_crawler.extract_content(source) 
                for source in supporting_sources
            ]
            
            # Generate article with style-guided generation
            self.generated_article = article_generator.generate_article(
                topic=topic,
                style_profile=self.tone_analysis,
                style_prompt=self.style_prompt,
                source_material=crawled_content
            )
            
            # Print article details
            print("\nGenerated Article Details:")
            print(f"Title: {self.generated_article.get('title', 'Untitled')}")
            print(f"Word Count: {len(self.generated_article.get('content', '').split())}")
            
            return self.generated_article
        
        except Exception as e:
            self.logger.error(f"Article generation failed: {e}")
            # Fallback mechanism for article generation
            return {
                "error": "Article generation failed",
                "details": str(e)
            }
    
    def define_content_strategy(self):
        """
        Define the content strategy for the workflow
        
        This method allows users to set up their content generation parameters
        and strategy before starting the tone analysis and article generation.
        """
        print("\n================================================================================")
        print("STEP 1: CONTENT STRATEGY DEFINITION")
        print("================================================================================")
        
        # Set up default strategy
        self.content_strategy = {
            "target_word_count": 1000,
            "tone_preference": "professional",
            "sources_limit": 50,
            "content_types": [
                "blog_articles", 
                "news_sources", 
                "professional_profiles"
            ]
        }
        
        # Interactive strategy definition if not in test mode
        if not self.test_mode:
            try:
                # Target word count
                word_count_input = input(f"Enter target word count (default: {self.content_strategy['target_word_count']}): ").strip()
                if word_count_input:
                    self.content_strategy['target_word_count'] = int(word_count_input)
                
                # Tone preference
                tone_input = input(f"Enter preferred tone (default: {self.content_strategy['tone_preference']}): ").strip()
                if tone_input:
                    self.content_strategy['tone_preference'] = tone_input
                
                # Sources limit
                sources_limit_input = input(f"Enter maximum number of sources (default: {self.content_strategy['sources_limit']}): ").strip()
                if sources_limit_input:
                    self.content_strategy['sources_limit'] = int(sources_limit_input)
                
                # Content types
                print("\nAvailable Content Types:")
                content_types = [
                    "blog_articles", 
                    "news_sources", 
                    "professional_profiles", 
                    "social_media", 
                    "academic_papers", 
                    "technical_documentation"
                ]
                for i, content_type in enumerate(content_types, 1):
                    print(f"{i}. {content_type}")
                
                content_type_input = input("Select content types (comma-separated numbers, default: all): ").strip()
                
                if content_type_input:
                    selected_types = []
                    for index in content_type_input.split(','):
                        try:
                            selected_types.append(content_types[int(index.strip()) - 1])
                        except (ValueError, IndexError):
                            print(f"Invalid selection: {index}")
                    
                    if selected_types:
                        self.content_strategy['content_types'] = selected_types
            
            except Exception as e:
                self.logger.warning(f"Error in content strategy definition: {e}. Using default strategy.")
        
        # Log the final content strategy
        self.logger.info(f"Content Strategy: {json.dumps(self.content_strategy, indent=2)}")
        
        return self.content_strategy

    def validate_style(self):
        """
        Validate the generated article's style against the original sources
        
        Returns:
            Dict[str, Any]: Style validation results
        """
        try:
            # Placeholder implementation for style validation
            validation_results = {
                "style_match_score": 0.75,  # 75% match
                "tone_consistency": True,
                "vocabulary_alignment": 0.8,
                "linguistic_complexity_match": 0.7,
                "recommendations": []
            }
            
            # Add specific recommendations if style doesn't fully match
            if validation_results["style_match_score"] < 0.9:
                validation_results["recommendations"].append(
                    "Consider refining the writing style to more closely match source materials"
                )
            
            return validation_results
        except Exception as e:
            self.logger.error(f"Style validation error: {e}")
            return {
                "error": "Style validation failed",
                "details": str(e)
            }

    def run_comprehensive_workflow(self):
        """
        Run the entire comprehensive workflow with advanced tone adaptation
        """
        print("\n================================================================================")
        print("RUNNING FULL WORKFLOW")
        print("================================================================================")
        
        try:
            # Start Flask server before workflow
            self.start_flask_server()
            
            # Step 1: Define content strategy
            self.define_content_strategy()
            
            # Step 2: Process tone sources and perform advanced analysis
            self.process_tone_sources()
            
            # Step 3: Generate advanced article with style matching
            self.generate_advanced_article()
            
            # Optional: Validate the generated article's style
            self.validate_style()
            
        except Exception as e:
            self.logger.error(f"Workflow failed: {e}")
            print(f"Error in workflow: {e}")
        finally:
            # Cleanup: Stop Flask server thread if running
            if self.flask_thread and self.flask_thread.is_alive():
                self.logger.info("Stopping Flask server...")

# Initialize Flask app
app = Flask(__name__, 
            template_folder=config.get('template_folder', 'templates'),
            static_folder=config.get('static_folder', 'static'))
app.secret_key = config.secret_key

# Register blueprints
try:
    app.register_blueprint(onboarding_bp, url_prefix='/onboarding')
    logger.info("Registered onboarding blueprint")
except NameError:
    logger.warning("Onboarding blueprint not available, using direct routes")

# Initialize the ArticleGenerator using the factory pattern
article_generator = get_article_generator(generator_type='auto')

# In-memory storage for the workflow
class WorkflowData:
    def __init__(self):
        self.data_sources = []
        self.tone_sources = []
        self.content_strategy = {}
        self.tone_analysis = {}
        self.crawled_data = {}
        self.generated_article = {}
        self.current_step = 1
        self.is_v2_workflow = False
        self.topic_relevance_data = {}  # Store topic relevance information for v2 workflow

workflow = WorkflowData()

# Routes for each step of the workflow
@app.route('/')
def index():
    """Landing page with the hero image and 'Start Free Trial' button"""
    logger.info("Rendering landing page")
    return render_template('landing.html')

@app.route('/test-page')
def test_page():
    """Simple test page to verify rendering is working"""
    logger.info("Rendering test page")
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>Test Page</h1>
        <p>If you can see this, the Flask app is working correctly.</p>
        <a href="/onboarding">Go to Onboarding</a>
    </body>
    </html>
    """

@app.route('/onboarding')
def onboarding():
    """Start of the workflow - Redirect to first step"""
    global workflow
    workflow = WorkflowData()
    return redirect('/onboarding/step1')

@app.route('/onboarding/step1', methods=['GET', 'POST'])
def step1_data_sources():
    """Step 1: Data Sources"""
    if request.method == 'POST':
        # Process and store sources
        sources = request.json.get('sources', [])
        workflow.data_sources = sources
    
    workflow.current_step = 1
    return render_template('onboarding/step1_data_sources.html', step=1, sources=workflow.data_sources)

@app.route('/onboarding/step2', methods=['GET', 'POST'])
def writing_style():
    """Step 2: Writing Style Analysis"""
    if request.method == 'POST':
        # Process writing style inputs
        tone_sources = request.json.get('tone_sources', [])
        workflow.tone_sources = tone_sources
    
    workflow.current_step = 2
    return render_template('onboarding/step2_writing_style.html', step=2, tone_sources=workflow.tone_sources)

@app.route('/onboarding/step3', methods=['GET', 'POST'])
def content_strategy():
    """Step 3: Content Strategy"""
    if request.method == 'POST':
        # Process content strategy inputs
        strategy = request.json.get('content_strategy', {})
        workflow.content_strategy = strategy
    
    workflow.current_step = 3
    return render_template('onboarding/step3_content_strategy.html', step=3, strategy=workflow.content_strategy)

@app.route('/onboarding/step4', methods=['GET', 'POST'])
def article_generation():
    """Step 4: Article Generation"""
    if request.method == 'POST':
        # Process article generation inputs
        article_params = request.json.get('article_params', {})
        workflow.generated_article = article_params
    
    workflow.current_step = 4
    return render_template('onboarding/step4_article_generation.html', step=4, article=workflow.generated_article)

@app.route('/add-source', methods=['POST'])
def add_source():
    """Add a source to the data sources list"""
    source_url = request.form.get('source_url', '')
    source_type = request.form.get('source_type', 'article')
    
    if source_url:
        workflow.data_sources.append({
            'url': source_url,
            'type': source_type,
            'added': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        logger.info(f"Added source: {source_url} ({source_type})")
    
    return jsonify({
        'status': 'success',
        'sources': workflow.data_sources,
        'count': len(workflow.data_sources)
    })

@app.route('/preview-source', methods=['POST'])
def preview_source():
    """Generate a preview of content from a source"""
    source_url = request.form.get('source_url', '')
    
    # In a real app, this would fetch actual content
    # For demo purposes, generate a simulated preview
    preview = {
        'title': f"Content from {source_url.split('//')[1] if '//' in source_url else source_url}",
        'excerpt': f"This is a preview of the content that would be extracted from {source_url}. In a real implementation, this would contain actual extracted content from the URL.",
        'topics': ['Topic 1', 'Topic 2', 'Topic 3'],
        'word_count': random.randint(800, 2500),
        'date_analyzed': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    return jsonify({
        'status': 'success',
        'preview': preview
    })

@app.route('/analyze-content', methods=['POST'])
def analyze_content():
    try:
        content = None
        content_type = request.form.get('type', 'text')
        
        logger.info(f"Analyzing content: type={content_type}")
        
        # Extract content based on the type
        if content_type == 'text':
            # Direct text input
            content = request.form.get('content', '')
            logger.info(f"Processing direct text input: {len(content)} characters")
            
        elif content_type == 'url':
            # URL input - use QuantumToneCrawler to extract content
            url = request.form.get('content', '')
            logger.info(f"Processing URL: {url}")
            
            # Use the QuantumToneCrawler to extract content from the URL
            try:
                crawler = ToneCrawler()
                content = crawler.extract_content_from_url(url)
                logger.info(f"Extracted {len(content)} characters from URL")
            except Exception as e:
                logger.error(f"Error extracting content from URL: {str(e)}")
                return jsonify({'status': 'error', 'message': f'Failed to extract content from URL: {str(e)}'})
                
        elif content_type == 'file':
            # File upload
            if 'file' not in request.files:
                logger.error("No file part in the request")
                return jsonify({'status': 'error', 'message': 'No file part in the request'})
                
            file = request.files['file']
            if file.filename == '':
                logger.error("No file selected")
                return jsonify({'status': 'error', 'message': 'No file selected'})
                
            # Read the file content
            try:
                content = file.read().decode('utf-8')
                logger.info(f"Read {len(content)} characters from uploaded file")
            except Exception as e:
                logger.error(f"Error reading file: {str(e)}")
                return jsonify({'status': 'error', 'message': f'Failed to read file: {str(e)}'})
        
        # Check if we have valid content to analyze
        if not content or len(content.strip()) == 0:
            logger.error("No content to analyze")
            return jsonify({'status': 'error', 'message': 'No content to analyze'})
        
        # Initialize the Neural Tone Mapper and analyze the content
        logger.info("Initializing NeuralToneMapper")
        mapper = NeuralToneMapper()
        
        # Analyze the text
        logger.info("Analyzing text with NeuralToneMapper")
        raw_analysis = mapper.analyze_text(content)
        logger.info(f"Raw analysis obtained: {list(raw_analysis.keys())}")
        
        # Format the analysis for display
        formatted_analysis = mapper.format_analysis_for_display(raw_analysis)
        logger.info("Analysis formatted for display")
        
        # Store in workflow data
        workflow.tone_analysis = formatted_analysis
        
        # Return the formatted analysis
        return jsonify(formatted_analysis)
        
    except Exception as e:
        logger.error(f"Error in tone analysis: {str(e)}")
        return jsonify({'status': 'error', 'message': f'An error occurred during analysis: {str(e)}'})

@app.route('/save-strategy', methods=['POST'])
def save_strategy():
    """Save the content strategy and schedule"""
    strategy_data = request.get_json()
    if strategy_data:
        workflow.content_strategy = strategy_data
        logger.info(f"Saved content strategy: {strategy_data}")
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'No strategy data provided'})

@app.route('/crawl-and-analyze', methods=['POST'])
def crawl_and_analyze():
    """
    Step 4a: Takes the URLs from step 1 and topics from step 3
    Uses the QuantumUniversalCrawler to extract key points from all data sources
    """
    if not workflow.data_sources:
        return jsonify({'status': 'error', 'message': 'No data sources available to crawl'})
    
    # Get all source URLs from step 1
    source_urls = [source['url'] for source in workflow.data_sources if source.get('url')]
    if not source_urls:
        return jsonify({'status': 'error', 'message': 'No valid URLs found in data sources'})
    
    logger.info(f"Crawling {len(source_urls)} sources")
    
    # Initialize the QuantumUniversalCrawler
    try:
        # Get the topic from the content strategy (step 3)
        topic = ''
        if workflow.content_strategy:
            topic = workflow.content_strategy.get('primary_topic', '')
        
        if not topic:
            return jsonify({
                'status': 'error',
                'message': 'No topic provided. Please set a primary topic in the content strategy first (step 3).'
            })
        
        logger.info(f"Using topic for relevance filtering: {topic}")
        
        # Initialize and use the QuantumUniversalCrawler
        crawler = UniversalCrawler(topic=topic, max_pages_per_domain=3)
        
        # Process all source URLs from step 1
        all_crawl_data = []
        all_key_insights = []
        all_key_topics = set([topic])  # Start with the main topic
        all_supporting_data = {
            "statistics": [],
            "case_studies": [],
            "quotes": []
        }
        
        # Crawl each URL
        for url in source_urls[:5]:  # Limit to first 5 URLs for performance
            try:
                logger.info(f"Crawling source: {url}")
                
                # Perform the crawl with the topic for relevance filtering
                crawl_result = crawler.crawl(url)
                
                # Handle the result correctly (crawl returns single result or list of results)
                if isinstance(crawl_result, list):
                    if not crawl_result:
                        logger.warning(f"No content crawled from {url}")
                        continue
                    crawl_data = crawl_result[0]
                else:
                    crawl_data = crawl_result
                    
                # Make sure we have the content to analyze
                if not hasattr(crawl_data, 'content') or not crawl_data.content:
                    logger.warning(f"No content extracted from {url}")
                    continue
                
                # Process the content
                content = crawl_data.content
                
                # Structure the results using our utility functions
                url_insights = extract_key_insights(crawler, content, topic)
                url_topics = extract_topics(crawler, content, topic)
                url_supporting_data = extract_supporting_data(crawler, content, topic)
                
                # Collect data from this URL
                all_crawl_data.append({
                    "url": url,
                    "content": content[:3000],  # Limit content size
                    "insights": url_insights,
                    "confidence": getattr(crawl_data, 'confidence_score', 0.5)
                })
                
                # Collect insights, avoiding duplicates
                for insight in url_insights:
                    if insight not in all_key_insights:
                        all_key_insights.append(insight)
                
                # Collect topics, avoiding duplicates
                for t in url_topics:
                    all_key_topics.add(t)
                
                # Collect supporting data, avoiding duplicates
                for key in url_supporting_data:
                    for item in url_supporting_data[key]:
                        if item not in all_supporting_data[key]:
                            all_supporting_data[key].append(item)
                
                logger.info(f"Successfully crawled {url}")
                
            except Exception as e:
                logger.error(f"Error crawling {url}: {str(e)}")
                # Continue with next URL
        
        # Save all the crawled data to the workflow
        workflow.crawled_data = {
            "sources": source_urls,
            "crawl_date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "key_topics": list(all_key_topics),
            "key_insights": all_key_insights[:10],  # Limit insights
            "supporting_data": all_supporting_data,
            "crawled_content": all_crawl_data
        }
        
        logger.info(f"Crawling complete. Processed {len(all_crawl_data)} sources.")
        logger.info(f"Found {len(all_key_insights)} key insights and {len(all_key_topics)} topics")
        
        return jsonify({
            'status': 'success', 
            'crawled_data': {
                'source_count': len(source_urls),
                'processed_count': len(all_crawl_data),
                'insight_count': len(all_key_insights),
                'topic_count': len(all_key_topics)
            }
        })
        
    except Exception as e:
        logger.error(f"Error during crawling process: {str(e)}")
        
        # Fallback to simulated data if crawling fails completely
        logger.warning("Using fallback simulated data due to crawling error")
        workflow.crawled_data = {
            "sources": source_urls,
            "crawl_date": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "key_topics": [
                "Content creation efficiency",
                "AI writing assistants",
                "Voice and tone consistency",
                "Content strategy automation",
                "Audience targeting"
            ],
            "key_insights": [
                "Companies using AI for content creation see 3x higher output",
                "Consistent voice across platforms increases brand recognition by 40%",
                "Personalized content generates 18% higher engagement rates",
                "Strategic content calendars improve team efficiency by 25%",
                "Data-driven content decisions lead to 30% higher conversion rates"
            ],
            "supporting_data": {
                "statistics": ["74% of marketers struggle with content consistency", 
                              "AI can reduce content production time by up to 67%",
                              "Content teams spend 33% of time on administrative tasks"],
                "case_studies": ["How Company X increased content output by 300%",
                               "Agency Y's content personalization strategy results"]
            },
            "error": str(e)
        }
        
        logger.info("Using fallback crawled data")
        return jsonify({
            'status': 'warning', 
            'message': f'Error during crawling: {str(e)}. Using fallback data.',
            'crawled_data': {
                'source_count': len(source_urls),
                'processed_count': 0,
                'insight_count': 5,
                'topic_count': 5
            }
        })

@app.route('/generate-article', methods=['POST'])
def generate_article():
    """
    Step 4 (c): Combines all collected data from previous steps to create a 4000-word article
    - Takes URLs and data from step 1 (via QuantumUniversalCrawler extraction in step 4a)
    - Takes tone analysis from step 2 
    - Uses topics and content strategy from step 3
    """
    if request.method == 'POST':
        try:
            # Get the article generator based on settings
            generator_type = request.form.get('generator_type', 'auto')
            article_generator = get_article_generator(generator_type=generator_type)
            
            # Generate the article
            topic = workflow.content_strategy.get('content_focus', 'General technology')
            style_profile = workflow.tone_analysis
            source_material = [
                {"content": entry, "relevance": 0.95} 
                for entry in workflow.crawled_data.get('sections', [])
            ]
            
            generated_article = article_generator.generate_article(
                topic=topic,
                style_profile=style_profile,
                source_material=source_material
            )
            
            workflow.generated_article = generated_article
            
            # Save to session
            session['article'] = generated_article
            session['workflow'] = workflow.__dict__
            
            return jsonify({
                'success': True,
                'message': 'Article generated successfully',
                'article': generated_article
            })
            
        except Exception as e:
            logger.error(f"Error generating article: {str(e)}")
            return jsonify({
                'success': False,
                'message': f"Error generating article: {str(e)}"
            }), 500
    else:
        return redirect(url_for('generate_content'))

@app.route('/article-preview')
def article_preview():
    """Preview the generated article"""
    if not workflow.generated_article:
        logger.error("No generated article found in workflow")
        return redirect('/onboarding/step4')
    
    # Pass article data directly to the template instead of relying on session storage
    logger.info("Rendering article preview page with article data")
    return render_template('article_preview.html', article_data=workflow.generated_article.get('article', {}))

# V2 Workflow Endpoints

@app.route('/v2/')
def start_v2():
    """Start of the reorganized workflow - Step 1: Content Strategy"""
    # Reset workflow data when starting from scratch
    global workflow
    workflow = WorkflowData()
    workflow.is_v2_workflow = True
    workflow.current_step = 1
    logger.info("Starting V2 workflow (reorganized order)")
    return jsonify({"status": "success", "message": "V2 workflow initialized"})

@app.route('/v2/step1')
def content_strategy_v2():
    """Step 1 (V2): Content Strategy and Scheduling"""
    workflow.current_step = 1
    return render_template('onboarding/step3_content_strategy.html', step=1, total_steps=4, is_v2=True)

@app.route('/v2/step2')
def data_sources_v2():
    """Step 2 (V2): Data Sources with Topic Guidance"""
    if not workflow.content_strategy:
        # Redirect to step 1 if content strategy not defined
        logger.warning("Attempted to access step 2 without completing step 1")
        return redirect('/v2/step1')
    
    workflow.current_step = 2
    return render_template('onboarding/step1_data_sources.html', 
                          step=2, 
                          total_steps=4, 
                          sources=workflow.data_sources, 
                          content_strategy=workflow.content_strategy,
                          is_v2=True)

@app.route('/v2/step3')
def writing_style_v2():
    """Step 3 (V2): Writing Style Analysis"""
    workflow.current_step = 3
    return render_template('onboarding/step2_writing_style_analysis.html', step=3, total_steps=4, is_v2=True)

@app.route('/v2/step4')
def generate_content_v2():
    """Step 4 (V2): Content Generation"""
    workflow.current_step = 4
    return render_template('onboarding/step4_article_generation.html', 
                          step=4, 
                          total_steps=4,
                          data_sources=workflow.data_sources,
                          tone_analysis=workflow.tone_analysis,
                          content_strategy=workflow.content_strategy,
                          is_v2=True)

@app.route('/add-source-with-topic', methods=['POST'])
def add_source_with_topic():
    """Add a source to the data sources list with topic relevance"""
    source_url = request.form.get('source_url', '')
    source_type = request.form.get('source_type', 'article')
    topic_relevance = request.form.get('topic_relevance', '')
    
    if source_url:
        new_source = {
            'url': source_url,
            'type': source_type,
            'topic_relevance': topic_relevance,
            'added': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        workflow.data_sources.append(new_source)
        logger.info(f"Added source with topic relevance: {source_url} ({source_type}) - Topic: {topic_relevance}")
    
    return jsonify({
        'status': 'success',
        'message': f'Source added with topic relevance: {topic_relevance}',
        'sources': workflow.data_sources,
        'count': len(workflow.data_sources)
    })

@app.route('/topic-guided-crawl', methods=['POST'])
def topic_guided_crawl():
    """Crawl sources with topic guidance for better relevance"""
    try:
        # Validate workflow state
        if not workflow.data_sources:
            return jsonify({
                'status': 'error',
                'message': 'No data sources defined'
            })
        
        if not workflow.content_strategy:
            return jsonify({
                'status': 'error',
                'message': 'Content strategy not defined'
            })
        
        # Extract topics from strategy for relevance scoring
        primary_topic = workflow.content_strategy.get('primary_topic', 'General Content')
        content_pillars = workflow.content_strategy.get('content_pillars', [])
        
        # Initialize crawler with the primary topic
        crawler = UniversalCrawler(topic=primary_topic)
        
        # Crawl sources with topic guidance
        crawl_results = []
        for source in workflow.data_sources:
            url = source.get('url', '')
            if not url:
                continue
                
            logger.info(f"Crawling source with topic guidance: {url}")
            
            # Use the UniversalCrawler to extract content
            crawl_result = crawler.crawl(url)
            
            if crawl_result.status == 'success':
                # Calculate topic relevance score
                content = crawl_result.content
                
                # Simple relevance scoring - count occurrences of topics
                relevance_score = 0
                if primary_topic and primary_topic.lower() in content.lower():
                    relevance_score += 5
                    logger.info(f"  Primary topic match in content (+5)")
                
                for pillar in content_pillars:
                    if pillar.lower() in content.lower():
                        relevance_score += 3
                        logger.info(f"  Content pillar match: {pillar} (+3)")
                
                # Convert CrawlResult to dictionary for JSON serialization
                result_dict = {
                    'url': crawl_result.url,
                    'content': crawl_result.content,
                    'status': crawl_result.status,
                    'word_count': crawl_result.word_count,
                    'source': crawl_result.source,
                    'error_reason': crawl_result.error_reason,
                    'confidence_score': crawl_result.confidence_score,
                    'timestamp': crawl_result.timestamp,
                    'topic_relevance': relevance_score,
                    'source_type': source.get('type', 'article'),
                    'topic_pillar': source.get('topic_relevance', '')
                }
                
                logger.info(f"  Content extracted: {result_dict['word_count']} words")
                logger.info(f"  Topic relevance score: {relevance_score}")
                
                crawl_results.append(result_dict)
            else:
                logger.error(f"  Failed to crawl {url}: {crawl_result.error_reason or 'Unknown error'}")
        
        # Sort results by relevance
        crawl_results.sort(key=lambda x: x.get('topic_relevance', 0), reverse=True)
        
        # Store in workflow data
        workflow.crawled_data = {
            'sources': crawl_results,
            'count': len(crawl_results),
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'topic_guided': True
        }
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully crawled {len(crawl_results)} sources with topic guidance',
            'sources': crawl_results,
            'count': len(crawl_results)
        })
        
    except Exception as e:
        logger.error(f"Error in topic-guided-crawl: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })

from app.article_generator import generate_article_logic

@app.route('/generate-article-v2', methods=['POST'])
def generate_article_v2():
    """Generate an article with the reorganized workflow approach"""
    try:
        # Validate workflow state
        if not workflow.data_sources:
            return jsonify({
                'status': 'error',
                'message': 'No data sources defined'
            })
            
        if not workflow.tone_analysis:
            return jsonify({
                'status': 'error',
                'message': 'Writing style analysis not completed'
            })
            
        if not workflow.content_strategy:
            return jsonify({
                'status': 'error',
                'message': 'Content strategy not defined'
            })
            
        if not workflow.crawled_data or not workflow.crawled_data.get('sources'):
            # If no crawled data, perform a topic-guided crawl first
            logger.info("No crawled data found, performing topic-guided crawl")
            crawl_response = topic_guided_crawl()
            crawl_data = json.loads(crawl_response.get_data(as_text=True))
            if crawl_data.get('status') != 'success':
                return jsonify({
                    'status': 'error',
                    'message': 'Failed to crawl sources: ' + crawl_data.get('message', 'Unknown error')
                })
        
        # Ensure tone analysis has the required keys
        tone_analysis = workflow.tone_analysis.get('analysis', {}).get('voice_character', {})
        tone_analysis['humor'] = tone_analysis.get('tone', 0)
        tone_analysis['formality'] = tone_analysis.get('formality', 50)
        tone_analysis['enthusiasm'] = tone_analysis.get('complexity', 50)
        
        # Generate article with topic guidance
        article = generate_article_logic(tone_analysis)
        
        # Store in workflow data
        workflow.generated_article = article
        
        return jsonify({
            'status': 'success',
            'message': 'Article generated successfully',
            'article': article,
            'success': True
        })
        
    except Exception as e:
        logger.error(f"Error in generate-article-v2: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}',
            'success': False
        })

@app.route('/workflow-version', methods=['GET'])
def workflow_version():
    """Return the current workflow version"""
    is_v2 = getattr(workflow, 'is_v2_workflow', False)
    return jsonify({
        'version': 'v2' if is_v2 else 'v1',
        'description': 'Reorganized workflow with content strategy first' if is_v2 else 'Original 4-step workflow',
        'current_step': workflow.current_step
    })

@app.route('/submit-content-strategy', methods=['POST'])
def submit_content_strategy():
    """Submit content strategy for the workflow"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['primary_topic', 'content_pillars', 'target_audience']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                })
        
        # Store content strategy in workflow data
        workflow.content_strategy = {
            'primary_topic': data.get('primary_topic', ''),
            'content_pillars': data.get('content_pillars', []),
            'target_audience': data.get('target_audience', ''),
            'publishing_frequency': data.get('publishing_frequency', 'Weekly'),
            'content_types': data.get('content_types', []),
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        logger.info(f"Content strategy submitted: {workflow.content_strategy['primary_topic']}")
        
        # For v2 workflow, update the step
        if workflow.is_v2_workflow and workflow.current_step == 1:
            workflow.current_step = 2
        
        return jsonify({
            'status': 'success',
            'message': 'Content strategy submitted successfully',
            'content_strategy': workflow.content_strategy
        })
        
    except Exception as e:
        logger.error(f"Error in submit-content-strategy: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })

@app.route('/analyze-writing-style', methods=['POST'])
def analyze_writing_style():
    """Analyze writing style from text input"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if 'text' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: text'
            })
        
        text = data.get('text', '')
        source_type = data.get('source_type', 'direct_input')
        
        if not text:
            return jsonify({
                'status': 'error',
                'message': 'Text cannot be empty'
            })
        
        # Initialize tone analyzer
        if tone_mapper_available:
            tone_analyzer = NeuralToneMapper()
            logger.info("Using NeuralToneMapper for writing style analysis")
        else:
            # Fallback to simulated analysis
            logger.warning("NeuralToneMapper not available, using simulated analysis")
            tone_analyzer = {
                'analyze': lambda text: {
                    'voice_character': {
                        'formality': 'moderate',
                        'tone': 'informative',
                        'perspective': 'third_person',
                        'complexity': 'advanced'
                    },
                    'linguistic_patterns': {
                        'sentence_structure': 'complex',
                        'vocabulary_richness': 'high',
                        'transition_style': 'logical',
                        'pacing': 'measured'
                    },
                    'content_architecture': {
                        'organization': 'thesis_support',
                        'paragraph_structure': 'topic_development',
                        'information_density': 'high',
                        'argument_style': 'evidence_based'
                    }
                }
            }
        
        # Analyze text
        analysis_result = tone_analyzer.analyze(text) if tone_mapper_available else tone_analyzer['analyze'](text)
        
        # Store in workflow data
        workflow.tone_analysis = {
            'voice_character': analysis_result.get('voice_character', {}),
            'linguistic_patterns': analysis_result.get('linguistic_patterns', {}),
            'content_architecture': analysis_result.get('content_architecture', {}),
            'source_type': source_type,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        logger.info("Writing style analysis completed")
        
        # For v2 workflow, update the step
        if workflow.is_v2_workflow and workflow.current_step == 3:
            workflow.current_step = 4
        
        return jsonify({
            'status': 'success',
            'message': 'Writing style analyzed successfully',
            'analysis': workflow.tone_analysis
        })
        
    except Exception as e:
        logger.error(f"Error in analyze-writing-style: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })

# Create a blueprint for workflow routes
workflow_bp = Blueprint('workflow', __name__, url_prefix='/api/workflow')

@workflow_bp.route('/start', methods=['POST'])
def start_workflow_api():
    workflow_id = str(uuid.uuid4())
    session['workflow_id'] = workflow_id
    return jsonify({
        'workflow_id': workflow_id,
        'initial_config': {
            'workflow_version': '2.0',
            'supported_features': [
                'topic_input', 
                'avatar_upload', 
                'data_sources', 
                'tone_sources', 
                'article_generation'
            ]
        }
    })

@workflow_bp.route('/<workflow_id>/topic', methods=['POST'])
def submit_topic_api(workflow_id):
    data = request.json
    # Placeholder implementation
    return jsonify({
        'status': 'success', 
        'message': 'Topic submitted successfully',
        'topic': data
    })

@workflow_bp.route('/<workflow_id>/avatar', methods=['POST'])
def upload_avatar_api(workflow_id):
    data = request.json
    # Placeholder implementation
    return jsonify({
        'status': 'success', 
        'message': 'Avatar uploaded successfully',
        'avatar': data
    })

@workflow_bp.route('/<workflow_id>/key-data-sources', methods=['POST'])
def add_data_sources_api(workflow_id):
    data = request.json
    # Placeholder implementation
    return jsonify({
        'status': 'success', 
        'message': 'Data sources added successfully',
        'sources': data.get('urls', [])
    })

@workflow_bp.route('/<workflow_id>/tone-analysis', methods=['POST'])
def add_tone_sources_api(workflow_id):
    data = request.json
    # Placeholder implementation
    return jsonify({
        'status': 'success', 
        'message': 'Tone sources added successfully',
        'sources': data.get('urls', [])
    })

@workflow_bp.route('/<workflow_id>/generate-article', methods=['POST'])
def generate_article_api(workflow_id):
    # Placeholder implementation
    return jsonify({
        'status': 'success',
        'article': {
            'text': 'Sample generated article about AI in Healthcare',
            'word_count': 250
        }
    })

@workflow_bp.route('/<workflow_id>/validate-article', methods=['POST'])
def validate_article_api(workflow_id):
    data = request.json
    # Placeholder implementation
    return jsonify({
        'status': 'success',
        'message': 'Article validated',
        'edits': data.get('edits', {})
    })

# Ensure blueprint is registered before running the app
app.register_blueprint(workflow_bp)

if __name__ == "__main__":
    print("Starting enhanced workflow test...")
    
    # Print out registered routes
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.rule}")
    
    app.run(host='0.0.0.0', port=8004, debug=True)
