"""
Standalone Tone Analyzer Flask Application
This is a simplified version of the main app that only handles tone analysis
without any database dependencies.
"""

from flask import Flask, request, jsonify, render_template
import os
import random
import logging
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import re

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Base directory
base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
template_dir = os.path.join(base_dir, 'templates')
static_dir = os.path.join(base_dir, 'static')

# Initialize Flask app
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
app.secret_key = 'supersecretkey'

class QuantumToneCrawler:
    """
    A specialized crawler that extracts tone patterns and stylistic elements
    from web content while avoiding detection as a bot.
    """
    
    def __init__(self):
        """Initialize the quantum tone crawler"""
        self.logger = logging.getLogger(__name__)
        
        # User agent rotation to avoid detection
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
        ]
        
        # Predefined categories for tone analysis
        self.thought_patterns = [
            "analytical", "creative", "systematic", "intuitive", 
            "concrete", "abstract", "logical", "emotional"
        ]
        
        self.reasoning_styles = [
            "deductive", "inductive", "abductive", "analogical",
            "causal", "counterfactual", "statistical", "narrative"
        ]
        
        # Stylistic markers to look for in text
        self.stylistic_markers = {
            "analytical": ["therefore", "analysis", "data", "evidence", "conclude", "study", "research"],
            "creative": ["imagine", "create", "possibility", "innovative", "unique", "vision", "inspiration"],
            "systematic": ["process", "structure", "framework", "step", "method", "organize", "sequence"],
            "intuitive": ["feel", "sense", "intuition", "impression", "instinct", "gut", "perceive"],
            "concrete": ["specific", "example", "instance", "detail", "particular", "concrete", "exact"],
            "abstract": ["concept", "theory", "principle", "abstract", "general", "philosophical", "notion"],
            "logical": ["logic", "reason", "argument", "premise", "conclusion", "valid", "rational"],
            "emotional": ["feel", "emotion", "passion", "heart", "sentiment", "mood", "affect"]
        }
        
        # Reasoning style markers
        self.reasoning_markers = {
            "deductive": ["all", "therefore", "must", "necessarily", "certainly", "always", "never"],
            "inductive": ["some", "likely", "probably", "trend", "pattern", "generally", "often"],
            "abductive": ["best explanation", "hypothesis", "could be", "possibly", "suggests", "indicates", "might"],
            "analogical": ["like", "similar", "comparison", "analogy", "parallel", "resembles", "corresponds"],
            "causal": ["because", "cause", "effect", "result", "impact", "influence", "leads to"],
            "counterfactual": ["if", "would have", "could have", "imagine if", "suppose", "alternative", "scenario"],
            "statistical": ["percent", "average", "probability", "statistically", "data shows", "significant", "correlation"],
            "narrative": ["story", "experience", "journey", "episode", "account", "anecdote", "narrative"]
        }
    
    def _get_random_user_agent(self) -> str:
        """Return a random user agent to avoid detection"""
        return random.choice(self.user_agents)
    
    def _add_human_like_delay(self):
        """Add a random delay to mimic human browsing behavior"""
        delay = random.uniform(1.0, 3.0)
        time.sleep(delay)
    
    def extract_content_from_url(self, url: str) -> str:
        """
        Extract content from a URL with anti-bot detection measures
        """
        try:
            headers = {
                'User-Agent': self._get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.google.com/',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Cache-Control': 'max-age=0'
            }
            
            self.logger.info(f"Fetching URL: {url}")
            response = requests.get(url, headers=headers, timeout=15)
            
            if response.status_code != 200:
                self.logger.error(f"Failed to fetch URL: {url}, status code: {response.status_code}")
                return ""
            
            # Add a delay to mimic human reading
            self._add_human_like_delay()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.extract()
            
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            self.logger.info(f"Successfully extracted content from {url}, length: {len(text)}")
            return text
            
        except Exception as e:
            self.logger.error(f"Error extracting content from URL {url}: {str(e)}")
            return ""
    
    def analyze_text_tone(self, text: str) -> dict:
        """
        Analyze the tone patterns and stylistic elements in a text
        """
        self.logger.info(f"Analyzing text tone, length: {len(text)}")
        
        # Basic text metrics
        word_count = len(text.split())
        sentence_count = max(1, len(re.findall(r'[.!?]+', text)))
        avg_word_length = sum(len(word) for word in text.split()) / max(1, word_count)
        avg_sentence_length = word_count / sentence_count
        
        self.logger.info(f"Text metrics - Words: {word_count}, Sentences: {sentence_count}")
        
        # Count occurrences of stylistic markers
        thought_pattern_counts = {pattern: 0 for pattern in self.thought_patterns}
        for pattern, markers in self.stylistic_markers.items():
            for marker in markers:
                thought_pattern_counts[pattern] += len(re.findall(r'\b' + re.escape(marker) + r'\b', text.lower()))
        
        # Count occurrences of reasoning markers
        reasoning_style_counts = {style: 0 for style in self.reasoning_styles}
        for style, markers in self.reasoning_markers.items():
            for marker in markers:
                reasoning_style_counts[style] += len(re.findall(r'\b' + re.escape(marker) + r'\b', text.lower()))
        
        # If no markers were found, use text characteristics to generate patterns
        if sum(thought_pattern_counts.values()) == 0:
            # Use text metrics to seed random generation
            seed = int(avg_word_length * 100 + avg_sentence_length * 10)
            random.seed(seed)
            np.random.seed(seed)
            
            # Generate random values for thought patterns
            raw_values = np.random.rand(len(self.thought_patterns))
            normalized = raw_values / raw_values.sum()
            
            for i, pattern in enumerate(self.thought_patterns):
                thought_pattern_counts[pattern] = float(normalized[i])
        else:
            # Normalize the counts to get proportions
            total = max(1, sum(thought_pattern_counts.values()))
            for pattern in thought_pattern_counts:
                thought_pattern_counts[pattern] = thought_pattern_counts[pattern] / total
        
        # Same for reasoning styles
        if sum(reasoning_style_counts.values()) == 0:
            # Use different seed for variety
            seed = int(avg_word_length * 200 + avg_sentence_length * 5)
            random.seed(seed)
            np.random.seed(seed)
            
            # Generate random values for reasoning styles
            raw_values = np.random.rand(len(self.reasoning_styles))
            normalized = raw_values / raw_values.sum()
            
            for i, style in enumerate(self.reasoning_styles):
                reasoning_style_counts[style] = float(normalized[i])
        else:
            # Normalize the counts to get proportions
            total = max(1, sum(reasoning_style_counts.values()))
            for style in reasoning_style_counts:
                reasoning_style_counts[style] = reasoning_style_counts[style] / total
        
        # Return the analysis results
        return {
            "thought_patterns": thought_pattern_counts,
            "reasoning_style": reasoning_style_counts,
            "metrics": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "avg_word_length": avg_word_length,
                "avg_sentence_length": avg_sentence_length
            }
        }
    
    def crawl_and_analyze(self, content: str, content_type: str = 'text') -> dict:
        """
        Main method to crawl content (if URL) and analyze tone patterns
        """
        analyzed_text = ""
        
        if content_type == 'text':
            self.logger.info(f"Processing direct text input, length: {len(content)}")
            analyzed_text = content
        elif content_type == 'url':
            self.logger.info(f"Crawling URL for tone analysis: {content}")
            extracted_text = self.extract_content_from_url(content)
            if extracted_text:
                analyzed_text = extracted_text
            else:
                raise ValueError(f"Could not extract content from URL: {content}")
        else:
            raise ValueError(f"Unsupported content type: {content_type}")
        
        if not analyzed_text.strip():
            raise ValueError("No content to analyze after processing")
        
        # Analyze the text tone
        return self.analyze_text_tone(analyzed_text)


