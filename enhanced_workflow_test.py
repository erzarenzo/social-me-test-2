#!/usr/bin/env python3
import requests
import json
import time
import os
import sys
import logging
from pprint import pprint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("enhanced_workflow_test")

# Base URL for the Flask app
BASE_URL = "http://localhost:8003"

# Session to maintain cookies across requests
session = requests.Session()

class EnhancedWorkflowTest:
    """
    Enhanced workflow test that focuses on generating a complete 4000-word article
    with proper tone adaptation based on analysis results.
    """
    
    def __init__(self):
        self.base_url = BASE_URL
        self.session = session
        self.sources = []
        self.tone_analysis = {}
        self.content_strategy = {}
        self.generated_article = None
        
    def run_test(self):
        """Run the complete workflow test with enhanced features"""
        print("\nENHANCED WORKFLOW TEST")
        print("======================\n")
        
        # Step 1: Test data sources page and add multiple sources
        self.test_data_sources()
        
        # Step 2: Test writing style analysis with realistic sample
        self.test_writing_style()
        
        # Step 3: Test content strategy
        self.test_content_strategy()
        
        # Step 4: Test article generation with enhanced features
        self.test_article_generation()
        
        # Summary
        self.print_summary()
    
    def test_data_sources(self):
        """Test the data sources page and add multiple diverse sources"""
        print("\nTESTING: Step 1: Data Sources")
        print("-----------------------------")
        start_time = time.time()
        
        # Access the data sources page
        print("\n===== Step 1: Data Sources Page =====")
        response = self.session.get(f"{self.base_url}/onboarding/step1")
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{response.text[:500]}...")
        print("="*50)
        
        # Add multiple diverse sources for comprehensive article generation
        sources = [
            {"url": "https://techcrunch.com/category/artificial-intelligence/", "type": "news"},
            {"url": "https://www.linkedin.com/in/andrew-ng-stanford/", "type": "linkedin"},
            {"url": "https://twitter.com/ylecun", "type": "twitter"},
            {"url": "https://openai.com/blog/", "type": "blog"},
            {"url": "https://www.deeplearning.ai/blog/", "type": "blog"}
        ]
        
        for source in sources:
            print(f"\n===== Add Source: {source['url']} =====")
            response = self.session.post(
                f"{self.base_url}/add-source",
                data={"source_url": source["url"], "source_type": source["type"]}
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response:\n{json.dumps(response.json(), indent=2)}")
            print("="*50)
            
            # Also preview each source to ensure content extraction works
            print(f"\n===== Preview Source: {source['url']} =====")
            response = self.session.get(
                f"{self.base_url}/preview-source",
                params={"url": source["url"]}
            )
            print(f"Status Code: {response.status_code}")
            print(f"Response:\n{json.dumps(response.json(), indent=2)}")
            print("="*50)
            
            # Store sources for later use
            self.sources.append(source)
            
        # Store time taken
        self.time_step1 = time.time() - start_time
        print(f"\nStep 1: Data Sources: COMPLETED (Time: {self.time_step1:.2f}s)")
        
    def test_writing_style(self):
        """Test the writing style analysis with a comprehensive sample"""
        print("\nTESTING: Step 2: Writing Style")
        print("-----------------------------")
        start_time = time.time()
        
        # Access the writing style page
        print("\n===== Step 2: Writing Style Page =====")
        response = self.session.get(f"{self.base_url}/onboarding/step2")
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{response.text[:500]}...")
        print("="*50)
        
        # Prepare a comprehensive writing sample
        sample_text = """
        The Evolution of Artificial Intelligence: From Rule-Based Systems to Deep Learning
        
        Artificial intelligence has undergone a remarkable transformation over the past few decades. What began as simple rule-based expert systems has evolved into sophisticated neural networks capable of recognizing patterns, understanding natural language, and even generating creative content.
        
        The early days of AI were characterized by symbolic approaches, where human experts would encode knowledge as explicit rules. These systems excelled at well-defined tasks but struggled with ambiguity and couldn't learn from experience. The limitations became apparent in the 1980s, leading to what's known as the "AI winter" - a period of reduced funding and interest.
        
        The renaissance of AI began with the resurgence of machine learning in the 1990s and early 2000s. Rather than hard-coding rules, these systems learned patterns from data. Support Vector Machines and Random Forests became popular for classification tasks, while recommendation systems began to appear in e-commerce platforms.
        
        The true breakthrough came with deep learning, particularly after 2012 when AlexNet demonstrated the power of convolutional neural networks for image recognition. Suddenly, AI systems could outperform humans at specific perceptual tasks. The development of architectures like recurrent neural networks and transformers further expanded capabilities into language processing, leading to models like GPT and BERT.
        
        Today, we're witnessing the emergence of multimodal AI systems that can process and generate content across different formats - text, images, audio, and video. These systems are increasingly integrated into our daily lives, from voice assistants to content recommendation engines.
        
        The future of AI likely involves more sophisticated reasoning capabilities, better alignment with human values, and increased transparency in how decisions are made. As these systems become more powerful, ensuring they remain beneficial, safe, and accessible becomes a critical societal challenge.
        """
        
        # Submit the writing sample for analysis
        print("\n===== Analyze Writing Style =====")
        response = self.session.post(
            f"{self.base_url}/analyze-content",
            data={"type": "text", "content": sample_text}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        print("="*50)
        
        # Store the tone analysis for article generation
        if response.status_code == 200:
            self.tone_analysis = response.json()
        
        # Store time taken
        self.time_step2 = time.time() - start_time
        print(f"\nStep 2: Writing Style: COMPLETED (Time: {self.time_step2:.2f}s)")
        
    def test_content_strategy(self):
        """Test the content strategy with detailed parameters"""
        print("\nTESTING: Step 3: Content Strategy")
        print("-------------------------------")
        start_time = time.time()
        
        # Access the content strategy page
        print("\n===== Step 3: Content Strategy Page =====")
        response = self.session.get(f"{self.base_url}/onboarding/step3")
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{response.text[:500]}...")
        print("="*50)
        
        # Create a detailed content strategy
        strategy = {
            "primary_topic": "The Future of AI in Healthcare",
            "content_focus": "How AI is transforming medical diagnostics, treatment planning, and patient care",
            "target_audience": "Healthcare professionals, technology leaders, and policy makers",
            "content_pillars": [
                "AI-powered diagnostic imaging",
                "Predictive analytics for patient outcomes",
                "Personalized treatment planning",
                "Ethical considerations and patient privacy",
                "Healthcare workflow automation",
                "AI for drug discovery and development"
            ],
            "desired_word_count": 4000,
            "tone_preferences": {
                "formality": "high",
                "technical_depth": "expert",
                "perspective": "balanced"
            }
        }
        
        # Submit the strategy
        print("\n===== Save Content Strategy =====")
        response = self.session.post(
            f"{self.base_url}/save-strategy",
            json=strategy,
            headers={"Content-Type": "application/json"}
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2) if response.headers.get('Content-Type') == 'application/json' else response.text[:500]}")
        print("="*50)
        
        # Store the content strategy
        self.content_strategy = strategy
        
        # Store time taken
        self.time_step3 = time.time() - start_time
        print(f"\nStep 3: Content Strategy: COMPLETED (Time: {self.time_step3:.2f}s)")
        
    def test_article_generation(self):
        """Test the article generation with enhanced parameters"""
        print("\nTESTING: Step 4: Article Generation")
        print("---------------------------------")
        start_time = time.time()
        
        # Access the article generation page
        print("\n===== Step 4: Article Generation Page =====")
        response = self.session.get(f"{self.base_url}/onboarding/step4")
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{response.text[:500]}...")
        print("="*50)
        
        # Make sure we first crawl and analyze the data sources
        print("\n===== Crawl and Analyze Sources =====")
        response = self.session.post(f"{self.base_url}/crawl-and-analyze")
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2) if response.headers.get('Content-Type') == 'application/json' else response.text[:500]}")
        print("="*50)
        
        # Now generate the article with enhanced parameters
        print("\n===== Generate Article (Enhanced) =====")
        
        # Set specific parameters to ensure a comprehensive article
        params = {
            "generator_type": "advanced",  # Use the advanced generator
            "word_count": 4000,            # Target 4000 words
            "apply_tone": "true",          # Apply the tone analysis
            "debug_mode": "true"           # Get detailed generation info
        }
        
        response = self.session.post(
            f"{self.base_url}/generate-article",
            data=params
        )
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2) if response.headers.get('Content-Type') == 'application/json' else response.text[:500]}")
        print("="*50)
        
        # Store the generated article
        if response.status_code == 200 and response.headers.get('Content-Type') == 'application/json':
            self.generated_article = response.json()
            
            # Save the article to a file for review
            self.save_article_to_file(self.generated_article)
        
        # View the article preview
        print("\n===== Article Preview =====")
        response = self.session.get(f"{self.base_url}/article-preview")
        print(f"Status Code: {response.status_code}")
        print(f"Response:\n{response.text[:500]}...")
        print("="*50)
        
        # Store time taken
        self.time_step4 = time.time() - start_time
        result = "PASSED" if self.generated_article else "FAILED"
        print(f"\nStep 4: Article Generation: {result} (Time: {self.time_step4:.2f}s)")
        
    def save_article_to_file(self, article_data):
        """Save the generated article to an HTML file"""
        if not article_data:
            return
            
        article = article_data.get('article', {})
        
        # Create a simple HTML file to view the article
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{article.get('title', 'Generated Article')}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        h1 {{
            color: #1a1a1a;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #2a2a2a;
            margin-top: 30px;
        }}
        h3 {{
            color: #3a3a3a;
        }}
        .subtitle {{
            font-size: 1.2em;
            color: #666;
            margin-bottom: 20px;
        }}
        .stats {{
            background: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #ccc;
        }}
        .conclusion {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 5px;
            margin-top: 30px;
            border-left: 4px solid #ddd;
        }}
    </style>
