"""
Onboarding Workflow Routes

This module contains all the routes associated with the 4-step onboarding workflow.
"""

from flask import Blueprint, render_template, request, jsonify, redirect, session
import logging
import datetime
import random
import json

# Import the workflow data class
from app.models.workflow import WorkflowData
from app.crawlers.universal import UniversalCrawler
from app.crawlers.tone import ToneCrawler
from app.services.neural_tone_mapper import NeuralToneMapper
from app.generators.article import ArticleGenerator
from app.generators.factory import get_article_generator

# Configure logging
logger = logging.getLogger(__name__)

# Create a Blueprint for the onboarding routes
onboarding_bp = Blueprint('onboarding', __name__)

# Global workflow data
workflow = WorkflowData()

# ===== V1 WORKFLOW ROUTES (ORIGINAL ORDER) =====

@onboarding_bp.route('/')
def start():
    """Start of the workflow - Step 1: Data Sources"""
    # Reset workflow data when starting from scratch
    global workflow
    workflow.reset()  # Reset existing workflow instead of creating new one
    logger.info(f"Workflow reset - Workflow object ID: {id(workflow)}")
    return render_template('onboarding/step1_data_sources.html', step=1, sources=workflow.data_sources)

@onboarding_bp.route('/step1', methods=['GET', 'POST'])
def step1_data_sources():
    """Step 1: Data Sources"""
    logger.info(f"Step 1 route called. Method: {request.method}")
    logger.info(f"Step 1 - Current workflow data_sources: {workflow.data_sources}")
    
    if request.method == 'POST':
        # Process and store sources
        logger.info(f"Step 1 POST - Request JSON: {request.json}")
        sources = request.json.get('sources', [])
        logger.info(f"Step 1 POST - Received sources: {sources}")
        logger.info(f"Step 1 POST - Workflow object ID before update: {id(workflow)}")
        
        workflow.data_sources = sources
        logger.info(f"Step 1 POST - Updated workflow data_sources: {workflow.data_sources}")
        logger.info(f"Step 1 POST - Workflow object ID after update: {id(workflow)}")
        
        # Return success response
        return jsonify({'status': 'success', 'sources': sources})
    
    workflow.current_step = 1
    logger.info(f"Step 1 - Rendering template with {len(workflow.data_sources)} sources")
    return render_template('onboarding/step1_data_sources.html', step=1, sources=workflow.data_sources)

@onboarding_bp.route('/add-source', methods=['POST'])
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

@onboarding_bp.route('/preview-source', methods=['POST'])
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

@onboarding_bp.route('/analyze-writing-style', methods=['POST'])
def analyze_writing_style():
    """Analyze writing style from user input (mock endpoint for frontend compatibility)"""
    try:
        data = request.get_json()
        input_text = data.get('input', '')  # Frontend sends 'input' field
        method = data.get('method', 'text')
        
        if not input_text:
            return jsonify({
                'status': 'error',
                'message': 'Missing required field: input'
            })
        
        # Mock analysis results
        analysis_result = {
            'tone': 'Professional and Informative',
            'communicationStyle': 'Clear and Concise',
            'readabilityScore': '8.5/10',
            'complexityLevel': 'Intermediate',
            'recommendations': [
                'Maintain your clear and professional tone',
                'Use industry-specific terminology sparingly',
                'Break complex ideas into digestible paragraphs'
            ],
            'input_method': method,
            'analyzed_text': input_text[:100] + '...' if len(input_text) > 100 else input_text
        }
        
        logger.info(f"Writing style analysis completed for method: {method}, input length: {len(input_text)}")
        return jsonify(analysis_result)
        
    except Exception as e:
        logger.error(f"Error in writing style analysis: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })

@onboarding_bp.route('/step2', methods=['GET', 'POST'])
def writing_style():
    """Step 2: Writing Style Analysis"""
    logger.info(f"Step 2 route called. Method: {request.method}")
    logger.info(f"Step 2 - Workflow object ID: {id(workflow)}")
    logger.info(f"Step 2 - Current data_sources: {workflow.data_sources}")
    
    if request.method == 'POST':
        # Save the writing style analysis data
        writing_style_data = request.get_json()
        if writing_style_data:
            # Store the writing style data in workflow
            workflow.writing_style = writing_style_data
            logger.info(f"Saved writing style data: {writing_style_data}")
            logger.info(f"Step 2 POST - Workflow object ID: {id(workflow)}")
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'No writing style data provided'})
    
    # GET request - render the template
    workflow.current_step = 2
    logger.info(f"Step 2 - Rendering template with {len(workflow.data_sources)} data sources")
    return render_template('onboarding/step2_writing_style.html', step=2, tone_sources=workflow.tone_sources)

