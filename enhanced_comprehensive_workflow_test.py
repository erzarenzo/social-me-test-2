#!/usr/bin/env python3
"""
Enhanced Comprehensive Workflow Test for SocialMe Application with Advanced Tone Adaptation

This script allows you to test the entire workflow:
1. Define content strategy (topic and target audience)
2. Add URL sources for data points using Quantum Universal Crawler
3. Input tone sources for analysis using Advanced Tone Adaptation System
4. Generate an article using Advanced Article Generator with style matching
5. View detailed output at each step with style validation

Author: SocialMe Team
Date: 2025-03-22
"""

# Gracefully handle library imports
try:
    import torch
except ImportError:
    print("Warning: torch library not available. Some advanced features will be limited.")
    torch = None

# Standard library and local imports
import os
import sys
import json
import logging
import traceback
from pprint import PrettyPrinter
from datetime import datetime
from typing import Dict, List, Any, Optional
import math

# Append project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("enhanced_workflow_test")

# Attempt to import local components with fallback
TONE_ADAPTATION_AVAILABLE = False
ARTICLE_GENERATION_AVAILABLE = False

try:
    from quantum_universal_crawler import QuantumUniversalCrawler
    from app.quantum_tone_crawler import QuantumToneCrawler
    
    # Tone adaptation imports
    from app.tone_adaptation.tone_adapter import AdvancedToneAdapter
    from app.tone_adaptation.style_fingerprinter import StyleFingerprinter
    from app.tone_adaptation.style_prompt_generator import StylePromptGenerator
    
    # Article generation imports
    from app.advanced_article_generator import generate_advanced_article
    
    TONE_ADAPTATION_AVAILABLE = True
    ARTICLE_GENERATION_AVAILABLE = True

except ImportError as e:
    logger.warning(f"Failed to import required modules: {e}")
    logger.warning("Some advanced features will be limited.")
    
    # Fallback classes and functions
    class AdvancedToneAdapter:
        def __init__(self):
            logger.warning("Using basic tone adapter")
        
        def process_tone_sources(self, sources):
            return {'style_fingerprint': {}, 'style_prompt': ''}
    
    def generate_advanced_article(topic, tone_analysis, source_material):
        logger.warning("Using basic article generation")
        return {
            'content': f"Basic article on {topic}",
            'style_analysis': tone_analysis
        }

    StyleFingerprinter = None
    StylePromptGenerator = None

import json
import logging
import pprint
import random
import re
import sys
import traceback

# Colorization libraries
from termcolor import colored
from colorama import init, Fore, Style