</head>
<body>
    <h1>{article.get('title', 'Generated Article')}</h1>
    <div class="subtitle">{article.get('subtitle', '')}</div>
    
    <div class="stats">
        <strong>Word Count Analysis:</strong><br>
        Introduction: {len(article.get('introduction', '').split())} words<br>
        Sections: {sum(len(section.get('content', '').split()) for section in article.get('sections', []))} words<br>
        Conclusion: {len(article.get('conclusion', '').split())} words<br>
        <strong>Total: {len(article.get('introduction', '').split()) + sum(len(section.get('content', '').split()) for section in article.get('sections', [])) + len(article.get('conclusion', '').split())} words</strong>
    </div>
    
    <div>
        <h2>Introduction</h2>
        <p>{article.get('introduction', 'No introduction provided.')}</p>
    </div>
    
    <div>
        <h2>Content</h2>
        {''.join([f'<h3>{section.get("subheading", "")}</h3><p>{section.get("content", "")}</p>' for section in article.get('sections', [])])}
    </div>
    
    <div class="conclusion">
        <h2>Conclusion</h2>
        <p>{article.get('conclusion', 'No conclusion provided.')}</p>
    </div>
    
    <div>
        <h2>Sources</h2>
        <ul>
            {''.join([f'<li>{source.get("url", "")}</li>' for source in self.sources])}
        </ul>
    </div>