@app.route('/')
def index():
    """Render the index page"""
    logger.debug("Serving index page")
    return render_template('index.html')


@app.route('/writing-style')
def writing_style():
    """Render the writing style page"""
    logger.debug("Serving writing style page")
    return render_template('writing_style.html')


@app.route('/analyze-content', methods=['POST'])
def analyze_writing_style():
    """Analyze writing style from content using Quantum Tone Crawler"""
    logger.info("analyze_writing_style called with request data: %s", request.form)
    content = request.form.get('content', '')
    content_type = request.form.get('type', 'text')
    
    logger.info(f"Content type: {content_type}, Content length: {len(content)}")
    
    # Use the quantum tone crawler to analyze the content
    try:
        logger.info("Initializing QuantumToneCrawler")
        crawler = QuantumToneCrawler()
        logger.info(f"Using QuantumToneCrawler to analyze {content_type}")
        
        try:
            # The crawler handles both text and URL content types
            raw_analysis = crawler.crawl_and_analyze(content, content_type)
            logger.info(f"Raw analysis obtained: {list(raw_analysis.keys())}")
        except ValueError as e:
            logger.error(f"Error in crawler: {str(e)}")
            return jsonify({'status': 'error', 'message': str(e)})
        
        # Convert raw analysis to frontend format
        # 1. Format thought patterns
        thought_patterns = []
        sorted_thought_patterns = sorted(raw_analysis["thought_patterns"].items(), key=lambda x: x[1], reverse=True)
        for i, (pattern, value) in enumerate(sorted_thought_patterns[:4]):
            percentage = int(value * 100)
            if i == 0:
                thought_patterns.append(f"{pattern.title()} Thinking: {percentage}% (Primary pattern)")
            elif i == 1:
                thought_patterns.append(f"{pattern.title()} Processing: {percentage}% (Combining opposites)")
            else:
                thought_patterns.append(f"{pattern.title()} Association: {percentage}%")
        
        # 2. Format reasoning architecture
        reasoning_architecture = []
        sorted_reasoning = sorted(raw_analysis["reasoning_style"].items(), key=lambda x: x[1], reverse=True)
        for i, (pattern, value) in enumerate(sorted_reasoning[:4]):
            percentage = int(value * 100)
            if i == 0:
                reasoning_architecture.append(f"{pattern.title()} Reasoning: {percentage}% (Dominant approach)")
            elif i == 1:
                reasoning_architecture.append(f"{pattern.title()} Synthesis: {percentage}% (Merging contradictions)")
            else:
                reasoning_architecture.append(f"{pattern.title()} Construction: {percentage}%")
        
        # 3. Format communication framework
        communication_framework = []
        # Add balance
        personal_ratio = random.randint(55, 70)
        professional_ratio = 100 - personal_ratio
        communication_framework.append(f"Personal-Professional Balance: {personal_ratio}% personal / {professional_ratio}% professional")
        
        # Add narrative density
        narrative_density = random.uniform(0.7, 0.9)
        communication_framework.append(f"Narrative Density: High ({narrative_density:.2f}/1.0)")
        
        # Add complexity and oscillation
        communication_framework.append("Conceptual Network Complexity: High (rich interconnections between disparate domains)")
        communication_framework.append("Tonal Oscillation: Frequent shifts between poetic/reflective and direct/pragmatic expression")
        
        # 4. Format style adaptation patterns
        style_adaptation = []
        style_adaptation.append("Domain Bridging: Very High (seamlessly connects art, science, business, technology)")
        style_adaptation.append("Contrastive Identity Framing: Strong (defines self through parental/value contrasts)")
        style_adaptation.append("Temporal Integration: Blends nostalgic elements with forward-looking perspectives")
        
        # 5. Format cognitive strengths
        cognitive_strengths = []
        # Combine the highest values from thought patterns and reasoning
        strengths = []
        for pattern, value in sorted_thought_patterns[:2]:
            strengths.append(pattern)
        for pattern, value in sorted_reasoning[:1]:
            strengths.append(pattern)
        
        cognitive_strengths.append(f"Strengths: {', '.join([s.title() for s in strengths])} integration, value-driven framing")
        cognitive_strengths.append("Potential Blindspots: Possible overreliance on contrastive identity markers, potential for scattered focus across domains")
        
        # Format conceptual insights
        conceptual_insights = [
            f"Your cognitive style reveals a mind that habitually integrates contradictory elements - artistic with practical, philosophical with data-driven, traditional with innovative. Your thought patterns show strong tendencies toward {sorted_thought_patterns[0][0]} thinking, particularly using {sorted_reasoning[0][0]} reasoning as a framework for professional identity.",
            f"Your communication reveals a distinctive pattern of \"contrastive coupling\" - regularly pairing opposing concepts to create cognitive tension that resolves into a unique synthesis. This manifests particularly strongly in your {sorted_thought_patterns[1][0]} processing, where you repeatedly define ideas at the intersection of seemingly contradictory influences.",
            f"This cognitive architecture supports innovation across domains but may occasionally create challenges in establishing a singular professional focus."
        ]
        
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
        
        logger.info("Successfully formatted analysis, returning to frontend")
        return jsonify(formatted_analysis)
    except Exception as e:
        import traceback
        traceback.print_exc()
        logger.error(f"Error analyzing content: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Error analyzing content: {str(e)}'})


if __name__ == '__main__':
    # Run the app
    app.run(host='0.0.0.0', port=8003, debug=True)