@onboarding_bp.route('/step3', methods=['GET', 'POST'])
def content_strategy():
    """Step 3: Content Strategy and Scheduling"""
    logger.info(f"Step 3 route called. Method: {request.method}")
    logger.info(f"Step 3 - Workflow object ID: {id(workflow)}")
    logger.info(f"Step 3 - Current data_sources: {workflow.data_sources}")
    
    if request.method == 'POST':
        # Save the content strategy
        strategy_data = request.get_json()
        if strategy_data:
            workflow.content_strategy = strategy_data
            logger.info(f"Saved content strategy: {strategy_data}")
            logger.info(f"Step 3 POST - Workflow object ID: {id(workflow)}")
            logger.info(f"Step 3 POST - Current workflow state: {workflow.to_dict()}")
            return jsonify({'status': 'success'})
        return jsonify({'status': 'error', 'message': 'No strategy data provided'})
    
    # GET request - render the template
    workflow.current_step = 3
    logger.info(f"Step 3 - Rendering template with {len(workflow.data_sources)} data sources")
    return render_template('onboarding/step3_content_strategy.html', step=3, tone_analysis=workflow.tone_analysis)

@onboarding_bp.route('/save-strategy', methods=['POST'])
def save_strategy():
    """Save the content strategy and schedule"""
    strategy_data = request.get_json()
    if strategy_data:
        workflow.content_strategy = strategy_data
        logger.info(f"Saved content strategy: {strategy_data}")
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'No strategy data provided'})

@onboarding_bp.route('/step4')
def generate_content():
    """Step 4: Content Generation"""
    logger.info(f"Step 4 route called")
    logger.info(f"Step 4 - Workflow object ID: {id(workflow)}")
    logger.info(f"Step 4 - Data sources count: {len(workflow.data_sources)}")
    logger.info(f"Step 4 - Data sources: {workflow.data_sources}")
    logger.info(f"Step 4 - Writing style: {workflow.writing_style}")
    logger.info(f"Step 4 - Content strategy: {workflow.content_strategy}")
    
    workflow.current_step = 4
    
    return render_template('onboarding/step4_article_generation.html', 
                          step=4, 
                          data_sources=workflow.data_sources,
                          tone_analysis=workflow.writing_style,  # Use writing_style instead of tone_analysis
                          content_strategy=workflow.content_strategy)

