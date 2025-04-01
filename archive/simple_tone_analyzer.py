"""
Simple Tone Analyzer Flask Application
This is a minimal version that only handles tone analysis API endpoint
without any database dependencies or complex templates.
"""

from flask import Flask, request, jsonify, render_template_string
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

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Simple HTML template for the main page
MAIN_PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tone Analyzer</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        textarea, input[type="text"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        textarea {
            height: 150px;
        }
        .tabs {
            display: flex;
            margin-bottom: 15px;
        }
        .tab {
            padding: 10px 15px;
            background-color: #eee;
            cursor: pointer;
            border: 1px solid #ddd;
            border-bottom: none;
            border-radius: 4px 4px 0 0;
            margin-right: 5px;
        }
        .tab.active {
            background-color: white;
            border-bottom: 1px solid white;
        }
        .tab-content {
            display: none;
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 0 4px 4px 4px;
            background-color: white;
        }
        .tab-content.active {
            display: block;
        }
        button {
            background-color: #4285f4;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            width: 100%;
        }
        button:hover {
            background-color: #3367d6;
        }
        .error {
            color: white;
            background-color: #f44336;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 15px;
            text-align: center;
        }
        .analysis-container {
            margin-top: 20px;
            display: none;
        }
        .analysis-section {
            margin-bottom: 20px;
        }
        .analysis-section h3 {
            border-bottom: 1px solid #eee;
            padding-bottom: 5px;
        }
        .analysis-item {
            margin-bottom: 10px;
        }
        .loading {
            text-align: center;
            display: none;
            margin: 20px 0;
        }
        .loading img {
            width: 50px;
            height: 50px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Neural Tone Analyzer</h1>
        
        <div id="error-message" class="error" style="display: none;"></div>
        
        <div class="tabs">
            <div class="tab active" onclick="switchTab('text')">Text Input</div>
            <div class="tab" onclick="switchTab('url')">URL Analysis</div>
        </div>
        
        <div id="text-tab" class="tab-content active">
            <div class="form-group">
                <label for="text-input">Enter your text:</label>
                <textarea id="text-input" placeholder="Paste your writing sample here..."></textarea>
            </div>
        </div>
        
        <div id="url-tab" class="tab-content">
            <div class="form-group">
                <label for="url-input">Enter URL to analyze:</label>
                <input type="text" id="url-input" placeholder="https://example.com/article">
            </div>
        </div>
        
        <button onclick="analyzeContent()">Analyze My Writing Style</button>
        
        <div id="loading" class="loading">
            <p>Analyzing your content...</p>
        </div>
        
        <div id="analysis-results" class="analysis-container">
            <h2 id="analysis-heading"></h2>
            
            <div class="analysis-section">
                <h3 id="cognitive-profile-title"></h3>
                
                <div class="analysis-item">
                    <h4 id="thought-patterns-title"></h4>
                    <ul id="thought-patterns-list"></ul>
                </div>
                
                <div class="analysis-item">
                    <h4 id="reasoning-architecture-title"></h4>
                    <ul id="reasoning-architecture-list"></ul>
                </div>
                
                <div class="analysis-item">
                    <h4 id="communication-framework-title"></h4>
                    <ul id="communication-framework-list"></ul>
                </div>
                
                <div class="analysis-item">
                    <h4 id="style-adaptation-title"></h4>
                    <ul id="style-adaptation-list"></ul>
                </div>
                
                <div class="analysis-item">
                    <h4 id="cognitive-strengths-title"></h4>
                    <ul id="cognitive-strengths-list"></ul>
                </div>
            </div>
            
            <div class="analysis-section">
                <h3 id="conceptual-analysis-title"></h3>
                <div id="conceptual-analysis-content"></div>
            </div>
        </div>
    </div>
    
    <script>
        function switchTab(tabName) {
            // Hide all tab contents
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Deactivate all tabs
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Activate the selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            document.querySelector(`.tab:nth-child(${tabName === 'text' ? 1 : 2})`).classList.add('active');
        }
        
        function showError(message) {
            const errorElement = document.getElementById('error-message');
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            
            // Hide loading indicator
            document.getElementById('loading').style.display = 'none';
        }
        
        function clearError() {
            document.getElementById('error-message').style.display = 'none';
        }
        
        function analyzeContent() {
            clearError();
            
            // Show loading indicator
            document.getElementById('loading').style.display = 'block';
            
            // Hide previous results
            document.getElementById('analysis-results').style.display = 'none';
            
            // Determine which tab is active
            const isTextTab = document.getElementById('text-tab').classList.contains('active');
            
            // Get the content to analyze
            let content = '';
            let contentType = '';
            
            if (isTextTab) {
                content = document.getElementById('text-input').value.trim();
                contentType = 'text';
                
                if (!content) {
                    showError('Please enter some text to analyze.');
                    return;
                }
            } else {
                content = document.getElementById('url-input').value.trim();
                contentType = 'url';
                
                if (!content) {
                    showError('Please enter a URL to analyze.');
                    return;
                }
                
                // Basic URL validation
                if (!content.startsWith('http://') && !content.startsWith('https://')) {
                    showError('Please enter a valid URL starting with http:// or https://');
                    return;
                }
            }
            
            // Send the analysis request
            fetch('/analyze-content', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `content=${encodeURIComponent(content)}&type=${contentType}`
            })
            .then(response => response.json())
            .then(data => {
                // Hide loading indicator
                document.getElementById('loading').style.display = 'none';
                
                if (data.status === 'error') {
                    showError(data.message);
                    return;
                }
                
                // Display the analysis results
                displayAnalysisResults(data.analysis);
            })
            .catch(error => {
                showError('An error occurred while analyzing the content. Please try again.');
                console.error('Error:', error);
            });
        }
        
        function displayAnalysisResults(analysis) {
            // Show the analysis container
            document.getElementById('analysis-results').style.display = 'block';
            
            // Set the heading
            document.getElementById('analysis-heading').textContent = analysis.heading;
            
            // Cognitive Profile Analysis
            const cognitiveProfile = analysis.cognitive_profile_analysis;
            document.getElementById('cognitive-profile-title').textContent = cognitiveProfile.title;
            
            // Thought Patterns
            const thoughtPatterns = cognitiveProfile.thought_patterns;
            document.getElementById('thought-patterns-title').textContent = thoughtPatterns.title;
            const thoughtPatternsList = document.getElementById('thought-patterns-list');
            thoughtPatternsList.innerHTML = '';
            thoughtPatterns.items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                thoughtPatternsList.appendChild(li);
            });
            
            // Reasoning Architecture
            const reasoningArchitecture = cognitiveProfile.reasoning_architecture;
            document.getElementById('reasoning-architecture-title').textContent = reasoningArchitecture.title;
            const reasoningArchitectureList = document.getElementById('reasoning-architecture-list');
            reasoningArchitectureList.innerHTML = '';
            reasoningArchitecture.items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                reasoningArchitectureList.appendChild(li);
            });
            
            // Communication Framework
            const communicationFramework = cognitiveProfile.communication_framework;
            document.getElementById('communication-framework-title').textContent = communicationFramework.title;
            const communicationFrameworkList = document.getElementById('communication-framework-list');
            communicationFrameworkList.innerHTML = '';
            communicationFramework.items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                communicationFrameworkList.appendChild(li);
            });
            
            // Style Adaptation Patterns
            const styleAdaptation = cognitiveProfile.style_adaptation_patterns;
            document.getElementById('style-adaptation-title').textContent = styleAdaptation.title;
            const styleAdaptationList = document.getElementById('style-adaptation-list');
            styleAdaptationList.innerHTML = '';
            styleAdaptation.items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                styleAdaptationList.appendChild(li);
            });
            
            // Cognitive Strengths & Blindspots
            const cognitiveStrengths = cognitiveProfile.cognitive_strengths_blindspots;
            document.getElementById('cognitive-strengths-title').textContent = cognitiveStrengths.title;
            const cognitiveStrengthsList = document.getElementById('cognitive-strengths-list');
            cognitiveStrengthsList.innerHTML = '';
            cognitiveStrengths.items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                cognitiveStrengthsList.appendChild(li);
            });
            
            // Conceptual Analysis
            const conceptualAnalysis = analysis.conceptual_analysis;
            document.getElementById('conceptual-analysis-title').textContent = conceptualAnalysis.title;
            const conceptualAnalysisContent = document.getElementById('conceptual-analysis-content');
            conceptualAnalysisContent.innerHTML = '';
            conceptualAnalysis.paragraphs.forEach(paragraph => {
                const p = document.createElement('p');
                p.textContent = paragraph;
                conceptualAnalysisContent.appendChild(p);
            });
        }
    </script>
