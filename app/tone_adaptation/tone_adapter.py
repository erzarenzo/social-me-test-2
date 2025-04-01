"""
Advanced Tone Adapter for SocialMe

Enhances the existing tone analysis and article generation workflow
with more sophisticated style matching capabilities.
"""

import logging
import re
import spacy  
from typing import Dict, Any, List, Optional

# Robust TextBlob import
try:
    from textblob import TextBlob
except ImportError:
    class TextBlob:
        def __init__(self, text):
            self.text = text
            self.sentiment = type('Sentiment', (), {'polarity': 0.0})()

# Logging setup
logger = logging.getLogger("app.tone_adaptation.tone_adapter")
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all log levels

class AdvancedToneAdapter:
    """
    Advanced Tone Adaptation System for precise style matching and article generation
    """
    def __init__(self):
        """
        Initialize the Advanced Tone Adapter with NLP capabilities
        """
        self.logger = logger
        
        # Load spaCy model
        self.nlp = spacy.load('en_core_web_sm')
        
        # Formal and informal word lists
        self.formal_words = {
            'utilize', 'implement', 'demonstrate', 'consequently', 
            'furthermore', 'moreover', 'therefore', 'however', 
            'nonetheless', 'nevertheless', 'subsequently', 
            'additionally', 'accordingly', 'specifically'
        }
        
        self.informal_words = {
            'gonna', 'wanna', 'kinda', 'sorta', 'awesome', 
            'cool', 'like', 'basically', 'totally', 'hey', 
            'yo', 'stuff', 'thing', 'gotta'
        }

    def _compute_formality(self, doc) -> float:
        """
        Compute formality score based on linguistic features
        """
        # Count formal and informal words
        formal_count = sum(1 for token in doc if token.text.lower() in self.formal_words)
        informal_count = sum(1 for token in doc if token.text.lower() in self.informal_words)
        
        # Compute total unique words
        total_unique_words = len(set(token.text.lower() for token in doc))
        
        # Adjust formality based on word choice and sentence structure
        if total_unique_words == 0:
            return 0.5
        
        # Weighted formality score
        formality_score = (formal_count - informal_count) / total_unique_words
        
        # Normalize to 0-1 range
        return max(0, min(1, 0.5 + formality_score))

    def _compute_complexity(self, doc) -> float:
        """
        Compute text complexity based on multiple linguistic features
        """
        # Sentence length variation
        sentences = list(doc.sents)
        if not sentences:
            return 0.5
        
        # Compute average sentence length
        avg_sentence_length = sum(len(sent) for sent in sentences) / len(sentences)
        
        # Count advanced vocabulary words (more than 6 characters)
        advanced_vocab_count = sum(1 for token in doc if len(token.text) > 6 and token.is_alpha)
        
        # Compute unique words ratio
        unique_words = len(set(token.text.lower() for token in doc))
        total_words = len(doc)
        
        # Complexity score with multiple factors
        complexity_score = (
            (avg_sentence_length / 20) * 0.3 +  # Sentence length factor
            (advanced_vocab_count / total_words) * 0.4 +  # Advanced vocabulary factor
            (unique_words / total_words) * 0.3  # Lexical diversity factor
        )
        
        return max(0, min(1, complexity_score))

    def _compute_sentiment(self, text: str) -> float:
        """
        Compute sentiment with more nuanced approach
        """
        if not text:
            return 0.0
        
        # Use TextBlob for sentiment analysis
        blob = TextBlob(text)
        
        # Sentiment polarity ranges from -1 to 1
        return blob.sentiment.polarity

    def process_tone_sources(self, sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process multiple tone sources and compute style metrics
        """
        # Combine sample contents, handling None and empty inputs
        combined_text = ' '.join([
            str(source.get('sample_content', '')) 
            for source in sources 
            if source and source.get('sample_content')
        ])
        
        # Handle empty input
        if not combined_text:
            return {
                'formality': 0.0, 
                'complexity': 0.5, 
                'sentiment': 0.0
            }
        
        # Process text with spaCy
        doc = self.nlp(combined_text)
        
        # Compute style metrics
        return {
            'formality': self._compute_formality(doc),
            'complexity': self._compute_complexity(doc),
            'sentiment': self._compute_sentiment(combined_text)
        }

def extract_tone_metrics(sources: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Convenience function to extract tone metrics
    """
    tone_adapter = AdvancedToneAdapter()
    return tone_adapter.process_tone_sources(sources)