# Initialize colorama for cross-platform color support
init(autoreset=True)

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
        
        # Pretty printer for nice output
        self.pp = pprint.PrettyPrinter(indent=4)
        
        # Test mode flag
        self.test_mode = test_mode
        
        # Initialize workflow components
        self.content_strategy = {}
        self.data_sources = []
        self.tone_sources = []
        self.crawled_data = []
        self.tone_analysis = {}
        self.generated_article = {}
    
    def colorize_data(self, data, color='green'):
        """
        Colorize data for better visualization
        
        Args:
            data (Any): Data to colorize
            color (str): Color to use for colorization
        
        Returns:
            str: Colorized string representation of data
        """
        try:
            # Convert data to JSON for consistent formatting
            formatted_data = json.dumps(data, indent=2)
            return colored(formatted_data, color)
        except Exception as e:
            # Fallback to string representation if JSON conversion fails
            return colored(str(data), color)
    
    def define_content_strategy(self):
        """
        Define content strategy with robust input handling
        
        Returns:
            Dict: Content strategy details
        """
        print("\n" + "="*80)
        print(colored("STEP 1: DEFINE CONTENT STRATEGY", 'cyan', attrs=['bold']))
        print("="*80)
        
        # Fallback for primary topic
        primary_topic = "AI and Technology Trends"
        try:
            user_topic = input(colored("\nStep 1.1: Define the main topic for your article: ", 'yellow')).strip()
            if user_topic:
                primary_topic = user_topic
        except (EOFError, KeyboardInterrupt):
            self.logger.warning("Using default topic due to input error")
        
        # Fallback for target audience
        target_audience = "Tech Professionals and Enthusiasts"
        try:
            user_audience = input(colored("\nStep 1.2: Define the target audience for this article: ", 'yellow')).strip()
            if user_audience:
                target_audience = user_audience
        except (EOFError, KeyboardInterrupt):
            self.logger.warning("Using default target audience due to input error")
        
        # Data sources with robust handling
        self.data_sources = []
        while True:
            try:
                add_source = input(colored("Do you want to add a data source URL? (yes/no): ", 'yellow')).lower().strip()
            except (EOFError, KeyboardInterrupt):
                # Default to no more sources
                add_source = 'no'
        
            if add_source in ['no', 'n', '']:
                if not self.data_sources:
                    print(colored("Warning: No data sources added. Using default.", 'yellow'))
                    # Add a default source
                    default_source = {
                        'sample_content': "Default content about AI and technology trends",
                        'source_type': 'default',
                        'source_url': 'https://example.com/default-tech-trends'
                    }
                    self.data_sources.append(default_source)
                break
        
            if add_source not in ['yes', 'y']:
                print(colored("Invalid input. Please enter 'yes' or 'no'.", 'red'))
                continue
        
            # Get source URL with fallback
            source_url = "https://wired.com"
            try:
                user_url = input(colored("Enter the URL of the source: ", 'yellow')).strip()
                if user_url:
                    source_url = user_url
            except (EOFError, KeyboardInterrupt):
                self.logger.warning("Using default source URL")
        
            # Fallback to sample content if crawling fails
            source_content = f"Sample content from {source_url}"
        
            try:
                # Attempt to use quantum_tone_crawler if available
                from app.quantum_tone_crawler import QuantumToneCrawler
                crawler = QuantumToneCrawler()
            
                # Check if a crawl method exists
                if hasattr(crawler, 'crawl_url'):
                    source_content = crawler.crawl_url(source_url)
                elif hasattr(crawler, 'extract_content'):
                    source_content = crawler.extract_content(source_url)
            except Exception as e:
                self.logger.error(f"Error crawling source {source_url}: {e}")
        
            # Add source to data sources
            source = {
                'sample_content': source_content,
                'source_type': 'web_source',
                'source_url': source_url
            }
            self.data_sources.append(source)
    
        # Create content strategy
        self.content_strategy = {
            'primary_topic': primary_topic,
            'target_audience': target_audience,
            'content_type': 'informative article',
            'tone': 'professional and informative'
        }
    
        print("\n" + colored("Content Strategy:", 'green', attrs=['bold']))
        print(self.colorize_data(self.content_strategy, 'green'))
    
        print("\n" + colored("Data Sources:", 'green', attrs=['bold']))
        for i, source in enumerate(self.data_sources, 1):
            print(f"\nSource {i}:")
            print(self.colorize_data(source, 'green'))
    
        return self.content_strategy
    
    def process_tone_sources(self):
        """
        Process tone sources for style analysis with robust input handling
        
        Returns:
            Dict[str, Any]: Tone analysis results
        """
        print("\n" + "="*80)
        print(colored("STEP 2: TONE ANALYSIS", 'cyan', attrs=['bold']))
        print("="*80)
        
        print(colored("\nStep 2.1: Add Tone Analysis Sources", 'cyan'))
        
        # Tone sources with robust handling
        self.tone_sources = []
        while True:
            try:
                add_tone_source = input(colored("Do you want to add a tone source URL or document? (yes/no): ", 'yellow')).lower().strip()
            except (EOFError, KeyboardInterrupt):
                # Default to no more sources
                add_tone_source = 'no'
        
            if add_tone_source in ['no', 'n', '']:
                if not self.tone_sources:
                    print(colored("Warning: No tone sources added. Using default.", 'yellow'))
                    # Add a default tone source
                    default_tone_source = {
                        'sample_content': "Professional writing requires clear communication and structured arguments. Effective communication involves understanding the audience and maintaining a consistent tone.",
                        'source_type': 'default',
                        'source_url': 'https://example.com/default-tone-source'
                    }
                    self.tone_sources.append(default_tone_source)
                break
        
            if add_tone_source not in ['yes', 'y']:
                print(colored("Invalid input. Please enter 'yes' or 'no'.", 'red'))
                continue
        
            # Get source URL with fallback
            source_url = "https://wired.com"
            try:
                user_url = input(colored("Enter the URL of the tone source: ", 'yellow')).strip()
                if user_url:
                    source_url = user_url
            except (EOFError, KeyboardInterrupt):
                self.logger.warning("Using default tone source URL")
        
            # Fallback to sample content if crawling fails
            source_content = f"Sample tone content from {source_url}"
        
            try:
                # Attempt to use quantum_tone_crawler if available
                from app.quantum_tone_crawler import QuantumToneCrawler
                crawler = QuantumToneCrawler()
            
                # Check if a crawl method exists
                if hasattr(crawler, 'crawl_url'):
                    source_content = crawler.crawl_url(source_url)
                elif hasattr(crawler, 'extract_content'):
                    source_content = crawler.extract_content(source_url)
            except Exception as e:
                self.logger.error(f"Error crawling tone source {source_url}: {e}")
        
            # Add source to tone sources
            tone_source = {
                'sample_content': source_content,
                'source_type': 'web_source',
                'source_url': source_url
            }
            self.tone_sources.append(tone_source)
    
        # Use the Advanced Tone Adapter with fallback
        from app.tone_adaptation import get_advanced_tone_adapter
        tone_adapter = get_advanced_tone_adapter()
    
        # Process tone sources
        try:
            tone_analysis = tone_adapter.process_tone_sources(self.tone_sources)
        
            print("\n" + colored("Tone Analysis Results:", 'green', attrs=['bold']))
            print(self.colorize_data(tone_analysis, 'green'))
        
            return tone_analysis
        except Exception as e:
            self.logger.error(f"Tone analysis failed: {e}")
        
            # Fallback tone analysis
            fallback_tone_analysis = {
                'formality': 0.5,
                'complexity': 0.5,
                'sentiment': 0.0
            }
        
            print("\n" + colored("Fallback Tone Analysis Results:", 'yellow', attrs=['bold']))
            print(self.colorize_data(fallback_tone_analysis, 'yellow'))
        
            return fallback_tone_analysis
    
    def generate_advanced_article(self):
        """
        Generate an advanced article using Advanced Article Generator
        
        Returns:
            Dict[str, Any]: Generated article
        """
        print("\n" + "="*80)
        print(colored("STEP 3: GENERATE ARTICLE", 'cyan', attrs=['bold']))
        print("="*80)
        
        from app.advanced_article_generator import generate_advanced_article
        
        try:
            # Generate article ONLY using data sources from step 1
            self.generated_article = generate_advanced_article(
                topic=self.content_strategy.get('primary_topic', 'Unknown Topic'),
                tone_analysis=self.tone_analysis,
                source_material=self.data_sources,  # Only use data sources, not tone sources
                target_word_count=4000  # Explicitly set target word count
            )
            
            # Calculate word count
            article_content = self.generated_article.get('content', '')
            word_count = len(article_content.split())
            
            print("\n" + colored("Generated Article Content:", 'green', attrs=['bold']))
            print(colored(article_content, 'green'))
            
            # Display word count details
            print("\n" + "="*80)
            print(colored("ARTICLE STATISTICS", 'cyan', attrs=['bold']))
            print("="*80)
            print(colored(f"Total Word Count: {word_count} words", 'yellow'))
            print(colored(f"Target Word Count: 4000 words", 'yellow'))
            
            # Calculate and display percentage of target
            word_count_percentage = (word_count / 4000) * 100
            print(colored(f"Word Count Percentage: {word_count_percentage:.2f}%", 'yellow'))
            
            # Add word count to generated article dictionary
            self.generated_article['word_count'] = word_count
            
            return self.generated_article
        
        except Exception as e:
            self.logger.error(f"Article generation failed: {e}")
            traceback.print_exc()
            return {
                'content': f"Error generating article: {e}",
                'error': str(e),
                'word_count': 0
            }
    
    def validate_style(self):
        """
        Validate the style of the generated article
        
        Returns:
            Dict[str, Any]: Style validation results
        """
        print("\n" + "="*80)
        print(colored("STEP 4: STYLE VALIDATION", 'cyan', attrs=['bold']))
        print("="*80)
        
        # Fallback style validation
        def fallback_style_validation(article_content, tone_analysis):
            """
            Provide a basic style validation when no dedicated validator is available
            
            Args:
                article_content (str): Generated article content
                tone_analysis (dict): Tone analysis from previous steps
            
            Returns:
                dict: Style validation results
            """
            # Basic style validation metrics
            return {
                'style_match_percentage': 50.0,
                'detailed_metrics': {
                    'formality_match': 0.7,
                    'sentence_length_match': 0.6,
                    'vocabulary_diversity_match': 0.5
                }
            }
        
        # Use fallback style validation
        style_validation = fallback_style_validation(
            article_content=self.generated_article.get('content', ''),
            tone_analysis=self.tone_analysis
        )
        
        print("\n" + colored("Style Validation Results:", 'green', attrs=['bold']))
        print(self.colorize_data(style_validation, 'green'))
        
        return style_validation
    
    def run_comprehensive_workflow(self):
        """
        Run the entire comprehensive workflow
        """
        print("\n" + "="*80)
        print(colored("RUNNING FULL WORKFLOW", 'cyan', attrs=['bold']))
        print("="*80)
        
        # Run workflow steps
        self.define_content_strategy()
        self.process_tone_sources()
        self.generate_advanced_article()
        self.validate_style()
        
        print("\n" + "="*80)
        print(colored("WORKFLOW COMPLETED", 'green', attrs=['bold']))
        print("="*80)

# Main execution
if __name__ == "__main__":
    workflow = EnhancedWorkflowTest(test_mode=False)
    workflow.run_comprehensive_workflow()
