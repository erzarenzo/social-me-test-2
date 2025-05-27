#!/usr/bin/env python3
"""
Simple Flask app to test the Advanced Article Generator
"""

import os
import json
import logging
import datetime
from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("test_app")

# Load environment variables
load_dotenv()

# Import the ArticleGenerator
from app.advanced_article_generator import ArticleGenerator

# Initialize Flask app
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
app.secret_key = 'test_secret_key'

# Initialize the ArticleGenerator
claude_api_key = os.getenv("CLAUDE_API_KEY")
article_generator = ArticleGenerator(api_key=claude_api_key)

# Sample data for testing
SAMPLE_TONE_ANALYSIS = {
    "voice_character": {
        "formality": 0.85,
        "technical_depth": 0.78,
        "persuasiveness": 0.65,
        "expressiveness": 0.45,
        "descriptiveness": 0.72
    },
    "linguistic_patterns": {
        "sentence_structure": {
            "complex": 0.65,
            "compound": 0.25,
            "simple": 0.10
        },
        "vocabulary_richness": 0.82,
        "transition_usage": 0.75,
        "active_voice_ratio": 0.68
    },
    "content_architecture": {
        "logical_flow": 0.88,
        "evidence_usage": 0.92,
        "concept_development": 0.85,
        "abstraction_level": 0.76
    },
    "engagement_dynamics": {
        "question_frequency": 0.25,
        "reader_addressing": 0.35,
        "anecdote_usage": 0.45,
        "emotional_appeal": 0.38
    }
}

SAMPLE_CRAWLED_CONTENT = [
    {
        "title": "The Evolution of Artificial Intelligence",
        "url": "https://example.com/ai-evolution",
        "content": """
        Artificial Intelligence has evolved significantly over the past decade. Machine learning algorithms 
        have become more sophisticated, enabling systems to recognize patterns and make decisions with minimal 
        human intervention. Deep learning, a subset of machine learning, has revolutionized fields like computer 
        vision and natural language processing. The development of neural networks that mimic the human brain's 
        structure has led to breakthroughs in image recognition, language translation, and speech synthesis.
        
        Recent advancements in reinforcement learning have enabled AI systems to master complex games and 
        tasks through trial and error. This approach has been successfully applied to domains ranging from 
        game playing to robotics and autonomous vehicles. The integration of AI into everyday applications 
        has transformed industries and created new opportunities for innovation.
        """,
        "relevance_score": 0.95,
        "key_points": [
            "Evolution of AI over the past decade",
            "Advancements in machine learning and deep learning",
            "Neural networks mimicking human brain structure",
            "Reinforcement learning enabling mastery of complex tasks",
            "Integration of AI into everyday applications"
        ]
    },
    {
        "title": "Ethical Considerations in AI Development",
        "url": "https://example.com/ai-ethics",
        "content": """
        As AI systems become more powerful and ubiquitous, ethical considerations have gained prominence. 
        Issues such as algorithmic bias, privacy concerns, and the potential for job displacement require 
        careful attention. Researchers and policymakers are working to establish frameworks for responsible 
        AI development and deployment.
        
        Transparency and explainability have emerged as crucial aspects of ethical AI. Users and stakeholders 
        need to understand how AI systems make decisions, especially in high-stakes contexts like healthcare, 
        criminal justice, and finance. The concept of "explainable AI" focuses on creating models that can 
        provide clear rationales for their outputs.
        
        Data privacy is another significant concern, as AI systems often rely on vast amounts of personal 
        information. Striking the right balance between utilizing data for innovation and respecting individual 
        privacy rights remains a challenge. Regulatory frameworks like GDPR in Europe have established guidelines 
        for data protection, but the rapid pace of technological advancement requires ongoing adaptation.
        """,
        "relevance_score": 0.88,
        "key_points": [
            "Ethical considerations in AI development",
            "Algorithmic bias and privacy concerns",
            "Importance of transparency and explainability",
            "Data privacy challenges",
            "Regulatory frameworks like GDPR"
        ]
    },
    {
        "title": "The Future of AI: Opportunities and Challenges",
        "url": "https://example.com/ai-future",
        "content": """
        Looking ahead, AI presents both tremendous opportunities and significant challenges. The potential 
        for AI to address global problems like climate change, healthcare accessibility, and resource 
        allocation is substantial. AI-powered systems could optimize energy usage, accelerate drug discovery, 
        and enhance educational outcomes.
        
        However, concerns about autonomous weapons, surveillance capabilities, and the concentration of AI 
        power in the hands of a few corporations or nations raise important questions about governance and 
        control. The development of artificial general intelligence (AGI) – systems with human-like cognitive 
        abilities across diverse domains – introduces additional complexities.
        
        Collaborative efforts between researchers, industry leaders, policymakers, and civil society will be 
        essential to harness AI's benefits while mitigating its risks. Establishing international norms and 
        standards for AI development could help ensure that these powerful technologies serve humanity's best 
        interests.
        """,
        "relevance_score": 0.92,
        "key_points": [
            "AI's potential to address global problems",
            "Concerns about autonomous weapons and surveillance",
            "Challenges of artificial general intelligence (AGI)",
            "Need for collaborative governance efforts",
            "Importance of international norms and standards"
        ]
    }
]

