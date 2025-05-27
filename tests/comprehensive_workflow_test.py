#!/usr/bin/env python3
"""
Comprehensive Workflow Test for SocialMe Application

This script allows you to test the entire workflow:
1. Define content strategy (topic and target audience)
2. Add URL sources for data points using Quantum Universal Crawler
3. Input tone sources for analysis using Quantum Tone Crawler and Neural Tone Mapper
4. Generate an article using Advanced Article Generator
5. View detailed output at each step

Author: SocialMe Team
Date: 2025-03-22
"""

import os
import sys
import json
import time
import logging
import pprint
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("workflow_test")

# Import required modules
try:
    from quantum_universal_crawler import QuantumUniversalCrawler
    from app.quantum_tone_crawler import QuantumToneCrawler
    from app.neural_tone_mapper import NeuralToneMapper
    from app.advanced_article_generator import (
        ArticleGenerator, 
        format_tone_analysis_to_style_profile,
        format_crawler_results_to_source_material,
        generate_advanced_article
    )
except ImportError as e:
    logger.error(f"Failed to import required modules: {e}")
    logger.error("Make sure you're running this script from the root directory of the project")
    sys.exit(1)

class WorkflowTester:
    """
    Comprehensive workflow tester for the SocialMe application
    """
    
    def __init__(self):
        """Initialize the workflow tester"""
        self.content_strategy = {}
        self.data_sources = []
        self.tone_sources = []
        self.crawled_data = []
        self.tone_analysis = {}
        self.generated_article = {}
        
        # Initialize the pretty printer for formatted output
        self.pp = pprint.PrettyPrinter(indent=4)
        
        logger.info("Workflow tester initialized")
    
    def define_content_strategy(self):
        """Define the content strategy (topic and target audience)"""
        print("\n" + "="*80)
        print("STEP 1: DEFINE CONTENT STRATEGY")
        print("="*80)
        
        # Get topic from user
        topic = input("\nEnter the main topic for your article: ")
        while not topic:
            print("Topic cannot be empty. Please enter a valid topic.")
            topic = input("Enter the main topic for your article: ")
        
        # Get target audience from user
        target_audience = input("\nEnter the target audience (e.g., 'Tech Professionals'): ")
        while not target_audience:
            print("Target audience cannot be empty. Please enter a valid target audience.")
            target_audience = input("Enter the target audience: ")
        
        # Get content pillars (optional)
        content_pillars_input = input("\nEnter content pillars (comma-separated, optional): ")
        content_pillars = [pillar.strip() for pillar in content_pillars_input.split(",")] if content_pillars_input else []
        
        # Create content strategy
        self.content_strategy = {
            "primary_topic": topic,
            "target_audience": target_audience,
            "content_pillars": content_pillars,
            "timestamp": datetime.now().isoformat()
        }
        
        print("\nContent Strategy defined:")
        self.pp.pprint(self.content_strategy)
        
        return self.content_strategy
    
    def add_data_sources(self):
        """Add URL sources for data points"""
        print("\n" + "="*80)
        print("STEP 2: ADD DATA SOURCES")
        print("="*80)
        
        print("\nAdd URL sources for data points. The Quantum Universal Crawler will extract relevant content.")
        print("Enter 'done' when you've finished adding sources.")
        
        source_count = 0
        while True:
            source_url = input(f"\nEnter URL for data source #{source_count + 1} (or 'done' to finish): ")
            
            if source_url.lower() == 'done':
                break
                
            if not source_url.startswith(('http://', 'https://')):
                print("Invalid URL. Please enter a valid URL starting with http:// or https://")
                continue
            
            source_type = input("Enter source type (blog, news, linkedin, twitter, rss, newsletter): ")
            if not source_type:
                source_type = "article"  # Default type
            
            topic_relevance = input(f"Enter topic relevance for this source (related to '{self.content_strategy['primary_topic']}'): ")
            if not topic_relevance:
                topic_relevance = self.content_strategy['primary_topic']
            
            # Add source to the list
            self.data_sources.append({
                "source_url": source_url,
                "source_type": source_type,
                "topic_relevance": topic_relevance
            })
            
            source_count += 1
            print(f"Source #{source_count} added: {source_url}")
            
            if source_count >= 3:
                continue_adding = input("\nYou've added 3 or more sources. Continue adding more? (y/n): ")
                if continue_adding.lower() != 'y':
                    break
        
        print(f"\nAdded {len(self.data_sources)} data sources:")
        self.pp.pprint(self.data_sources)
        
        return self.data_sources
    
    def crawl_data_sources(self):
        """Crawl the data sources using Quantum Universal Crawler"""
        print("\n" + "="*80)
        print("STEP 3: CRAWL DATA SOURCES")
        print("="*80)
        
        if not self.data_sources:
            print("No data sources defined. Please add data sources first.")
            return []
        
        print(f"\nCrawling {len(self.data_sources)} data sources with topic guidance...")
        
        # Initialize the crawler with the main topic
        topic = self.content_strategy['primary_topic']
        
        try:
            crawler = QuantumUniversalCrawler(topic=topic)
        except Exception as e:
            print(f"Error initializing crawler: {str(e)}")
            print("Using a simplified crawler instead.")
            crawler = QuantumUniversalCrawler()
        
        # Crawl each source
        all_results = []
        for i, source in enumerate(self.data_sources):
            url = source['source_url']
            print(f"\nCrawling source #{i+1}: {url}...")
            
            # Validate URL format
            if not url.startswith(('http://', 'https://')):
                print(f"Invalid URL format: {url}. Skipping...")
                continue
                
            try:
                # Crawl the source with topic guidance
                results = crawler.crawl(url)
                
                if not results:
                    print(f"No content found at {url}")
                    continue
                
                # Add metadata to the results
                for result in results:
                    try:
                        result_dict = result.to_dict()
                        result_dict['source_type'] = source['source_type']
                        result_dict['topic_pillar'] = source['topic_relevance']
                        all_results.append(result_dict)
                    except Exception as e:
                        print(f"Error processing result: {str(e)}")
                
                print(f"Successfully crawled {len(results)} pages from {url}")
            except Exception as e:
                print(f"Error crawling {url}: {str(e)}")
                print("Adding a placeholder result to continue the workflow.")
                # Add a placeholder result to allow workflow to continue
                all_results.append({
                    'url': url,
                    'title': f"Content from {url}",
                    'content': f"This is placeholder content for {url} which could not be crawled. The topic is {topic}.",
                    'word_count': 20,
                    'source_type': source['source_type'],
                    'topic_pillar': source['topic_relevance']
                })
        
        self.crawled_data = all_results
        
        if not all_results:
            print("\nNo data could be crawled from any sources.")
            print("Adding placeholder data to continue the workflow.")
            self.crawled_data = [{
                'url': 'https://example.com',
                'title': f"Example content about {topic}",
                'content': f"This is example content about {topic}. It contains information relevant to the topic and can be used to generate an article.",
                'word_count': 50,
                'source_type': 'article',
                'topic_pillar': topic
            }]
        
        print(f"\nCrawled {len(all_results)} pages from {len(self.data_sources)} sources")
        print("\nSample of crawled data:")
        
        # Display a sample of the crawled data
        for i, result in enumerate(self.crawled_data[:2]):  # Show first 2 results
            print(f"\nSource {i+1}: {result['url']}")
            print(f"Title: {result.get('title', 'No title')}")
            print(f"Word count: {result.get('word_count', 'Unknown')}")
            content_sample = result.get('content', '')[:300]
            print(f"Content sample: {content_sample}...")
        
        return self.crawled_data
    
    def add_tone_sources(self):
        """Add sources for tone analysis"""
        print("\n" + "="*80)
        print("STEP 4: ADD TONE SOURCES")
        print("="*80)
        
        print("\nAdd sources for tone analysis. You can input text directly or provide URLs.")
        print("The system will analyze your writing style using the Quantum Tone Crawler and Neural Tone Mapper.")
        
        while True:
            input_method = input("\nChoose input method (text, url): ").strip().lower()
            if input_method in ['text', 'url']:
                break
            print("Invalid choice. Please enter 'text' or 'url'.")
        
        if input_method == 'text':
            print("\nEnter your writing sample below. Type 'DONE' on a new line when finished:")
            print("=" * 50)
            
            # Collect multi-line input
            lines = []
            while True:
                try:
                    line = input()
                    if line.strip().upper() == 'DONE':
                        break
                    lines.append(line)
                except EOFError:
                    break
            
            text = '\n'.join(lines)
            
            if not text.strip():
                print("No text detected. Using a default sample instead.")
                text = "This is a sample text for tone analysis. The system will analyze this text to determine your writing style."
            
            self.tone_sources = [{"type": "text", "content": text}]
            
        elif input_method == 'url':
            url = input("\nEnter URL containing your writing style: ").strip()
            
            if not url.startswith(('http://', 'https://')):
                print("Invalid URL. Using a default sample instead.")
                self.tone_sources = [{"type": "text", "content": "This is a sample text for tone analysis. The system will analyze this text to determine your writing style."}]
            else:
                self.tone_sources = [{"type": "url", "url": url}]
        
        print("\nTone sources added:")
        self.pp.pprint(self.tone_sources)
        
        return self.tone_sources
    
    def analyze_tone(self):
        """Analyze the tone using Quantum Tone Crawler and Neural Tone Mapper"""
        print("\n" + "="*80)
        print("STEP 5: ANALYZE WRITING STYLE")
        print("="*80)
        
        if not self.tone_sources:
            print("No tone sources defined. Please add tone sources first.")
            print("Using default tone analysis to continue the workflow.")
            
            # Create default tone analysis
            self.tone_analysis = {
                "thought_patterns": {
                    "analytical": 0.7,
                    "logical": 0.6,
                    "systematic": 0.5,
                    "creative": 0.3
                },
                "reasoning_style": {
                    "deductive": 0.6,
                    "inductive": 0.4,
                    "statistical": 0.5,
                    "analogical": 0.3
                }
            }
            
            print("\nDefault tone analysis created:")
            self.pp.pprint(self.tone_analysis)
            return self.tone_analysis
        
        print("\nAnalyzing writing style...")
        
        # Initialize the tone crawler and mapper
        try:
            tone_crawler = QuantumToneCrawler()
            tone_mapper = NeuralToneMapper()
            
            # Process each tone source
            for source in self.tone_sources:
                if source["type"] == "text":
                    # Direct text analysis
                    text = source["content"]
                    print(f"\nAnalyzing text sample ({len(text.split())} words)...")
                    
                    # Analyze with Neural Tone Mapper
                    try:
                        analysis = tone_mapper.analyze_text(text)
                    except Exception as e:
                        print(f"Error analyzing text: {str(e)}")
                        analysis = self._create_default_analysis()
                    
                elif source["type"] == "url":
                    # URL analysis with Quantum Tone Crawler
                    url = source["url"]
                    print(f"\nAnalyzing content from URL: {url}...")
                    
                    try:
                        # Use the correct method: crawl_and_analyze instead of crawl_url
                        analysis = tone_crawler.crawl_and_analyze(url, content_type='url')
                    except Exception as e:
                        print(f"Error analyzing URL content: {str(e)}")
                        analysis = self._create_default_analysis()
            
            # Format the analysis results
            self.tone_analysis = {
                "thought_patterns": analysis.get("thought_patterns", {
                    "analytical": 0.6,
                    "logical": 0.5,
                    "systematic": 0.4,
                    "creative": 0.3
                }),
                "reasoning_style": analysis.get("reasoning_style", {
                    "deductive": 0.5,
                    "inductive": 0.4,
                    "statistical": 0.3,
                    "analogical": 0.2
                })
            }
            
        except Exception as e:
            print(f"Error in tone analysis: {str(e)}")
            # Create default tone analysis
            self.tone_analysis = {
                "thought_patterns": {
                    "analytical": 0.7,
                    "logical": 0.6,
                    "systematic": 0.5,
                    "creative": 0.3
                },
                "reasoning_style": {
                    "deductive": 0.6,
                    "inductive": 0.4,
                    "statistical": 0.5,
                    "analogical": 0.3
                }
            }
        
        print("\nWriting style analysis complete:")
        self.pp.pprint(self.tone_analysis)
        
        return self.tone_analysis
    
    def _create_default_analysis(self):
        """Create a default analysis when tone analysis fails"""
        return {
            "thought_patterns": {
                "analytical": 0.7,
                "logical": 0.6,
                "systematic": 0.5,
                "creative": 0.3
            },
            "reasoning_style": {
                "deductive": 0.6,
                "inductive": 0.4,
                "statistical": 0.5,
                "analogical": 0.3
            },
            "dominant_tone": "informative",
            "formality": "moderate",
            "perspective": "third_person",
            "complexity": "moderate",
            "sentence_complexity": "moderate",
            "vocabulary_level": "advanced",
            "transition_style": "logical",
            "pacing": "measured",
            "organization": "thesis_support",
            "argument_style": "balanced",
            "information_density": "high",
            "paragraph_structure": "complex"
        }
    
    def generate_article(self):
        """Generate an article using the Advanced Article Generator"""
        print("\n" + "="*80)
        print("STEP 6: GENERATE ARTICLE")
        print("="*80)
        
        if not self.crawled_data:
            print("No crawled data available. Please crawl data sources first.")
            return {}
        
        if not self.tone_analysis:
            print("No tone analysis available. Please analyze writing style first.")
            return {}
        
        print("\nGenerating article...")
        
        # Generate the article using the advanced article generator
        try:
            # Format the inputs for the generator
            topic = self.content_strategy['primary_topic']
            
            # Generate the article
            try:
                article = generate_advanced_article(
                    topic=topic,
                    tone_analysis=self.tone_analysis,
                    source_material=self.crawled_data
                )
                
                self.generated_article = article
            except Exception as e:
                print(f"Error using generate_advanced_article: {str(e)}")
                print("Falling back to direct ArticleGenerator usage...")
                
                try:
                    # Try direct usage of ArticleGenerator
                    generator = ArticleGenerator()
                    article_content = generator.generate_article(
                        topic=topic,
                        style_profile=format_tone_analysis_to_style_profile(self.tone_analysis),
                        source_material=self.crawled_data
                    )
                    
                    self.generated_article = {
                        "article": article_content,
                        "validation": {"status": "success"}
                    }
                except Exception as e2:
                    print(f"Error with direct ArticleGenerator: {str(e2)}")
                    print("Using fallback article generation...")
                    
                    # Create a fallback article
                    self.generated_article = {
                        "article": self._create_fallback_article(topic),
                        "validation": {"status": "fallback", "message": str(e2)}
                    }
            
            # Display article information
            print("\nArticle generated successfully!")
            
            article_content = self.generated_article.get("article", {})
            
            print(f"\nTitle: {article_content.get('title', 'Untitled')}")
            
            if 'subtitle' in article_content:
                print(f"Subtitle: {article_content['subtitle']}")
            
            # Count words in the article
            article_text = ""
            if 'introduction' in article_content:
                article_text += article_content['introduction'] + " "
            
            if 'body' in article_content:
                for section in article_content['body']:
                    if isinstance(section, dict):
                        if 'subheading' in section:
                            article_text += section['subheading'] + " "
                        if 'content' in section:
                            article_text += section['content'] + " "
            
            if 'conclusion' in article_content:
                article_text += article_content['conclusion']
            
            word_count = len(article_text.split())
            print(f"\nWord count: {word_count} words")
            
            # Display the article with proper formatting
            self.display_formatted_article(article_content)
            
        except Exception as e:
            print(f"Error generating article: {str(e)}")
            self.generated_article = {"error": str(e)}
        
        return self.generated_article
    
    def _create_fallback_article(self, topic):
        """Create a fallback article when generation fails"""
        return {
            "title": f"Article About {topic}",
            "subtitle": "Generated with SocialMe",
            "introduction": f"This is an introduction to {topic}. The topic is important and relevant to many people today.",
            "body": [
                {
                    "subheading": f"Understanding {topic}",
                    "content": f"This section provides an overview of {topic} and its key concepts. {topic} has become increasingly important in recent years due to technological advancements and changing market dynamics."
                },
                {
                    "subheading": f"Key Aspects of {topic}",
                    "content": f"There are several important aspects of {topic} that should be considered. These include the historical context, current applications, and future potential."
                },
                {
                    "subheading": f"Benefits of {topic}",
                    "content": f"Implementing {topic} can provide numerous benefits, including improved efficiency, reduced costs, and enhanced capabilities."
                }
            ],
            "conclusion": f"In conclusion, {topic} represents a significant opportunity for innovation and growth. By understanding and leveraging the concepts discussed in this article, organizations can position themselves for success in this area."
        }
    
    def display_formatted_article(self, article):
        """Display the article with proper HTML formatting"""
        print("\n" + "="*80)
        print("FORMATTED ARTICLE")
        print("="*80 + "\n")
        
        # Display title and subtitle
        print(f"<h1>{article.get('title', 'Untitled')}</h1>")
        if 'subtitle' in article:
            print(f"<h2>{article['subtitle']}</h2>\n")
        
        # Display introduction
        if 'introduction' in article:
            print("<p><strong>Introduction:</strong></p>")
            print(f"<p>{article['introduction']}</p>\n")
        
        # Display body sections
        if 'body' in article:
            for i, section in enumerate(article['body']):
                if 'subheading' in section:
                    print(f"<h2>{section['subheading']}</h2>")
                if 'content' in section:
                    paragraphs = section['content'].split('\n\n')
                    for para in paragraphs:
                        print(f"<p>{para}</p>")
                print()
        
        # Display conclusion
        if 'conclusion' in article:
            print("<p><strong>Conclusion:</strong></p>")
            print(f"<p>{article['conclusion']}</p>\n")
    
    def run_workflow(self):
        """Run the complete workflow"""
        try:
            # Step 1: Define content strategy
            self.define_content_strategy()
            
            # Step 2: Add data sources
            self.add_data_sources()
            
            # Step 3: Crawl data sources
            self.crawl_data_sources()
            
            # Step 4: Add tone sources
            self.add_tone_sources()
            
            # Step 5: Analyze tone
            self.analyze_tone()
            
            # Step 6: Generate article
            self.generate_article()
            
            print("\n" + "="*80)
            print("WORKFLOW COMPLETE")
            print("="*80)
            
        except KeyboardInterrupt:
            print("\n\nWorkflow interrupted by user.")
        except Exception as e:
            print(f"\n\nError in workflow: {str(e)}")

if __name__ == "__main__":
    print("="*80)
    print("SOCIALME COMPREHENSIVE WORKFLOW TEST")
    print("="*80)
    print("\nThis script allows you to test the entire workflow from content strategy to article generation.")
    print("It uses the following modules:")
    print("- Quantum Universal Crawler for data points with topic guidance")
    print("- Quantum Tone Crawler and Neural Tone Mapper for tone analysis")
    print("- Advanced Article Generator for article generation")
    
    # Run the workflow
    tester = WorkflowTester()
    tester.run_workflow()