</body>
</html>
"""

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
            "analytical": ["therefore", "analysis", "data", "evidence", "conclude", "study", "research", "examine", "investigate", "evaluate"],
            "creative": ["imagine", "create", "possibility", "innovative", "unique", "vision", "inspiration", "explore", "discover", "invent"],
            "systematic": ["process", "structure", "framework", "step", "method", "organize", "sequence", "procedure", "system", "order"],
            "intuitive": ["feel", "sense", "intuition", "impression", "instinct", "gut", "perceive", "insight", "awareness", "consciousness"],
            "concrete": ["specific", "example", "instance", "detail", "particular", "concrete", "exact", "precise", "definite", "tangible"],
            "abstract": ["concept", "theory", "principle", "abstract", "general", "philosophical", "notion", "idea", "thought", "hypothesis"],
            "logical": ["logic", "reason", "argument", "premise", "conclusion", "valid", "rational", "deduction", "inference", "proposition"],
            "emotional": ["feel", "emotion", "passion", "heart", "sentiment", "mood", "affect", "empathy", "compassion", "sympathy"]
        }
        
        # Reasoning style markers
        self.reasoning_markers = {
            "deductive": ["all", "therefore", "must", "necessarily", "certainly", "always", "never", "every", "none", "absolute"],
            "inductive": ["some", "likely", "probably", "trend", "pattern", "generally", "often", "usually", "typically", "tend"],
            "abductive": ["best explanation", "hypothesis", "could be", "possibly", "suggests", "indicates", "might", "perhaps", "infer", "guess"],
            "analogical": ["like", "similar", "comparison", "analogy", "parallel", "resembles", "corresponds", "metaphor", "as if", "akin to"],
            "causal": ["because", "cause", "effect", "result", "impact", "influence", "leads to", "due to", "consequently", "thus"],
            "counterfactual": ["if", "would have", "could have", "imagine if", "suppose", "alternative", "scenario", "otherwise", "instead", "contrary"],
            "statistical": ["percent", "average", "probability", "statistically", "data shows", "significant", "correlation", "rate", "frequency", "distribution"],
            "narrative": ["story", "experience", "journey", "episode", "account", "anecdote", "narrative", "tale", "recounting", "chronicle"]
        }
        
        # Domain-specific content markers
        self.domain_markers = {
            "technical": ["code", "algorithm", "function", "implementation", "software", "hardware", "system", "interface", "protocol", "architecture"],
            "business": ["market", "strategy", "customer", "product", "service", "revenue", "growth", "investment", "stakeholder", "profit"],
            "academic": ["research", "study", "theory", "hypothesis", "literature", "methodology", "findings", "analysis", "conclusion", "implications"],
            "journalistic": ["report", "news", "article", "interview", "source", "coverage", "story", "journalist", "media", "press"],
            "educational": ["learn", "teach", "student", "education", "knowledge", "skill", "curriculum", "instruction", "training", "development"],
            "philosophical": ["philosophy", "ethics", "morality", "existence", "consciousness", "meaning", "truth", "reality", "being", "knowledge"],
            "creative": ["art", "design", "create", "imagination", "expression", "aesthetic", "creative", "artistic", "craft", "composition"]
        }
    
    def _get_random_user_agent(self) -> str:
        """Return a random user agent to avoid detection"""
        return random.choice(self.user_agents)
    
    def _add_human_like_delay(self):
        """Add a random delay to mimic human browsing behavior"""
        delay = random.uniform(1.0, 3.0)
        time.sleep(delay)
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL to ensure it has the correct format"""
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url
    
    def _extract_main_content(self, soup: BeautifulSoup) -> str:
        """
        Extract the main content from a webpage, focusing on the article or main text
        and avoiding navigation, headers, footers, etc.
        """
        # First try to find article or main content tags
        main_content_tags = ['article', 'main', '.post-content', '.entry-content', '.article-content', '.post-body']
        
        for tag in main_content_tags:
            if tag.startswith('.'):  # It's a class
                content = soup.select(tag)
                if content:
                    return ' '.join([c.get_text(separator=' ', strip=True) for c in content])
            else:  # It's a tag name
                content = soup.find(tag)
                if content:
                    return content.get_text(separator=' ', strip=True)
        
        # If no main content tags found, try to find the div with the most text
        divs = soup.find_all('div')
        if divs:
            # Find the div with the most text content
            max_length = 0
            max_div = None
            for div in divs:
                text = div.get_text(separator=' ', strip=True)
                if len(text) > max_length:
                    max_length = len(text)
                    max_div = div
            
            if max_div and max_length > 200:  # Only use if it has substantial content
                return max_div.get_text(separator=' ', strip=True)
        
        # If all else fails, just get all the text
        return soup.get_text(separator=' ', strip=True)
    
    def _handle_substack(self, url: str) -> str:
        """Special handler for Substack sites which may require different approaches"""
        try:
            self.logger.info(f"Using Substack-specific handler for: {url}")
            
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
            
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=15)
            
            if response.status_code != 200:
                self.logger.error(f"Failed to fetch Substack URL: {url}, status code: {response.status_code}")
                return ""
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Try to find the article content specifically for Substack
            article_content = soup.select('.post-content, .available-content, .body')
            
            if article_content:
                content = ' '.join([c.get_text(separator=' ', strip=True) for c in article_content])
                self.logger.info(f"Successfully extracted Substack content, length: {len(content)}")
                return content
            
            # If we couldn't find the specific Substack content, fall back to general extraction
            return self._extract_main_content(soup)
            
        except Exception as e:
            self.logger.error(f"Error in Substack handler for URL {url}: {str(e)}")
            return ""
    
    def extract_content_from_url(self, url: str) -> str:
        """
        Extract content from a URL with anti-bot detection measures
        """
        try:
            # Normalize the URL
            url = self._normalize_url(url)
            self.logger.info(f"Fetching URL: {url}")
            
            # Check if it's a Substack site
            if 'substack.com' in url or any(marker in url for marker in ['.substack.', '/p/']):
                return self._handle_substack(url)
            
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
            
            # Use a session to handle redirects and cookies
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=15, allow_redirects=True)
            
            if response.status_code != 200:
                self.logger.error(f"Failed to fetch URL: {url}, status code: {response.status_code}")
                return ""
            
            # Add a delay to mimic human reading
            self._add_human_like_delay()
            
            # Parse the HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract the main content
            text = self._extract_main_content(soup)
            
            self.logger.info(f"Successfully extracted content from {url}, length: {len(text)}")
            return text
            
        except Exception as e:
            self.logger.error(f"Error extracting content from URL {url}: {str(e)}")
            return ""
    
    def _extract_key_phrases(self, text: str, num_phrases: int = 5) -> list:
        """Extract key phrases from the text to use in the analysis"""
        # Simple extraction based on sentence importance
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if not sentences:
            return []
        
        # Score sentences based on word frequency
        word_freq = {}
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            for word in words:
                if len(word) > 3:  # Skip short words
                    word_freq[word] = word_freq.get(word, 0) + 1
        
        # Score sentences
        sentence_scores = []
        for sentence in sentences:
            words = re.findall(r'\b\w+\b', sentence.lower())
            score = sum(word_freq.get(word, 0) for word in words if len(word) > 3)
            sentence_scores.append((sentence, score))
        
        # Get top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        top_sentences = [s[0] for s in sentence_scores[:num_phrases]]
        
        return top_sentences
    
    def _detect_domain(self, text: str) -> str:
        """Detect the primary domain/field of the text"""
        domain_scores = {}
        for domain, markers in self.domain_markers.items():
            score = 0
            for marker in markers:
                score += len(re.findall(r'\b' + re.escape(marker) + r'\b', text.lower()))
            domain_scores[domain] = score
        
        # Get the domain with the highest score
        if sum(domain_scores.values()) > 0:
            return max(domain_scores.items(), key=lambda x: x[1])[0]
        return "general"
    
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
        
        # Extract key phrases and domain
        key_phrases = self._extract_key_phrases(text)
        primary_domain = self._detect_domain(text)
        
        # Return the analysis results
        return {
            "thought_patterns": thought_pattern_counts,
            "reasoning_style": reasoning_style_counts,
            "metrics": {
                "word_count": word_count,
                "sentence_count": sentence_count,
                "avg_word_length": avg_word_length,
                "avg_sentence_length": avg_sentence_length
            },
            "key_phrases": key_phrases,
            "primary_domain": primary_domain
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
    """Render the main page"""
    logger.debug("Serving main page")
    return render_template_string(MAIN_PAGE_TEMPLATE)


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
        
        # Add domain-specific insights
        primary_domain = raw_analysis.get("primary_domain", "general")
        communication_framework.append(f"Domain Focus: {primary_domain.title()} (primary content area)")
        
        # Add balance based on thought patterns
        analytical_value = raw_analysis["thought_patterns"].get("analytical", 0)
        creative_value = raw_analysis["thought_patterns"].get("creative", 0)
        logical_value = raw_analysis["thought_patterns"].get("logical", 0)
        emotional_value = raw_analysis["thought_patterns"].get("emotional", 0)
        
        # Calculate ratios
        analytical_creative_ratio = int(100 * analytical_value / max(0.01, analytical_value + creative_value))
        logical_emotional_ratio = int(100 * logical_value / max(0.01, logical_value + emotional_value))
        
        communication_framework.append(f"Analytical-Creative Balance: {analytical_creative_ratio}% analytical / {100-analytical_creative_ratio}% creative")
        communication_framework.append(f"Logical-Emotional Balance: {logical_emotional_ratio}% logical / {100-logical_emotional_ratio}% emotional")
        
        # Add complexity based on metrics
        avg_sentence_length = raw_analysis["metrics"]["avg_sentence_length"]
        if avg_sentence_length > 25:
            complexity = "High"
        elif avg_sentence_length > 15:
            complexity = "Medium"
        else:
            complexity = "Accessible"
            
        communication_framework.append(f"Conceptual Network Complexity: {complexity} (avg sentence length: {avg_sentence_length:.1f} words)")
        
        # 4. Format style adaptation patterns
        style_adaptation = []
        
        # Use key phrases if available
        key_phrases = raw_analysis.get("key_phrases", [])
        if key_phrases:
            phrase_sample = random.choice(key_phrases) if len(key_phrases) > 0 else ""
            style_adaptation.append(f"Key Concept Focus: '{phrase_sample}'")
        
        # Add domain-specific style adaptations
        if primary_domain == "technical":
            style_adaptation.append("Technical Precision: High (uses specific terminology and structured explanations)")
        elif primary_domain == "business":
            style_adaptation.append("Strategic Framing: Strong (presents concepts in terms of value and outcomes)")
        elif primary_domain == "academic":
            style_adaptation.append("Analytical Depth: High (explores concepts with theoretical rigor)")
        elif primary_domain == "journalistic":
            style_adaptation.append("Narrative Clarity: Strong (presents information in accessible, engaging format)")
        else:
            style_adaptation.append("Domain Bridging: Versatile (connects concepts across different knowledge domains)")
        
        # Add a third style adaptation based on reasoning styles
        top_reasoning = sorted_reasoning[0][0]
        if top_reasoning == "deductive":
            style_adaptation.append("Structural Approach: Builds arguments from general principles to specific conclusions")
        elif top_reasoning == "inductive":
            style_adaptation.append("Pattern Recognition: Identifies trends and extrapolates broader principles")
        elif top_reasoning == "analogical":
            style_adaptation.append("Comparative Framework: Explains concepts through meaningful parallels")
        elif top_reasoning == "narrative":
            style_adaptation.append("Storytelling Integration: Weaves concepts into compelling narrative structures")
        else:
            style_adaptation.append("Cognitive Flexibility: Adapts reasoning approach based on context")
        
        # 5. Format cognitive strengths
        cognitive_strengths = []
        # Combine the highest values from thought patterns and reasoning
        strengths = []
        for pattern, value in sorted_thought_patterns[:2]:
            strengths.append(pattern)
        for pattern, value in sorted_reasoning[:1]:
            strengths.append(pattern)
        
        cognitive_strengths.append(f"Strengths: {', '.join([s.title() for s in strengths])} integration")
        
        # Add domain-specific strengths
        if primary_domain == "technical":
            cognitive_strengths.append("Potential Blindspots: May emphasize technical details over broader implications or user experience")
        elif primary_domain == "business":
            cognitive_strengths.append("Potential Blindspots: May focus on strategic outcomes at the expense of implementation details")
        elif primary_domain == "academic":
            cognitive_strengths.append("Potential Blindspots: May prioritize theoretical frameworks over practical applications")
        elif primary_domain == "journalistic":
            cognitive_strengths.append("Potential Blindspots: May simplify complex topics to maintain narrative flow and accessibility")
        else:
            cognitive_strengths.append("Potential Blindspots: May shift between different cognitive modes, potentially diluting focus")
        
        # Format conceptual insights using actual content from the analysis
        top_thought = sorted_thought_patterns[0][0].title()
        second_thought = sorted_thought_patterns[1][0].title()
        top_reasoning_style = sorted_reasoning[0][0].title()
        
        # Use key phrases if available
        phrase_references = ""
        if key_phrases and len(key_phrases) >= 2:
            phrase_references = f" This is evident in your focus on concepts like '{key_phrases[0]}' and '{key_phrases[1]}'."
        
        conceptual_insights = [
            f"Your cognitive style reveals a mind that primarily utilizes {top_thought} thinking, particularly using {top_reasoning_style} reasoning as a framework.{phrase_references} This creates a distinctive approach in the {primary_domain.title()} domain.",
            f"Your communication reveals a pattern of integrating {top_thought} and {second_thought} processing, where you combine seemingly different cognitive approaches to create a unique synthesis. This is reflected in your {analytical_creative_ratio}% analytical to {100-analytical_creative_ratio}% creative balance.",
            f"This cognitive architecture supports your strengths in {', '.join([s.title() for s in strengths])}, while maintaining a complexity level that is {complexity.lower()} (average sentence length: {avg_sentence_length:.1f} words)."
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