@app.route('/')
def index():
    """Render the test page"""
    return render_template('results.html', 
        article={
            'title': 'Test Article',
            'subtitle': 'This is a test article for the Advanced Article Generator',
            'body': 'Click the "Generate Advanced Article" button to test the generator.',
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'publishing_frequency': 'Weekly',
            'sources': ['Test Source 1', 'Test Source 2', 'Test Source 3'],
            'summary': {
                'audience': 'Technology professionals and AI enthusiasts',
                'tone': 'Informative and analytical',
                'purpose': 'Educational'
            },
            'stats': {
                'sections': 3,
                'words': 500,
                'reading_time': 3
            }
        },
        use_advanced_generator=True  # Always enable the advanced generator button
    )

@app.route('/generate_advanced_article', methods=['POST'])
def generate_advanced_article_route():
    """Generate an article using the advanced article generator"""
    # Log the request
    logger.info("Generating advanced article on topic: The Impact of Artificial Intelligence on Modern Society")
    logger.info("Using 3 sources")
    
    # Sample tone analysis data
    tone_analysis = {
        "voice_profile": {
            "formality": 0.8,
            "technical_level": 0.7,
            "persuasiveness": 0.6,
            "emotional_tone": "neutral",
            "engagement_style": "informative"
        },
        "linguistic_patterns": {
            "sentence_length": "medium",
            "vocabulary_complexity": "high",
            "transition_phrases": ["furthermore", "however", "in addition"],
            "rhetorical_devices": ["analogy", "rhetorical question"]
        },
        "content_structure": {
            "intro_style": "question-based",
            "paragraph_structure": "claim-evidence-explanation",
            "conclusion_style": "summary with call to action"
        }
    }
    
    # Sample crawled content
    crawled_content = [
        {
            "url": "https://example.com/ai-article-1",
            "title": "The Evolution of AI in the 21st Century",
            "content": "Artificial Intelligence has evolved significantly in the past decade. From simple rule-based systems to complex neural networks, AI technologies have transformed industries and daily life. Machine learning algorithms now power recommendation systems, autonomous vehicles, and medical diagnostics. Deep learning, a subset of machine learning, has revolutionized image and speech recognition. The development of transformer models like GPT has enabled AI to generate human-like text and engage in meaningful conversations. As computing power increases and algorithms improve, AI continues to advance at an unprecedented pace.",
            "date": "2023-05-15"
        },
        {
            "url": "https://example.com/ai-article-2",
            "title": "Ethical Considerations in AI Development",
            "content": "As AI becomes more integrated into our daily lives, ethical considerations have become increasingly important. Issues such as bias in algorithms, privacy concerns, and the potential for job displacement require careful attention. AI systems trained on biased data can perpetuate and amplify existing societal inequalities. The collection and use of personal data for AI training raises significant privacy concerns. Additionally, as AI automates more tasks, there's growing concern about workforce disruption. Developing ethical frameworks and regulations for AI is essential to ensure these technologies benefit humanity while minimizing harm. Transparency in AI decision-making processes is also crucial for building public trust.",
            "date": "2023-06-22"
        },
        {
            "url": "https://example.com/ai-article-3",
            "title": "AI and the Future of Work",
            "content": "The impact of AI on employment and the workforce has been a topic of debate among economists, technologists, and policymakers. While AI will likely automate certain jobs, it's also expected to create new opportunities and transform existing roles. Routine and repetitive tasks are most susceptible to automation, while jobs requiring creativity, emotional intelligence, and complex problem-solving may be enhanced by AI. Workers will need to develop new skills and adapt to changing job requirements. Educational systems and workforce development programs must evolve to prepare people for this AI-augmented future. Organizations that effectively integrate human and artificial intelligence may gain significant competitive advantages.",
            "date": "2023-07-10"
        }
    ]
    
    # Create an instance of ArticleGenerator
    try:
        from app.advanced_article_generator import ArticleGenerator
        generator = ArticleGenerator()
        
        # Generate the article
        article = generator.generate_article(
            topic="The Impact of Artificial Intelligence on Modern Society",
            style_profile=tone_analysis,
            source_material=crawled_content
        )
        
        logger.info(f"Generated article with title: {article.get('title', 'No title')}")
        
        # Check if there was an error
        if "error" in article:
            logger.error(f"Error in article generation: {article.get('error')}")
            
            # Format the error for JSON response
            return jsonify({
                "status": "error",
                "message": article.get("error", "Unknown error"),
                "article": {
                    "title": article.get("title", "Error Generating Article"),
                    "subtitle": article.get("subtitle", "An error occurred"),
                    "introduction": article.get("introduction", "There was an error generating your article."),
                    "body": article.get("body", []),
                    "conclusion": article.get("conclusion", "")
                }
            })
        
        # Format the article for JSON response
        formatted_article = {
            "title": article.get("title", "Generated Article"),
            "subtitle": article.get("subtitle", ""),
            "introduction": article.get("introduction", ""),
            "overview": article.get("overview", ""),
            "body": article.get("body", []),
            "conclusion": article.get("conclusion", ""),
            "sources": [{"name": source["title"], "url": source["url"]} for source in crawled_content]
        }
        
        # Calculate stats
        word_count = sum(len(str(v).split()) for v in article.values() if isinstance(v, str))
        if isinstance(article.get("body"), list):
            for section in article.get("body", []):
                if isinstance(section, dict) and "content" in section:
                    word_count += len(section["content"].split())
                    
        reading_time = max(1, word_count // 200)  # Assume 200 words per minute
        sections_count = len(article.get("body", [])) if isinstance(article.get("body"), list) else 3
        
        # Return JSON response
        return jsonify({
            "status": "success",
            "article": formatted_article,
            "validation": {
                "sources_used": len(crawled_content),
                "word_count": word_count,
                "generation_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        })
        
    except Exception as e:
        logger.error(f"Exception in generate_advanced_article: {e}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Return an error message as JSON
        return jsonify({
            "status": "error",
            "message": str(e),
            "article": {
                "title": "Error Generating Article",
                "subtitle": "An unexpected error occurred",
                "introduction": f"Error: {str(e)}",
                "body": [],
                "conclusion": "Please try again later or contact support if the issue persists."
            }
        })

if __name__ == '__main__':
    port = 8003  # Explicitly set port to 8003
    app.run(host='0.0.0.0', port=port, debug=True)
