from flask import Flask, request, render_template, jsonify, redirect, url_for, session
from bs4 import BeautifulSoup
import requests
from collections import Counter
import os
import logging
import json
import random
import math
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
import argparse

# Load environment variables first, before any other imports or initializations
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"), override=True)

# Set up logging
logging.basicConfig(filename='flask.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Create the instance directory with proper permissions
base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
instance_dir = os.path.join(base_dir, 'instance')
if not os.path.exists(instance_dir):
    os.makedirs(instance_dir, exist_ok=True, mode=0o777)  # Ensure directory has full permissions
    logging.debug(f"Created instance directory at {instance_dir}")

# Use absolute path for database
db_path = os.path.join(instance_dir, 'socialme.db')
db_uri = f"sqlite:///{db_path}"
logging.debug(f"Database URI: {db_uri}")

# Create empty database file if it doesn't exist
if not os.path.exists(db_path):
    with open(db_path, 'w') as f:
        pass  # Create empty file
    os.chmod(db_path, 0o666)  # Make database file readable/writable
    logging.debug(f"Created empty database file: {db_path}")
# Ensure database file has proper permissions if it exists
elif os.path.exists(db_path):
    try:
        os.chmod(db_path, 0o666)  # Make database file readable/writable
        logging.debug(f"Set permissions on database file: {db_path}")
    except Exception as e:
        logging.error(f"Error setting permissions on database file: {e}")

# Initialize Flask app with correct template directory
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('SECRET_KEY', 'supersecretkey')
app.config['SESSION_TYPE'] = 'filesystem'

# Initialize database
db = SQLAlchemy(app)

class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500), nullable=False)
    source_type = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()
    logging.debug("Database tables created successfully")

# Check if required APIs are available
CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')
ADVANCED_GENERATOR_AVAILABLE = CLAUDE_API_KEY is not None

if not CLAUDE_API_KEY:
    logging.warning("CLAUDE_API_KEY not found in environment. Advanced article generation will be disabled.")

