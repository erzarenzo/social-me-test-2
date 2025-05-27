import logging
import re
import numpy as np
import spacy
from typing import Dict, List, Any, Optional

# Logging setup
logger = logging.getLogger(__name__)

class StyleFingerprinter:
    """
    Extracts style features from text to create a comprehensive style fingerprint
    using advanced NLP techniques
    """
    def __init__(self, model_url: Optional[str] = None):
        """
        Initialize the StyleFingerprinter
        
        Args:
            model_url (Optional[str]): Optional URL for advanced model (deprecated)
        """
        # Remove TensorFlow dependencies
        self.style_markers = {
            'questions': r'\?',
            'exclamations': r'!',
            'quotes': r'"[^"]*"',
            'lists': r'^\s*\d+\.',
            'parentheticals': r'\([^)]*\)',
            'em_dashes': r'—'
        }
        
        # Load spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
        except Exception as e:
            logger.error(f"Failed to load spaCy model: {e}")
            self.nlp = None

    def analyze_style(self, text: str) -> Dict[str, Any]:
        """
        Analyze the style of the given text and generate a comprehensive style fingerprint.
        
        Args:
            text (str): Input text to analyze
        
        Returns:
            Dict[str, Any]: Comprehensive style metrics
        """
        try:
            # Fallback if spaCy is not loaded
            if not self.nlp:
                return self._basic_style_analysis(text)
            
            # Process text with spaCy
            doc = self.nlp(text)
            
            # Sentence length analysis
            sentences = list(doc.sents)
            sentence_lengths = [len(list(sent)) for sent in sentences]
            
            # Vocabulary diversity
            unique_words = len(set(token.text.lower() for token in doc if not token.is_punct and not token.is_stop))
            total_words = len([token for token in doc if not token.is_punct and not token.is_stop])
            
            # Dependency depth analysis
            dependency_depths = [self._compute_dependency_depth(token) for token in doc if token.dep_ != 'ROOT']
            
            # Clause complexity
            clause_complexity = sum(len(list(sent.root.children)) for sent in sentences)
            
            # Construct style fingerprint
            style_fingerprint = {
                'avg_sentence_length': np.mean(sentence_lengths) if sentence_lengths else 0,
                'sentence_length_std': np.std(sentence_lengths) if sentence_lengths else 0,
                'max_sentence_length': max(sentence_lengths) if sentence_lengths else 0,
                'min_sentence_length': min(sentence_lengths) if sentence_lengths else 0,
                'vocabulary_diversity': unique_words / max(1, total_words),
                'unique_word_ratio': unique_words / max(1, total_words),
                'avg_word_length': np.mean([len(token.text) for token in doc if not token.is_punct]),
                'named_entity_density': len(list(doc.ents)) / max(1, len(list(doc))),
                'named_entity_types': len(set(ent.label_ for ent in doc.ents)),
                'avg_dependency_depth': np.mean(dependency_depths) if dependency_depths else 0,
                'max_dependency_depth': max(dependency_depths) if dependency_depths else 0,
                'clause_complexity': clause_complexity,
                'style_embedding': self._generate_custom_embedding(text),
                'total_sentences': len(sentences),
                'total_words': len(list(doc))
            }
            
            return style_fingerprint
        
        except Exception as e:
            logger.error(f"Style analysis failed: {e}")
            return self._basic_style_analysis(text)

    def _basic_style_analysis(self, text: str) -> Dict[str, Any]:
        """
        Perform basic style analysis when advanced methods fail
        
        Args:
            text (str): Input text to analyze
        
        Returns:
            Dict[str, Any]: Basic style metrics
        """
        words = text.split()
        sentences = re.split(r'[.!?]+', text)
        
        return {
            'avg_sentence_length': len(words) / max(1, len(sentences)),
            'sentence_length_std': 0,
            'max_sentence_length': max(len(s.split()) for s in sentences) if sentences else 0,
            'min_sentence_length': min(len(s.split()) for s in sentences) if sentences else 0,
            'vocabulary_diversity': len(set(words)) / max(1, len(words)),
            'unique_word_ratio': len(set(words)) / max(1, len(words)),
            'avg_word_length': np.mean([len(word) for word in words]) if words else 0,
            'named_entity_density': 0,
            'named_entity_types': 0,
            'avg_dependency_depth': 0,
            'max_dependency_depth': 0,
            'clause_complexity': 0,
            'style_embedding': self._generate_custom_embedding(text),
            'total_sentences': len(sentences),
            'total_words': len(words)
        }

    def _compute_dependency_depth(self, token):
        """
        Compute dependency depth for a given token
        
        Args:
            token: spaCy token
        
        Returns:
            int: Dependency depth
        """
        depth = 0
        current_token = token
        while current_token.dep_ != 'ROOT':
            depth += 1
            current_token = current_token.head
        return depth

    def _generate_custom_embedding(self, text: str) -> List[float]:
        """
        Generate a simple custom embedding for the text
        
        Args:
            text (str): Input text
        
        Returns:
            List[float]: Custom style embedding
        """
        words = text.lower().split()
        
        # Basic features
        features = [
            # 1. Average word length
            np.mean([len(word) for word in words]) if words else 0,
            
            # 2. Unique word ratio
            len(set(words)) / max(1, len(words)),
            
            # 3. Sentence complexity (average words per sentence)
            len(words) / max(1, len(re.split(r'[.!?]+', text))),
            
            # 4. Punctuation complexity
            len(re.findall(r'[,;:]', text)) / max(1, len(words)),
            
            # 5. Verb diversity
            len(set(word for word in words if len(word) > 3)) / max(1, len(words)),
            
            # 6. Noun ratio
            len(set(word for word in words if len(word) > 4)) / max(1, len(words)),
            
            # 7. Adverb/adjective complexity
            len(set(word for word in words if word.endswith(('ly', 'ful', 'ous')))) / max(1, len(words)),
            
            # 8. Text length normalization
            min(1.0, len(text) / 1000),
            
            # 9. Vocabulary richness
            len(set(words)) / max(1, len(words) ** 0.5),
            
            # 10. Emotional tone proxy
            sum(1 for word in words if word in ['good', 'great', 'excellent', 'positive']) / max(1, len(words)) -
            sum(1 for word in words if word in ['bad', 'terrible', 'worst', 'negative']) / max(1, len(words))
        ]
        
        # Normalize features
        features = np.array(features, dtype=np.float32)
        features = (features - features.mean()) / (features.std() + 1e-9)
        
        # Pad to 20 dimensions
        padded_features = np.zeros(20, dtype=np.float32)
        padded_features[:len(features)] = features
        
        return padded_features.tolist()

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Alias for analyze_style to maintain backwards compatibility
        
        Args:
            text (str): Input text to analyze
        
        Returns:
            Dict[str, Any]: Style analysis results
        """
        return self.analyze_style(text)
