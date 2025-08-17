import numpy as np
import random
import re
import logging
import networkx as nx
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import json

class NeuralToneMapper:
    """
    Advanced Neural Tone Mapper with Comprehensive Tone Analysis
    Integrates multi-dimensional style extraction, web crawling, 
    and advanced NLP techniques.
    """
    
    def __init__(self, debug=False):
        """Initialize the advanced neural tone mapper"""
        self.logger = logging.getLogger(__name__)
        self.logger.info("Initializing Advanced NeuralToneMapper")
        
        # Debug mode for verbose logging
        self.debug = debug
        
        # User agent rotation to avoid detection
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0'
        ]
        
        # Comprehensive tone and style categories
        self.thought_patterns = [
            "analytical", "creative", "systematic", "intuitive", 
            "concrete", "abstract", "logical", "emotional"
        ]
        
        self.reasoning_styles = [
            "deductive", "inductive", "abductive", "analogical",
            "causal", "counterfactual", "statistical", "narrative"
        ]
        
        # Enhanced stylistic markers with weighted importance
        self.stylistic_markers = {
            "analytical": {
                "keywords": ["therefore", "analysis", "data", "evidence", "conclude", "study", "research"],
                "weight": 0.9
            },
            "creative": {
                "keywords": ["imagine", "create", "possibility", "innovative", "unique", "vision"],
                "weight": 0.8
            },
            "systematic": {
                "keywords": ["process", "structure", "framework", "step", "method", "organize"],
                "weight": 0.85
            },
            "intuitive": {
                "keywords": ["feel", "sense", "intuition", "impression", "instinct", "gut"],
                "weight": 0.75
            }
        }
        
        # Reasoning style markers with contextual weighting
        self.reasoning_markers = {
            "deductive": {
                "keywords": ["all", "therefore", "must", "necessarily", "certainly"],
                "weight": 0.9
            },
            "inductive": {
                "keywords": ["some", "likely", "probably", "trend", "pattern"],
                "weight": 0.8
            },
            "abductive": {
                "keywords": ["best explanation", "hypothesis", "could be", "possibly"],
                "weight": 0.75
            }
        }
        
        # Domain-specific content markers
        self.domain_markers = {
            "technical": ["code", "algorithm", "function", "implementation"],
            "business": ["market", "strategy", "customer", "product"],
            "academic": ["research", "study", "theory", "hypothesis"],
            "journalistic": ["report", "news", "article", "interview"]
        }
    
    def _get_random_user_agent(self):
        """Return a random user agent to avoid detection"""
        return random.choice(self.user_agents)
    
    def extract_content_from_url(self, url, max_length=5000):
        """
        Advanced web content extraction with multiple fallback mechanisms
        
        Args:
            url (str): URL to extract content from
            max_length (int): Maximum length of extracted content
        
        Returns:
            str: Extracted and cleaned text content
        """
        try:
            # Prepare headers to mimic browser request
            headers = {
                'User-Agent': self._get_random_user_agent(),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Referer': 'https://www.google.com/'
            }
            
            # Add random delay to simulate human browsing
            time.sleep(random.uniform(1.0, 3.0))
            
            # Make request with timeout
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script, style, and navigation elements
            for script in soup(["script", "style", "nav", "header", "footer"]):
                script.decompose()
            
            # Extract text
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean and truncate text
            text = re.sub(r'\s+', ' ', text)
            text = text[:max_length]
            
            return text
        
        except requests.RequestException as e:
            self.logger.error(f"Error extracting content from {url}: {e}")
            return ""
    
    def analyze_tone(self, text_sources):
        """
        Comprehensive tone analysis across multiple sources
        
        Args:
            text_sources (list): List of text sources or URLs to analyze
        
        Returns:
            dict: Comprehensive tone analysis results
        """
        try:
            # Normalize and extract content from sources
            processed_sources = []
            for source in text_sources:
                try:
                    # Check if source is a URL
                    if source.startswith(('http://', 'https://')):
                        content = self.extract_content_from_url(source)
                    else:
                        content = source
                    
                    if content and len(content.strip()) > 0:
                        processed_sources.append(content)
                except Exception as e:
                    self.logger.warning(f"Error processing source {source}: {e}")
                    continue
            
            # Handle case where no content could be processed
            if not processed_sources:
                return {
                    "thought_patterns": {"analytical": 0.5, "creative": 0.5, "systematic": 0.5, "intuitive": 0.5},
                    "reasoning_styles": {"deductive": 0.5, "inductive": 0.5, "abductive": 0.5, "analogical": 0.5},
                    "domain_characteristics": {"technical": 0.5, "business": 0.5, "academic": 0.5, "journalistic": 0.5},
                    "key_phrases": [],
                    "linguistic_complexity": {"avg_sentence_length": 10.0, "word_complexity": 2.0},
                    "overall_tone_score": 0.5
                }
            
            # Combine sources
            combined_text = ' '.join(processed_sources)
            
            # Advanced tone analysis
            tone_profile = {
                "thought_patterns": self._analyze_thought_patterns(combined_text),
                "reasoning_styles": self._analyze_reasoning_styles(combined_text),
                "domain_characteristics": self._identify_domain_markers(combined_text),
                "key_phrases": self._extract_key_phrases(combined_text),
                "linguistic_complexity": self._measure_linguistic_complexity(combined_text)
            }
            
            # Compute overall tone score
            tone_profile['overall_tone_score'] = self._compute_tone_score(tone_profile)
            
            return tone_profile
            
        except Exception as e:
            self.logger.error(f"Error in analyze_tone: {e}")
            # Return default analysis on error
            return {
                "thought_patterns": {"analytical": 0.5, "creative": 0.5, "systematic": 0.5, "intuitive": 0.5},
                "reasoning_styles": {"deductive": 0.5, "inductive": 0.5, "abductive": 0.5, "analogical": 0.5},
                "domain_characteristics": {"technical": 0.5, "business": 0.5, "academic": 0.5, "journalistic": 0.5},
                "key_phrases": [],
                "linguistic_complexity": {"avg_sentence_length": 10.0, "word_complexity": 2.0},
                "overall_tone_score": 0.5
            }
    
    def _analyze_thought_patterns(self, text):
        """
        Analyze thought patterns based on stylistic markers
        
        Args:
            text (str): Text to analyze
        
        Returns:
            dict: Thought pattern scores
        """
        pattern_scores = {}
        for pattern, marker_data in self.stylistic_markers.items():
            # Count keyword occurrences with weighted scoring
            keyword_count = sum(
                text.lower().count(keyword.lower()) * marker_data['weight'] 
                for keyword in marker_data['keywords']
            )
            pattern_scores[pattern] = keyword_count
        
        return pattern_scores
    
    def _analyze_reasoning_styles(self, text):
        """
        Analyze reasoning styles based on marker keywords
        
        Args:
            text (str): Text to analyze
        
        Returns:
            dict: Reasoning style scores
        """
        style_scores = {}
        for style, marker_data in self.reasoning_markers.items():
            # Count keyword occurrences with weighted scoring
            keyword_count = sum(
                text.lower().count(keyword.lower()) * marker_data['weight'] 
                for keyword in marker_data['keywords']
            )
            style_scores[style] = keyword_count
        
        return style_scores
    
    def _identify_domain_markers(self, text):
        """
        Identify domain-specific content characteristics
        
        Args:
            text (str): Text to analyze
        
        Returns:
            dict: Domain marker scores
        """
        domain_scores = {}
        for domain, markers in self.domain_markers.items():
            # Count domain-specific marker occurrences
            domain_count = sum(text.lower().count(marker.lower()) for marker in markers)
            domain_scores[domain] = domain_count
        
        return domain_scores
    
    def _extract_key_phrases(self, text, num_phrases=5):
        """
        Extract key phrases using TF-IDF
        
        Args:
            text (str): Text to extract phrases from
            num_phrases (int): Number of phrases to extract
        
        Returns:
            list: Top key phrases
        """
        try:
            # Use TF-IDF to identify important phrases
            vectorizer = TfidfVectorizer(
                stop_words='english', 
                ngram_range=(1, 2), 
                max_features=num_phrases
            )
            
            # Fit and transform the text
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            
            # Get top phrases based on TF-IDF scores
            sorted_phrases = sorted(
                zip(feature_names, tfidf_matrix.toarray()[0]), 
                key=lambda x: x[1], 
                reverse=True
            )
            
            return [phrase for phrase, score in sorted_phrases[:num_phrases]]
        
        except Exception as e:
            self.logger.error(f"Error extracting key phrases: {e}")
            return []
    
    def _measure_linguistic_complexity(self, text):
        """
        Measure linguistic complexity using various metrics
        
        Args:
            text (str): Text to analyze
        
        Returns:
            dict: Linguistic complexity metrics
        """
        try:
            # Handle empty or very short text
            if not text or len(text.strip()) < 10:
                return {
                    "avg_sentence_length": 10.0,
                    "word_complexity": 2.0
                }
            
            # Sentence length analysis
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]  # Remove empty sentences
            
            if not sentences:
                return {
                    "avg_sentence_length": 10.0,
                    "word_complexity": 2.0
                }
            
            sentence_lengths = [len(sentence.split()) for sentence in sentences if sentence.strip()]
            
            if not sentence_lengths:
                avg_sentence_length = 10.0
            else:
                avg_sentence_length = np.mean(sentence_lengths)
                if np.isnan(avg_sentence_length) or np.isinf(avg_sentence_length):
                    avg_sentence_length = 10.0
            
            # Word complexity (using syllable count as a proxy)
            def count_syllables(word):
                """Simple syllable counting heuristic"""
                if not word or len(word) < 2:
                    return 1
                    
                word = word.lower()
                count = 0
                vowels = "aeiouy"
                if word[0] in vowels:
                    count += 1
                for index in range(1, len(word)):
                    if word[index] in vowels and word[index - 1] not in vowels:
                        count += 1
                if word.endswith("e"):
                    count -= 1
                if count == 0:
                    count += 1
                return count
            
            words = text.split()
            if not words:
                word_complexity = 2.0
            else:
                syllable_counts = [count_syllables(word) for word in words if word.strip()]
                if not syllable_counts:
                    word_complexity = 2.0
                else:
                    word_complexity = np.mean(syllable_counts)
                    if np.isnan(word_complexity) or np.isinf(word_complexity):
                        word_complexity = 2.0
            
            return {
                "avg_sentence_length": float(avg_sentence_length),
                "word_complexity": float(word_complexity)
            }
            
        except Exception as e:
            self.logger.error(f"Error measuring linguistic complexity: {e}")
            return {
                "avg_sentence_length": 10.0,
                "word_complexity": 2.0
            }
    
    def _compute_tone_score(self, tone_profile):
        """
        Compute an overall tone score based on various analysis dimensions
        
        Args:
            tone_profile (dict): Comprehensive tone analysis results
        
        Returns:
            float: Overall tone score
        """
        try:
            # Weight different components of the tone profile
            weights = {
                "thought_patterns": 0.3,
                "reasoning_styles": 0.25,
                "domain_characteristics": 0.2,
                "linguistic_complexity": 0.25
            }
            
            # Normalize and compute weighted score
            def normalize_scores(scores):
                if not scores:
                    return {}
                max_val = max(scores.values()) if scores else 1
                if max_val == 0:
                    return {k: 0.5 for k in scores.keys()}  # Default to 0.5 if all scores are 0
                return {k: v/max_val for k, v in scores.items()}
            
            # Compute weighted score
            total_score = 0
            total_weight = 0
            
            for category, weight in weights.items():
                if category in tone_profile and tone_profile[category]:
                    try:
                        normalized_scores = normalize_scores(tone_profile[category])
                        if normalized_scores:
                            category_score = sum(normalized_scores.values()) / len(normalized_scores)
                            if not np.isnan(category_score) and not np.isinf(category_score):
                                total_score += category_score * weight
                                total_weight += weight
                    except (ZeroDivisionError, ValueError) as e:
                        self.logger.warning(f"Error computing score for {category}: {e}")
                        continue
            
            # Return normalized score or default
            if total_weight > 0:
                final_score = total_score / total_weight
                if np.isnan(final_score) or np.isinf(final_score):
                    return 0.5
                return float(final_score)
            else:
                return 0.5
                
        except Exception as e:
            self.logger.error(f"Error computing tone score: {e}")
            return 0.5

    def generate_style_prompt(self, tone_profile):
        """
        Generate a detailed style prompt based on tone analysis
        
        Args:
            tone_profile (dict): Comprehensive tone analysis results
        
        Returns:
            str: Detailed writing style prompt
        """
        # Identify dominant thought patterns
        dominant_patterns = sorted(
            tone_profile['thought_patterns'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:2]
        
        # Identify reasoning styles
        dominant_styles = sorted(
            tone_profile['reasoning_styles'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:2]
        
        # Construct style prompt
        prompt_parts = [
            "Writing Style Guide:",
            f"Dominant Thought Patterns: {', '.join(p[0] for p in dominant_patterns)}",
            f"Reasoning Approach: {', '.join(s[0] for s in dominant_styles)}",
            "Key Phrases to Incorporate: " + ", ".join(tone_profile.get('key_phrases', [])),
            f"Linguistic Complexity: Avg Sentence Length {tone_profile['linguistic_complexity']['avg_sentence_length']:.1f}, Word Complexity {tone_profile['linguistic_complexity']['word_complexity']:.2f}"
        ]
        
        return "\n".join(prompt_parts)

# Example usage
if __name__ == "__main__":
    # Simple test
    mapper = NeuralToneMapper(debug=True)
    sources = [
        "https://www.example.com/article1",
        "This is a sample text demonstrating analytical thinking and systematic reasoning."
    ]
    tone_analysis = mapper.analyze_tone(sources)
    print(json.dumps(tone_analysis, indent=2))
    print("\nStyle Prompt:")
    print(mapper.generate_style_prompt(tone_analysis))