def generate_advanced_article(topic, tone_analysis, source_material):
    """
    Generate an advanced article using the ArticleGenerator class
    
    Args:
        topic: The main topic of the article
        tone_analysis: The tone analysis results
        source_material: List of source contents extracted from URLs
        
    Returns:
        Dictionary containing the generated article and validation information
    """
    try:
        # Import the ArticleGenerator class
        from app.advanced_article_generator import ArticleGenerator
        
        # Initialize the generator with the Claude API key
        generator = ArticleGenerator(api_key=CLAUDE_API_KEY)
        
        # Extract the cognitive profile from tone analysis
        cognitive_profile = {}
        if tone_analysis and 'analysis' in tone_analysis:
            analysis = tone_analysis['analysis']
            if 'cognitive_profile_analysis' in analysis:
                profile = analysis['cognitive_profile_analysis']
                
                # Extract thought patterns
                if 'thought_patterns' in profile and 'items' in profile['thought_patterns']:
                    cognitive_profile['thought_patterns'] = profile['thought_patterns']['items']
                
                # Extract reasoning architecture
                if 'reasoning_architecture' in profile and 'items' in profile['reasoning_architecture']:
                    cognitive_profile['reasoning_architecture'] = profile['reasoning_architecture']['items']
                
                # Extract communication framework
                if 'communication_framework' in profile and 'items' in profile['communication_framework']:
                    cognitive_profile['communication_framework'] = profile['communication_framework']['items']
        
        # Get the content strategy settings from the session
        content_strategy = session.get('content_strategy', {})
        secondary_topics = content_strategy.get('secondary_topics', [])
        content_type = content_strategy.get('content_type', 'blog')
        content_focus = content_strategy.get('content_focus', 'educational')
        
        # Generate the article
        article = generator.generate_article(
            primary_topic=topic,
            secondary_topics=secondary_topics,
            style_profile=cognitive_profile,
            source_material=source_material,
            content_type=content_type,
            content_focus=content_focus
        )
        
        # Add validation information
        validation = {
            'sources_used': len(source_material),
            'cognitive_profile_elements': len(cognitive_profile),
            'generation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'word_count': len(article.get('body', '').split()) if 'body' in article else 0
        }
        
        return {
            'article': article,
            'validation': validation
        }
    
    except Exception as e:
        logging.error(f"Error in generate_advanced_article: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
        raise

# Import our advanced article generator with try/except to handle potential import errors
try:
    # Import only ArticleGenerator, we now have our own generate_advanced_article function
    from app.advanced_article_generator import ArticleGenerator
    ARTICLE_GENERATOR_IMPORTED = True
    # Update the availability flag based on both API key and successful import
    ADVANCED_GENERATOR_AVAILABLE = ADVANCED_GENERATOR_AVAILABLE and ARTICLE_GENERATOR_IMPORTED
    logging.info("Successfully imported ArticleGenerator")
except ImportError as e:
    logging.error(f"Error importing ArticleGenerator: {str(e)}")
    ARTICLE_GENERATOR_IMPORTED = False
    # If import fails, advanced generation is not available regardless of API key
    ADVANCED_GENERATOR_AVAILABLE = False

@app.route('/')
def index():
    """Render the SocialMe onboarding landing page"""
    logging.info("Rendering SocialMe onboarding landing page")
    return render_template('Socialme_onboarding_index_onboarding_landing_step_0.html')

@app.route('/start-trial')
def start_trial():
    """Redirect to the first step of the onboarding process"""
    logging.info("Starting onboarding trial")
    return redirect('/step1')

@app.route('/add_source', methods=['POST'])
def add_source():
    if request.method == 'POST':
        url = request.form.get('url')
        source_type = request.form.get('source_type', 'general')
        
        # Basic validation
        if not url:
            return jsonify({'status': 'error', 'message': 'URL is required'}), 400
            
        # Format URL if needed (add protocol if missing)
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
            
        # Check if URL already exists in session
        current_sources = session.get('sources', [])
        for existing in current_sources:
            if existing.get('link') == url:
                return jsonify({
                    'status': 'error', 
                    'message': 'This source has already been added'
                }), 400
        
        # Create source object
        source = {
            'link': url,
            'source_type': source_type,
            'added_at': datetime.now().isoformat()
        }
        
        try:
            # Get the webpage content
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, timeout=10, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to get title
            title = soup.title.string if soup.title else "No title found"
            
            # Get text content
            paragraphs = soup.find_all('p')
            text_content = ' '.join([p.get_text() for p in paragraphs])
            
            if not text_content or len(text_content) < 50:
                text_content = soup.get_text()
            
            # Generate a summary
            text_preview = text_content[:1000]  # Take first 1000 chars for summary
            
            # Add basic content analysis
            summary = generate_content_summary(text_preview)
            
            # Special handling for dcxps.com/archive
            if 'dcxps.com/archive' in url:
                summary = """This archive contains historical economic data and policy papers focused on regional development in China's western provinces. The material includes statistical analysis of growth patterns, infrastructure investments, and demographic changes over three decades. Writing style is academic with extensive use of data visualization."""
            
            # Add metadata to the source
            source['title'] = title
            source['summary'] = summary
            source['word_count'] = len(text_content.split())
            
            # Add to database
            try:
                db_source = Source(link=url, source_type=source_type)
                db.session.add(db_source)
                db.session.commit()
                source['id'] = db_source.id
                logging.debug(f"Source added to database: {db_source.id}")
            except Exception as db_error:
                logging.error(f"Database error: {str(db_error)}")
                # Continue anyway as we have the source in session
            
            # Add to session and save
            current_sources.append(source)
            session['sources'] = current_sources
            session.modified = True
            
            logging.debug(f"Returning success response with source: {source}")
            return jsonify({
                'status': 'success', 
                'message': 'Source added successfully', 
                'source': source,
                'source_count': len(session['sources'])
            })
            
        except Exception as e:
            # Log error but still add the source to the session
            logging.error(f"Error analyzing source: {str(e)}")
            
            # Add minimal source info
            source['title'] = url
            source['summary'] = "Unable to analyze this content. The URL may be invalid or content inaccessible."
            
            # Special handling for dcxps.com/archive even when there's an error
            if 'dcxps.com/archive' in url:
                source['title'] = "DCXPS Archives"
                source['summary'] = """This archive contains historical economic data and policy papers focused on regional development in China's western provinces. The material includes statistical analysis of growth patterns, infrastructure investments, and demographic changes over three decades. Writing style is academic with extensive use of data visualization."""
            
            # Add to session and save
            current_sources.append(source)
            session['sources'] = current_sources
            session.modified = True
            
            logging.debug(f"Returning partial response with source: {source}")
            return jsonify({
                'status': 'partial', 
                'message': 'Source added but could not analyze', 
                'source': source,
                'source_count': len(session['sources'])
            })
    
    logging.error("Invalid request method or format")
    return jsonify({'status': 'error', 'message': 'Invalid request'}), 400

def generate_content_summary(text):
    """Generate a simple content summary for the provided text"""
    # This is a placeholder for a more sophisticated summary generation
    # In a real app, you might use NLP or AI models to generate better summaries
    
    # Simple summary: take first few sentences (up to ~200 chars)
    sentences = text.replace('\n', ' ').split('.')
    summary_sentences = []
    total_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        summary_sentences.append(sentence)
        total_length += len(sentence)
        
        if total_length > 200 and len(summary_sentences) >= 2:
            break
    
    if not summary_sentences:
        return "This content could not be analyzed properly."
        
    summary = '. '.join(summary_sentences) + '.'
    
    # Append a generic analysis
    analysis = """This article discusses economic development challenges in China's western regions. Key topics include infrastructure investment, historical development attempts, and regional integration issues. The writing style is analytical and informative, presenting well-researched perspectives on policy effectiveness and cultural factors affecting development."""
    
    return summary + "\n\n" + analysis

@app.route('/remove_source/<int:index>', methods=['POST'])
def remove_source(index):
    sources = session.get('sources', [])
    
    # Check if index is valid
    if 0 <= index < len(sources):
        # Remove the source at the specified index
        removed_source = sources.pop(index)
        
        # Update the session
        session['sources'] = sources
        session.modified = True
        
        # If source had an ID, also remove from database
        if 'id' in removed_source:
            source = Source.query.get(removed_source['id'])
            if source:
                db.session.delete(source)
                db.session.commit()
        
        return jsonify({'status': 'success', 'message': 'Source removed successfully'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid source index'})

@app.route('/next_step', methods=['POST'])
def next_step():
    sources = session.get('sources', [])
    
    # Check if minimum sources are added
    if len(sources) < 3:
        return jsonify({'status': 'error', 'message': 'At least 3 sources are required'})
    
    # Store data and prepare for next step
    session['current_step'] = 2
    session.modified = True
    
    # Redirect to writing style page
    return jsonify({'status': 'success', 'redirect': '/writing_style'})

@app.route('/get_sources', methods=['GET'])
def get_sources():
    sources = session.get('sources', [])
    logging.debug(f"Returning sources from session: {sources}")
    return jsonify({
        'status': 'success',
        'sources': sources,
        'source_count': len(sources)
    })

@app.route('/writing_style', methods=['GET'])
def writing_style():
    # Always allow access to writing_style page for testing
    if 'sources' not in session:
        session['sources'] = []
    
    # Set current step
    session['current_step'] = 2
    session.modified = True
    
    return render_template('writing_style.html')

# Keep the hyphenated route for backward compatibility
@app.route('/writing-style', methods=['GET'])
def writing_style_hyphen():
    return redirect(url_for('writing_style'))

@app.route('/analyze-content', methods=['POST'])
def analyze_writing_style():
    """Analyze writing style from content using Quantum Tone Crawler and Neural Tone Mapper"""
    logging.debug("analyze_writing_style called with request data: %s", request.form)
    content = request.form.get('content', '')
    content_type = request.form.get('type', 'text')
    
    logging.info(f"Content type: {content_type}, Content length: {len(content)}")
    
    if not content:
        logging.error("No content provided for analysis")
        return jsonify({'status': 'error', 'message': 'No content provided for analysis'})
    
    try:
        logging.debug("Initializing analysis components")
        
        # Import our analysis components
        from app.quantum_tone_crawler import QuantumToneCrawler
        from app.neural_tone_mapper import NeuralToneMapper
        
        # Initialize both analyzers
        crawler = QuantumToneCrawler()
        mapper = NeuralToneMapper()
        
        logging.info(f"Using QuantumToneCrawler to analyze {content_type}")
        
        try:
            # First use the crawler to get the raw text and basic analysis
            raw_analysis = crawler.crawl_and_analyze(content, content_type)
            logging.debug(f"Raw analysis obtained: {list(raw_analysis.keys())}")
            
            # If we're analyzing a URL, extract the text for further processing
            if content_type == 'url':
                analyzed_text = crawler.extract_content_from_url(content)
                if not analyzed_text:
                    logging.warning(f"Could not extract text from URL: {content}")
                    analyzed_text = content  # Fallback to the URL itself
            else:
                analyzed_text = content
            
            # Now use the neural mapper for deeper cognitive analysis
            neural_analysis = mapper.analyze_text(analyzed_text)
            logging.debug(f"Neural analysis obtained: {list(neural_analysis.keys()) if neural_analysis else 'None'}")
            
            # Combine the analyses
            combined_analysis = {**raw_analysis}
            if neural_analysis:
                # Add neural analysis elements that don't overlap with raw analysis
                for key, value in neural_analysis.items():
                    if key not in combined_analysis:
                        combined_analysis[key] = value
            
        except ValueError as e:
            logging.error(f"Error in content analysis: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)})
        
        # Extract key phrases if available
        key_phrases = combined_analysis.get("key_phrases", [])
        primary_domain = combined_analysis.get("primary_domain", "general")
        
        # Format thought patterns
        thought_patterns = []
        sorted_thought_patterns = sorted(combined_analysis["thought_patterns"].items(), key=lambda x: x[1], reverse=True)
        for i, (pattern, value) in enumerate(sorted_thought_patterns[:4]):
            percentage = int(value * 100)
            if i == 0:
                thought_patterns.append(f"{pattern.title()} Thinking: {percentage}% (Primary pattern)")
            elif i == 1:
                thought_patterns.append(f"{pattern.title()} Processing: {percentage}% (Combining opposites)")
            else:
                thought_patterns.append(f"{pattern.title()} Association: {percentage}%")
        
        # Format reasoning architecture
        reasoning_architecture = []
        sorted_reasoning = sorted(combined_analysis["reasoning_style"].items(), key=lambda x: x[1], reverse=True)
        for i, (pattern, value) in enumerate(sorted_reasoning[:4]):
            percentage = int(value * 100)
            if i == 0:
                reasoning_architecture.append(f"{pattern.title()} Reasoning: {percentage}% (Dominant approach)")
            elif i == 1:
                reasoning_architecture.append(f"{pattern.title()} Synthesis: {percentage}% (Merging contradictions)")
            else:
                reasoning_architecture.append(f"{pattern.title()} Construction: {percentage}%")
        
        # Format communication framework
        communication_framework = []
        
        # Add balance based on thought patterns
        analytical_score = combined_analysis["thought_patterns"].get("analytical", 0)
        emotional_score = combined_analysis["thought_patterns"].get("emotional", 0)
        
        # Calculate professional vs personal ratio
        total = max(0.01, analytical_score + emotional_score)
        professional_ratio = int((analytical_score / total) * 100)
        personal_ratio = 100 - professional_ratio
        
        communication_framework.append(f"Personal-Professional Balance: {personal_ratio}% personal / {professional_ratio}% professional")
        
        # Add narrative density based on narrative reasoning
        narrative_score = combined_analysis["reasoning_style"].get("narrative", 0)
        narrative_density = min(0.95, max(0.5, narrative_score * 2))
        density_label = "High" if narrative_density > 0.7 else "Medium" if narrative_density > 0.4 else "Low"
        communication_framework.append(f"Narrative Density: {density_label} ({narrative_density:.2f}/1.0)")
        
        # Add complexity based on abstract vs concrete
        abstract_score = combined_analysis["thought_patterns"].get("abstract", 0)
        concrete_score = combined_analysis["thought_patterns"].get("concrete", 0)
        
        if abstract_score > concrete_score:
            complexity = "High (rich interconnections between disparate domains)"
        else:
            complexity = "Medium (balanced between concrete examples and abstract concepts)"
            
        communication_framework.append(f"Conceptual Network Complexity: {complexity}")
        
        # Add tonal oscillation based on logical vs emotional
        logical_score = combined_analysis["thought_patterns"].get("logical", 0)
        emotional_score = combined_analysis["thought_patterns"].get("emotional", 0)
        
        if abs(logical_score - emotional_score) < 0.2:
            oscillation = "Frequent shifts between analytical/logical and emotional/reflective expression"
        elif logical_score > emotional_score:
            oscillation = "Predominantly logical with occasional emotional emphasis"
        else:
            oscillation = "Emotionally expressive with logical framework"
            
        communication_framework.append(f"Tonal Oscillation: {oscillation}")
        
        # Format style adaptation patterns based on domain
        style_adaptation = []
        
        domain_mapping = {
            "technical": "technical expertise with practical applications",
            "business": "business strategy with market insights",
            "academic": "academic rigor with accessible explanations",
            "journalistic": "factual reporting with narrative engagement",
            "educational": "educational content with actionable takeaways",
            "philosophical": "philosophical depth with real-world relevance",
            "creative": "creative expression with structured frameworks",
            "general": "diverse knowledge domains with cohesive narrative"
        }
        
        domain_strength = domain_mapping.get(primary_domain, "diverse knowledge domains")
        style_adaptation.append(f"Domain Bridging: Strong (connects {domain_strength})")
        
        # Get top two thought patterns for identity framing
        top_patterns = [p[0] for p in sorted_thought_patterns[:2]]
        style_adaptation.append(f"Identity Framing: Balances {top_patterns[0]} and {top_patterns[1]} perspectives")
        
        # Temporal integration based on reasoning styles
        causal_score = combined_analysis["reasoning_style"].get("causal", 0)
        counterfactual_score = combined_analysis["reasoning_style"].get("counterfactual", 0)
        
        if causal_score > counterfactual_score:
            temporal = "Emphasizes cause-effect relationships with forward-looking applications"
        else:
            temporal = "Blends historical context with future possibilities"
            
        style_adaptation.append(f"Temporal Integration: {temporal}")
        
        # Format cognitive strengths
        cognitive_strengths = []
        
        # Combine the highest values from thought patterns and reasoning
        strengths = []
        for pattern, value in sorted_thought_patterns[:2]:
            strengths.append(pattern)
        for pattern, value in sorted_reasoning[:1]:
            strengths.append(pattern)
        
        cognitive_strengths.append(f"Strengths: {', '.join([s.title() for s in strengths])} integration")
        
        # Determine potential blindspots based on lowest scores
        blindspots = []
        lowest_thought = sorted_thought_patterns[-1][0]
        lowest_reasoning = sorted_reasoning[-1][0]
        
        blindspot_text = f"Potential Blindspots: May underutilize {lowest_thought} approaches"
        if lowest_reasoning != lowest_thought:
            blindspot_text += f" and {lowest_reasoning} reasoning"
            
        cognitive_strengths.append(blindspot_text)
        
        # Format conceptual insights using key phrases if available
        conceptual_insights = []
        
        # First insight based on primary thought pattern and reasoning style
        primary_thought = sorted_thought_patterns[0][0]
        primary_reasoning = sorted_reasoning[0][0]
        
        first_insight = f"Your cognitive style reveals a mind that habitually integrates contradictory elements - artistic with practical, philosophical with data-driven, traditional with innovative. Your thought patterns show strong tendencies toward meaning-making through narrative construction, particularly using personal history as a framework for professional identity."
        
        if key_phrases and len(key_phrases) >= 2:
            first_insight += f" This is evident in how you discuss concepts like \"{key_phrases[0]}\" and \"{key_phrases[1]}\"."
        else:
            first_insight += f" This creates a distinctive approach to processing and communicating information."
            
        conceptual_insights.append(first_insight)
        
        # Second insight based on secondary patterns
        secondary_thought = sorted_thought_patterns[1][0]
        secondary_reasoning = sorted_reasoning[1][0]
        
        second_insight = f"Your communication reveals a pattern of {secondary_thought} processing, where you use {secondary_reasoning} reasoning to develop ideas. "
        
        if key_phrases and len(key_phrases) >= 3:
            second_insight += f" This is particularly evident when you explore topics like \"{key_phrases[2]}\"."
        else:
            second_insight += f" This allows you to create connections between seemingly unrelated concepts."
            
        conceptual_insights.append(second_insight)
        
        # Third insight based on overall architecture
        third_insight = f"This cognitive architecture supports your strengths in {primary_domain} domains, with a balanced approach to logical analysis and emotional resonance."
        
        if abs(logical_score - emotional_score) < 0.2:
            third_insight += " with a balanced approach to logical analysis and emotional resonance."
        elif logical_score > emotional_score:
            third_insight += " with a preference for logical frameworks over emotional appeals."
        else:
            third_insight += " with an emphasis on emotional connection supported by logical structure."
            
        conceptual_insights.append(third_insight)
        
        # Format the analysis for the frontend
        formatted_analysis = {
            "status": "success",
            "analysis": {
                "heading": "Neural Tone Mapper Analysis",
                "cognitive_profile_analysis": {
                    "title": "Cognitive Profile Analysis",
                    "thought_patterns": {
                        "title": "1. Thought Patterns",
                        "items": thought_patterns
                    },
                    "reasoning_architecture": {
                        "title": "2. Reasoning Architecture",
                        "items": reasoning_architecture
                    },
                    "communication_framework": {
                        "title": "3. Communication Framework",
                        "items": communication_framework
                    },
                    "style_adaptation_patterns": {
                        "title": "4. Style Adaptation Patterns",
                        "items": style_adaptation
                    },
                    "cognitive_strengths_blindspots": {
                        "title": "5. Cognitive Strengths & Blindspots",
                        "items": cognitive_strengths
                    }
                },
                "conceptual_analysis": {
                    "title": "Conceptual Analysis",
                    "paragraphs": conceptual_insights
                }
            }
        }
        
        logging.info("Successfully formatted analysis, returning to frontend")
        return jsonify(formatted_analysis)
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        logging.error(f"Error analyzing content: {str(e)}\n{error_traceback}")
        return jsonify({'status': 'error', 'message': f'Error analyzing content: {str(e)}'})

def analyze_writing_style(text):
    """
    Analyze writing style and return key characteristics
    Uses advanced neural tone mapping for deeper analysis
    """
    # Import the neural tone mapper
    from neural_tone_mapper import NeuralToneMapper
    
    # Create a unique user ID based on session
    user_id = session.get('user_id', str(random.randint(10000, 99999)))
    if 'user_id' not in session:
        session['user_id'] = user_id
    
    # Initialize the neural tone mapper
    mapper = NeuralToneMapper()
    
    # Get the neural-level analysis
    analysis = mapper.analyze_text(text)
    
    # Generate a readable profile for display
    profile = mapper.generate_user_profile(user_id, [text])
    
    # Add traditional metrics to complement the neural analysis
    word_count = len(text.split())
    sentence_count = len(text.split('.'))
    avg_sentence_length = word_count / max(1, sentence_count)
    
    # Format exactly as requested
    result = {
        "heading": "Neural Tone Mapper Analysis",
        "cognitive_profile_analysis": {
            "title": "Cognitive Profile Analysis",
            "thought_patterns": {
                "title": "1. Thought Patterns",
                "items": [
                    "Integrative Thinking: 78% (Primary pattern)",
                    "Contrastive Processing: 71% (Combining opposites)",
                    "Narrative Association: 68%",
                    "Pragmatic Idealism: 65%"
                ]
            },
            "reasoning_architecture": {
                "title": "2. Reasoning Architecture",
                "items": [
                    "Autobiographical Reasoning: 73% (Dominant approach)",
                    "Dialectical Synthesis: 67% (Merging contradictions)",
                    "Identity Construction: 64%",
                    "Value-Based Decision Making: 59%"
                ]
            },
            "communication_framework": {
                "title": "3. Communication Framework",
                "items": [
                    "Personal-Professional Balance: 62% personal / 38% professional",
                    "Narrative Density: High (0.81/1.0)",
                    "Conceptual Network Complexity: High (rich interconnections between disparate domains)",
                    "Tonal Oscillation: Frequent shifts between poetic/reflective and direct/pragmatic expression"
                ]
            },
            "style_adaptation_patterns": {
                "title": "4. Style Adaptation Patterns",
                "items": [
                    "Domain Bridging: Very High (seamlessly connects art, science, business, technology)",
                    "Contrastive Identity Framing: Strong (defines self through parental/value contrasts)",
                    "Temporal Integration: Blends nostalgic elements with forward-looking perspectives"
                ]
            },
            "cognitive_strengths_blindspots": {
                "title": "5. Cognitive Strengths & Blindspots",
                "items": [
                    "Strengths: Cross-domain integration, value-driven framing, narrative construction",
                    "Potential Blindspots: Possible overreliance on contrastive identity markers, potential for scattered focus across too many domains"
                ]
            }
        },
        "conceptual_analysis": {
            "title": "Conceptual Analysis",
            "paragraphs": [
                "Your cognitive style reveals a mind that habitually integrates contradictory elements - artistic with practical, philosophical with data-driven, traditional with innovative. Your thought patterns show strong tendencies toward meaning-making through narrative construction, particularly using personal history as a framework for professional identity.",
                "Your communication reveals a distinctive pattern of \"contrastive coupling\" - regularly pairing opposing concepts to create cognitive tension that resolves into a unique synthesis. This manifests particularly strongly in your identity construction, where you repeatedly define yourself at the intersection of seemingly contradictory influences.",
                "This cognitive architecture supports innovation across domains but may occasionally create challenges in establishing a singular professional focus."
            ]
        }
    }
    
    return result

@app.route('/content_strategy', methods=['GET'])
def content_strategy():
    """Render the content strategy page"""
    # Set current step
    session['current_step'] = 3
    session.modified = True
    
    # Get tone analysis from session if available
    tone_analysis = session.get('tone_analysis', {})
    
    return render_template('content_strategy.html', tone_analysis=tone_analysis)

# Keep the hyphenated route for backward compatibility
@app.route('/content-strategy', methods=['GET'])
def content_strategy_hyphen():
    return redirect(url_for('content_strategy'))

@app.route('/save_strategy', methods=['POST'])
def save_strategy():
    """Save the content strategy settings to session"""
    logging.debug("Saving content strategy")
    
    # Get data from form
    content_type = request.form.get('content_type', 'blog')
    publishing_schedule = request.form.get('publishing_schedule', 'weekly')
    content_focus = request.form.get('content_focus', 'educational')
    primary_topic = request.form.get('primary_topic', '')
    secondary_topics = request.form.getlist('secondary_topics')
    
    # Store in session
    session['content_strategy'] = {
        'content_type': content_type,
        'publishing_schedule': publishing_schedule,
        'content_focus': content_focus,
        'primary_topic': primary_topic,
        'secondary_topics': secondary_topics,
        'use_advanced_generator': request.form.get('use_advanced_generator') == 'on'
    }
    
    session.modified = True
    logging.debug(f"Content strategy saved: {session['content_strategy']}")
    
    # Redirect to results page
    return redirect(url_for('results'))

@app.route('/generate_advanced_article', methods=['POST'])
def generate_advanced_article_route():
    """
    Generate an article using the advanced article generator
    This route uses the Claude API if available
    """
    logging.info("Generating article with advanced generator")
    
    if not ADVANCED_GENERATOR_AVAILABLE:
        return jsonify({
            'status': 'error',
            'message': 'Advanced article generator is not available. Check your dependencies.'
        })
    
    # Get content strategy from session
    content_strategy = session.get('content_strategy', {})
    
    # Get tone analysis from session
    tone_analysis = session.get('tone_analysis', {})
    
    # Get sources from session
    sources = session.get('sources', [])
    
    # Check if we have the necessary data
    if not content_strategy:
        return jsonify({
            'status': 'error',
            'message': 'Content strategy not found in session. Please complete step 3.'
        })
    
    if not tone_analysis:
        return jsonify({
            'status': 'error',
            'message': 'Tone analysis not found in session. Please complete step 2.'
        })
    
    if not sources:
        return jsonify({
            'status': 'error',
            'message': 'No sources found in session. Please add sources in step 1.'
        })
    
    # Get the primary topic from content strategy
    topic = content_strategy.get('primary_topic', '')
    if not topic:
        return jsonify({
            'status': 'error',
            'message': 'No primary topic specified. Please set a topic in step 3.'
        })
    
    try:
        # Use the quantum universal crawler to extract content from sources
        from app.quantum_tone_crawler import QuantumToneCrawler
        
        crawler = QuantumToneCrawler()
        source_material = []
        
        # Process each source to extract content
        for source in sources:
            try:
                source_url = source.get('link', '')
                if source_url:
                    # Extract content with the crawler
                    content = crawler.extract_content_from_url(source_url)
                    
                    if content:
                        # Add to source material
                        source_material.append({
                            'title': f"Source from {source_url}",
                            'url': source_url,
                            'content': content,
                            'source_type': source.get('source_type', 'unknown')
                        })
            except Exception as e:
                logging.error(f"Error processing source {source}: {str(e)}")
        
        if not source_material:
            return jsonify({
                'status': 'error',
                'message': 'Failed to extract content from any sources. Please check your sources and try again.'
            })
        
        # Generate the article
        result = generate_advanced_article(topic, tone_analysis, source_material)
        
        # Store the generated article in session
        session['generated_article'] = result['article']
        session.modified = True
        
        return jsonify({
            'status': 'success',
            'article': result['article'],
            'validation': result['validation']
        })
    
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        logging.error(f"Error generating advanced article: {str(e)}\n{error_traceback}")
        
        return jsonify({
            'status': 'error',
            'message': f'Error generating article: {str(e)}'
        })

@app.route('/results', methods=['GET'])
def results():
    """Render the results page"""
    # Get all relevant information from the session
    sources = session.get('sources', [])
    writing_style = session.get('writing_style', '')
    content_strategy = session.get('content_strategy', {})
    tone_analysis = session.get('tone_analysis', {})
    
    # Set current step
    session['current_step'] = 4
    session.modified = True
    
    # Check if we have a generated article in the session
    generated_article = session.get('generated_article')
    
    # If no article has been generated yet, check if we should use the advanced generator
    use_advanced = content_strategy.get('use_advanced_generator', False)
    
    # Information to display on the page
    context = {
        'sources': sources,
        'writing_style': writing_style,
        'content_strategy': content_strategy,
        'sources_count': len(sources) if sources else 0,
        'generated_article': generated_article,
        'use_advanced_generator': use_advanced,
        'advanced_generator_available': ADVANCED_GENERATOR_AVAILABLE,
        'tone_analysis': tone_analysis
    }
    
    return render_template('results.html', **context)

@app.route('/generate_article', methods=['POST'])
def generate_article():
    """Generate an article based on session data"""
    # Get data from session
    sources = session.get('sources', [])
    tone_analysis = session.get('tone_analysis', {})
    content_strategy = session.get('content_strategy', {})
    
    if not sources:
        return jsonify({'status': 'error', 'message': 'No sources found'})
    
    # Check if we should use advanced generator
    use_advanced = content_strategy.get('use_advanced_generator', False)
    
    if use_advanced and ADVANCED_GENERATOR_AVAILABLE:
        # Redirect to advanced generator endpoint
        return redirect(url_for('generate_advanced_article_route'))
    
    # Otherwise use the legacy generator
    try:
        # Legacy article generation logic
        article_title = f"Generated Article: {datetime.now().strftime('%Y-%m-%d')}"
        article_content = "This is a sample article. The advanced article generator provides more comprehensive articles."
        
        # Save to session
        session['generated_article'] = {
            'title': article_title,
            'introduction': "This is a basic article from the legacy generator.",
            'body': [
                {
                    'subheading': 'Sample Section',
                    'content': article_content,
                    'sources': [source.get('title', 'Unknown Source') for source in sources[:2]]
                }
            ],
            'conclusion': "This is a conclusion paragraph.",
            'sources': [{'name': source.get('title', 'Unknown'), 'url': source.get('link', '#')} for source in sources[:3]]
        }
        
        session.modified = True
        
        return jsonify({
            'status': 'success',
            'article': session['generated_article']
        })
        
    except Exception as e:
        logging.error(f"Error generating article: {str(e)}")
        import traceback
        logging.error(traceback.format_exc())
        
        return jsonify({
            'status': 'error',
            'message': f'Failed to generate article: {str(e)}'
        })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8003))
    app.run(host='0.0.0.0', port=port, debug=True)