@onboarding_bp.route('/crawl-analyze', methods=['POST'])
def crawl_and_analyze():
    """Crawl sources and analyze content"""
    try:
        # Get source URLs from the request
        source_urls = request.json.get('source_urls', [])
        if not source_urls:
            return jsonify({
                'status': 'error',
                'message': 'No source URLs provided'
            })
        
        # Initialize crawler
        crawler = UniversalCrawler()
        
        # Crawl each URL
        results = []
        for url in source_urls:
            result = crawler.crawl(url)
            if result.get('status') == 'success':
                results.append(result)
        
        # Store results in workflow data
        workflow.crawled_data = {
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'results': results
        }
        
        return jsonify({
            'status': 'success',
            'message': f'Successfully crawled {len(results)} sources',
            'result_count': len(results)
        })
        
    except Exception as e:
        logger.error(f"Error in crawl-analyze: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })

@onboarding_bp.route('/analyze-tone', methods=['POST'])
def analyze_tone():
    """Analyze writing style and tone from sources"""
    try:
        # Get tone sources from the request
        tone_sources = request.json.get('tone_sources', [])
        if not tone_sources:
            return jsonify({
                'status': 'error',
                'message': 'No tone sources provided'
            })
        
        # Store tone sources in workflow data
        workflow.tone_sources = tone_sources
        
        # Initialize tone crawler and analyzer
        tone_crawler = ToneCrawler()
        tone_mapper = NeuralToneMapper()
        
        # Crawl and analyze each source
        all_text = ""
        for source in tone_sources:
            if source.get('type') == 'url':
                result = tone_crawler.crawl(source.get('content', ''))
                if result.get('status') == 'success':
                    # Extract paragraphs and add to combined text
                    paragraphs = result.get('paragraphs', [])
                    all_text += "\n\n".join(paragraphs)
            else:  # Direct text input
                all_text += source.get('content', '') + "\n\n"
        
        # Analyze the combined text
        analysis_results = tone_mapper.analyze_text(all_text)
        formatted_analysis = tone_mapper.format_analysis_for_display(analysis_results)
        
        # Store analysis results in workflow data
        workflow.tone_analysis = formatted_analysis
        
        return jsonify({
            'status': 'success',
            'analysis': formatted_analysis,
            'message': 'Tone analysis completed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error in analyze-tone: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })

# Removed duplicate generate_article function to avoid conflicts
# This route was replaced by the comprehensive version below

# Removed duplicate article_preview function to avoid conflicts
# This route was replaced by the comprehensive version below

# ===== V2 WORKFLOW ROUTES (REORGANIZED ORDER) =====

@onboarding_bp.route('/v2/')
def start_v2():
    """Start of the reorganized workflow - Step 1: Content Strategy"""
    # Reset workflow data when starting from scratch
    global workflow
    workflow.reset()  # Reset existing workflow instead of creating new one
    workflow.is_v2_workflow = True
    workflow.current_step = 1
    logger.info(f"Starting V2 workflow (reorganized order) - Workflow object ID: {id(workflow)}")
    return jsonify({"status": "success", "message": "V2 workflow initialized"})

@onboarding_bp.route('/v2/step1')
def content_strategy_v2():
    """Step 1 (V2): Content Strategy and Scheduling"""
    workflow.current_step = 1
    return render_template('onboarding/step3_content_strategy.html', step=1, total_steps=4, is_v2=True)

@onboarding_bp.route('/v2/step2')
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

@onboarding_bp.route('/v2/step3')
def writing_style_v2():
    """Step 3 (V2): Writing Style Analysis"""
    workflow.current_step = 3
    return render_template('onboarding/step2_writing_style.html', step=3, total_steps=4, is_v2=True)

@onboarding_bp.route('/v2/step4')
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

@onboarding_bp.route('/add-source-with-topic', methods=['POST'])
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

@onboarding_bp.route('/topic-guided-crawl', methods=['POST'])
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
        primary_topic = workflow.content_strategy.get('primary_topic', '')
        content_pillars = workflow.content_strategy.get('content_pillars', [])
        
        # Initialize crawler
        crawler = UniversalCrawler()
        
        # Crawl sources with topic guidance
        crawl_results = []
        for source in workflow.data_sources:
            url = source.get('url', '')
            if not url:
                continue
                
            logger.info(f"Crawling source with topic guidance: {url}")
            
            # Use the UniversalCrawler to extract content
            crawl_result = crawler.crawl(url)
            
            if crawl_result.get('status') == 'success':
                # Calculate topic relevance score
                content = crawl_result.get('content', '')
                
                # Simple relevance scoring - count occurrences of topics
                relevance_score = 0
                if primary_topic and primary_topic.lower() in content.lower():
                    relevance_score += 5
                    logger.info(f"  Primary topic match in content (+5)")
                
                for pillar in content_pillars:
                    if pillar.lower() in content.lower():
                        relevance_score += 3
                        logger.info(f"  Content pillar match: {pillar} (+3)")
                
                # Add relevance score to result
                crawl_result['topic_relevance'] = relevance_score
                crawl_result['source_type'] = source.get('type', 'article')
                crawl_result['topic_pillar'] = source.get('topic_relevance', '')
                
                logger.info(f"  Content extracted: {crawl_result.get('word_count', 0)} words")
                logger.info(f"  Topic relevance score: {relevance_score}")
                
                crawl_results.append(crawl_result)
            else:
                logger.error(f"  Failed to crawl {url}: {crawl_result.get('message', 'Unknown error')}")
        
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

@onboarding_bp.route('/generate-article-v2', methods=['POST'])
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
        
        # Get generator parameters
        generator_type = request.form.get('generator_type', 'advanced')
        word_count = int(request.form.get('word_count', 2000))
        include_citations = request.form.get('include_citations', 'true').lower() == 'true'
        style_emphasis = request.form.get('style_emphasis', 'balanced')
        
        # Initialize article generator
        generator = ArticleGenerator()
        
        # Prepare source material from crawled data
        source_material = []
        for source in workflow.crawled_data.get('sources', []):
            source_material.append({
                'url': source.get('url', ''),
                'title': source.get('title', ''),
                'content': source.get('content', ''),
                'domain': source.get('domain', ''),
                'type': source.get('source_type', 'article'),
                'relevance': source.get('topic_relevance', 0),
                'topic_pillar': source.get('topic_pillar', '')
            })
        
        # Generate article with topic guidance
        primary_topic = workflow.content_strategy.get('primary_topic', '')
        article = generator.generate_article(
            topic=primary_topic,
            style_profile=workflow.tone_analysis,
            source_material=source_material,
            word_count=word_count,
            include_citations=include_citations,
            style_emphasis=style_emphasis
        )
        
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

@onboarding_bp.route('/generate-article', methods=['POST'])
def generate_article():
    """
    Generate article using collected workflow data
    """
    try:
        logger.info(f"Generate article called - Workflow object ID: {id(workflow)}")
        logger.info(f"Content strategy: {workflow.content_strategy}")
        logger.info(f"Data sources: {workflow.data_sources}")
        logger.info(f"Writing style: {workflow.writing_style}")
        
        # Get the article generator based on settings
        generator_type = request.form.get('generator_type', 'auto')
        article_generator = get_article_generator(generator_type=generator_type)
        
        # Extract topic from content strategy with intelligent fallback
        content_strategy = workflow.content_strategy or {}
        logger.info(f"Content strategy for article generation: {content_strategy}")
        
        # Try multiple possible keys for the topic
        topic = (
            content_strategy.get('primaryTopic') or  # From step 3 form
            content_strategy.get('primary_topic') or
            content_strategy.get('content_focus') or
            content_strategy.get('main_topic') or
            content_strategy.get('topic') or
            'General Content'  # Better fallback
        )
        
        logger.info(f"Using topic for article generation: {topic}")
        
        # Use writing style analysis if available
        style_profile = workflow.writing_style or workflow.tone_analysis or {}
        logger.info(f"Style profile for article generation: {style_profile}")
        
        # Use actual data sources if available, otherwise use crawled data
        if workflow.data_sources:
            source_material = [
                {"content": f"Source: {source}", "relevance": 0.95} 
                for source in workflow.data_sources
            ]
            logger.info(f"Using {len(workflow.data_sources)} data sources for article generation")
        else:
            source_material = [
                {"content": entry, "relevance": 0.95} 
                for entry in workflow.crawled_data.get('sections', [])
            ]
            logger.info(f"Using crawled data for article generation: {len(source_material)} sections")
        
        generated_article = article_generator.generate_article(
            topic=topic,
            style_profile=style_profile,
            source_material=source_material
        )
        
        # Debug: Log what the article generator returned
        logger.info(f"Article generator returned: {generated_article}")
        logger.info(f"Article generator return type: {type(generated_article)}")
        if isinstance(generated_article, dict):
            logger.info(f"Article generator keys: {list(generated_article.keys())}")
        
        workflow.generated_article = generated_article
        
        return jsonify({
            'status': 'success',
            'message': 'Article generated successfully',
            'article': generated_article,
            'redirect_url': '/onboarding/article-preview'
        })
        
    except Exception as e:
        logger.error(f"Error generating article: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': f"Error generating article: {str(e)}"
        }), 500

@onboarding_bp.route('/article-preview')
def article_preview():
    """Preview the generated article"""
    logger.info(f"Article preview route called. Workflow generated_article: {workflow.generated_article}")
    
    if not workflow.generated_article:
        logger.error("No generated article found in workflow")
        return redirect('/onboarding/step4')
    
    # Debug: Log the structure of the generated article
    logger.info(f"Generated article type: {type(workflow.generated_article)}")
    logger.info(f"Generated article keys: {workflow.generated_article.keys() if isinstance(workflow.generated_article, dict) else 'Not a dict'}")
    
    # Try to extract article data with fallbacks
    if isinstance(workflow.generated_article, dict):
        # Try different possible structures
        article_data = (
            workflow.generated_article.get('article', {}) or
            workflow.generated_article.get('content', {}) or
            workflow.generated_article.get('text', {}) or
            workflow.generated_article  # Use the whole thing as fallback
        )
    else:
        # If it's not a dict, try to convert it
        article_data = {'content': str(workflow.generated_article)}
    
    logger.info(f"Final article_data for template: {article_data}")
    
    # Pass article data directly to the template instead of relying on session storage
    return render_template('article_preview.html', article_data=article_data)

@onboarding_bp.route('/workflow-version', methods=['GET'])
def workflow_version():
    """Return the current workflow version"""
    is_v2 = getattr(workflow, 'is_v2_workflow', False)
    return jsonify({
        'version': 'v2' if is_v2 else 'v1',
        'description': 'Reorganized workflow with content strategy first' if is_v2 else 'Original 4-step workflow',
        'current_step': workflow.current_step
    })