</body>
</html>
"""
        
        with open('enhanced_article.html', 'w') as f:
            f.write(html_content)
            
        print(f"Article saved to enhanced_article.html for review")
        
        # Also save a text version with word counts
        text_content = f"""
ARTICLE TITLE: {article.get('title', 'Generated Article')}
SUBTITLE: {article.get('subtitle', '')}

WORD COUNT ANALYSIS:
Introduction: {len(article.get('introduction', '').split())} words
Sections: {sum(len(section.get('content', '').split()) for section in article.get('sections', []))} words
Conclusion: {len(article.get('conclusion', '').split())} words
TOTAL: {len(article.get('introduction', '').split()) + sum(len(section.get('content', '').split()) for section in article.get('sections', [])) + len(article.get('conclusion', '').split())} words

INTRODUCTION:
{article.get('introduction', 'No introduction provided.')}

CONTENT:
"""
        
        for section in article.get('sections', []):
            text_content += f"\n--- {section.get('subheading', '')} ---\n"
            text_content += f"{section.get('content', '')}\n"
            text_content += f"(Section word count: {len(section.get('content', '').split())} words)\n"
            
        text_content += f"\nCONCLUSION:\n{article.get('conclusion', 'No conclusion provided.')}"
        
        with open('enhanced_article.txt', 'w') as f:
            f.write(text_content)
            
        print(f"Text version saved to enhanced_article.txt with word counts")
    
    def print_summary(self):
        """Print a summary of the test results"""
        print("\n\nTEST SUMMARY")
        print("============")
        print(f"Step 1: Data Sources           {'PASSED' if self.sources else 'FAILED'}     {self.time_step1:.2f}s")
        print(f"Step 2: Writing Style          {'PASSED' if self.tone_analysis else 'FAILED'}     {self.time_step2:.2f}s")
        print(f"Step 3: Content Strategy       {'PASSED' if self.content_strategy else 'FAILED'}     {self.time_step3:.2f}s")
        print(f"Step 4: Article Generation     {'PASSED' if self.generated_article else 'FAILED'}     {self.time_step4:.2f}s")
        
        if self.generated_article:
            article = self.generated_article.get('article', {})
            total_words = len(article.get('introduction', '').split()) + \
                         sum(len(section.get('content', '').split()) for section in article.get('sections', [])) + \
                         len(article.get('conclusion', '').split())
            print(f"\nTotal article word count: {total_words} words")
            if total_words < 3500:
                print("⚠️ WARNING: Article is shorter than the 4000-word target")

if __name__ == "__main__":
    print("Starting enhanced workflow test...")
    
    # Ensure the Flask app is running
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print(f"Error: Flask app not responding at {BASE_URL}. Make sure it's running.")
            sys.exit(1)
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to Flask app at {BASE_URL}. Make sure it's running.")
        sys.exit(1)
    
    # Run the enhanced test
    test = EnhancedWorkflowTest()
    test.run_test()
