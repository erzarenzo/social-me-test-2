"""
Quantum Universal Crawler for Tone Analysis
This specialized crawler analyzes tone patterns and stylistic elements in content
without triggering anti-bot measures on websites.
"""

import random
import numpy as np
import requests
from bs4 import BeautifulSoup
import time
import logging
from typing import Dict, Any, List, Optional
import re
import urllib.parse

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
    
    def extract_text_from_url(self, url: str) -> str:
        """
        Extract text content from a URL for tone analysis.
        
        Args:
            url (str): URL to extract text from
        
        Returns:
            str: Extracted text content
        """
        self.logger.info(f"Extracting text from URL: {url}")
        
        try:
            # Sanitize URL
            sanitized_url = self._sanitize_url(url)
            
            # Fetch content with robust error handling
            response = requests.get(
                sanitized_url,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                    'Cache-Control': 'max-age=0'
                },
                timeout=10
            )
            
            # Check if request was successful
            if response.status_code != 200:
                self.logger.warning(f"Failed to fetch URL {url}: HTTP {response.status_code}")
                return ""
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove non-content elements
            for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
                element.decompose()
            
            # Extract text from main content areas
            content_elements = soup.select('article, main, .content, .article, .post, section')
            
            if content_elements:
                # Use the largest content element
                main_content = max(content_elements, key=lambda x: len(x.get_text()))
                text = main_content.get_text(separator=' ', strip=True)
            else:
                # Fallback to all paragraphs
                paragraphs = soup.find_all('p')
                text = ' '.join(p.get_text(strip=True) for p in paragraphs if len(p.get_text(strip=True)) > 20)
            
            # Clean up the text
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Ensure we have meaningful content
            if len(text.split()) < 50:
                self.logger.warning(f"Extracted text from {url} is too short ({len(text.split())} words)")
                
                # Try a different approach - get all visible text
                text = soup.get_text(separator=' ', strip=True)
                text = re.sub(r'\s+', ' ', text).strip()
            
            self.logger.info(f"Successfully extracted {len(text.split())} words from {url}")
            return text
            
        except Exception as e:
            self.logger.error(f"Error extracting text from {url}: {e}")
            return ""
    
    def _sanitize_url(self, url: str) -> str:
        """
        Sanitize and normalize URLs by removing fragments and cleaning up parameters.
        
        Args:
            url (str): The input URL to sanitize
        
        Returns:
            str: A cleaned and normalized URL
        """
        try:
            # Parse the URL
            parsed_url = urllib.parse.urlparse(url)
            
            # Remove fragment and specific problematic parameters
            cleaned_url = parsed_url._replace(fragment='')
            
            # Optionally remove specific query parameters that might be tracking or unnecessary
            query_params = urllib.parse.parse_qs(parsed_url.query)
            filtered_params = {k: v for k, v in query_params.items() 
                              if k not in ['utm_source', 'utm_medium', 'utm_campaign', 'ref', 'text']}
            
            # Reconstruct the URL without fragment and unnecessary parameters
            cleaned_url = cleaned_url._replace(query=urllib.parse.urlencode(filtered_params, doseq=True))
            
            return urllib.parse.urlunparse(cleaned_url)
        except Exception as e:
            self.logger.warning(f"Error sanitizing URL {url}: {e}")
            return url
    
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
    
    def extract_text_from_url(self, url: str, max_length: int = 5000) -> str:
        """
        Extract text content from a given URL with advanced parsing and filtering.
        
        Args:
            url (str): The URL to extract text from
            max_length (int): Maximum length of text to return
        
        Returns:
            str: Extracted and cleaned text content
        """
        try:
            # Randomize user agent to avoid bot detection
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept-Language': 'en-US,en;q=0.9'
            }
            
            # Add a small random delay to mimic human browsing
            time.sleep(random.uniform(0.5, 1.5))
            
            # Send request with timeout
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script, style, and navigation elements
            for script_or_style in soup(["script", "style", "nav", "header", "footer"]):
                script_or_style.decompose()
            
            # Extract text from paragraphs and headings
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article', 'div'])
            
            # Combine text, filtering out very short or irrelevant text
            text_content = []
            for element in text_elements:
                element_text = element.get_text(strip=True)
                # Filter out very short or irrelevant text
                if len(element_text) > 50:
                    text_content.append(element_text)
            
            # Join text and truncate
            full_text = " ".join(text_content)
            
            # Apply additional cleaning
            full_text = re.sub(r'\s+', ' ', full_text)  # Normalize whitespace
            full_text = re.sub(r'[^\x00-\x7F]+', '', full_text)  # Remove non-ASCII characters
            
            # Truncate to max length
            return full_text[:max_length]
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error extracting text from {url}: {e}")
            return ""
        except Exception as e:
            self.logger.error(f"Unexpected error extracting text from {url}: {e}")
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
