"""
Advanced Style Fingerprinter with Custom Embedding Techniques

Provides a sophisticated approach to style analysis using
advanced NLP techniques and custom embedding generation.
"""

import re
import logging
import numpy as np
import spacy
from typing import Dict, List, Any, Optional

# Lightweight machine learning and NLP imports
import sklearn.feature_extraction.text
import sklearn.preprocessing

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("advanced_style_fingerprinter")

class AdvancedStyleFingerprinter:
    """
    Enhanced style fingerprinting using advanced NLP techniques
    and custom embedding generation
    """
    
    def __init__(self, max_text_length: int = 1000):
        """
        Initialize the advanced style fingerprinter
        
        Args:
            max_text_length (int): Maximum text length to process to prevent memory issues
        """
        # Load spaCy model for advanced linguistic analysis
        self.nlp = None
        try:
            # Use a smaller spaCy model to reduce memory footprint
            self.nlp = spacy.load('en_core_web_sm')
        except OSError:
            logger.warning("spaCy model not found. Some advanced features will be limited.")
        
        # Configuration
        self.max_text_length = max_text_length
        
        # Initialize style markers and vectorizers
        self._initialize_style_markers()
        self._initialize_vectorizers()
    
    def _initialize_style_markers(self):
        """Initialize various linguistic and stylistic markers"""
        # Formality markers
        self.formality_markers = {
            'formal': [
                'therefore', 'consequently', 'furthermore', 'moreover', 'thus',
                'accordingly', 'hence', 'subsequently', 'nevertheless', 'whereas'
            ],
            'informal': [
                'anyway', 'plus', 'so', 'also', 'like', 'actually', 'basically',
                'really', 'honestly', 'literally', 'totally', 'kinda', 'sorta'
            ]
        }
    
    def _initialize_vectorizers(self):
        """
        Initialize text vectorization techniques for custom embedding
        """
        # TF-IDF Vectorizer for text representation
        self.tfidf_vectorizer = sklearn.feature_extraction.text.TfidfVectorizer(
            stop_words='english',
            max_features=100,  # Limit features to prevent memory issues
            ngram_range=(1, 2)  # Capture unigrams and bigrams
        )
        
        # Scaler for normalizing features
        self.feature_scaler = sklearn.preprocessing.StandardScaler()
    
    def _preprocess_text(self, text: str) -> str:
        """
        Preprocess text to reduce memory usage and improve analysis
        
        Args:
            text (str): Input text to preprocess
        
        Returns:
            str: Preprocessed text
        """
        try:
            # Truncate text to prevent memory issues
            text = text[:self.max_text_length]
            
            # Basic text cleaning
            text = text.strip()
            text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
            
            return text
        except Exception as e:
            logger.error(f"Text preprocessing failed: {e}")
            return ""
    
    def analyze_style(self, text: str) -> Dict[str, Any]:
        """
        Comprehensive style analysis with advanced linguistic techniques
        
        Args:
            text (str): Text to analyze
        
        Returns:
            Dict containing advanced style fingerprint
        """
        try:
            # Validate input
            if not text or not isinstance(text, str):
                logger.warning("Invalid input text. Returning default style fingerprint.")
                return self._get_default_style_fingerprint()
            
            # Preprocess text
            text = self._preprocess_text(text)
            
            # Validate processed text
            if not text:
                logger.warning("Text preprocessing resulted in empty string.")
                return self._get_default_style_fingerprint()
            
            # Linguistic analysis with spaCy
            doc = self.nlp(text) if self.nlp else None
            
            # Sentence structure
            sentences = list(doc.sents) if doc else re.split(r'[.!?]+', text)
            sentences = [str(sent) for sent in sentences if str(sent).strip()]
            
            # Prevent empty sentences
            if not sentences:
                logger.warning("No sentences found in text. Returning default style fingerprint.")
                return self._get_default_style_fingerprint()
            
            # Advanced sentence metrics
            sentence_metrics = self._analyze_sentence_structure(sentences)
            
            # Vocabulary and lexical complexity
            vocab_metrics = self._analyze_vocabulary(doc, text)
            
            # Syntactic complexity
            syntactic_metrics = self._analyze_syntax(doc) if doc else {}
            
            # Custom embedding generation
            style_embedding = self._generate_custom_embedding(text)
            
            # Combine all metrics
            style_fingerprint = {
                # Sentence structure
                **sentence_metrics,
                
                # Vocabulary metrics
                **vocab_metrics,
                
                # Syntactic complexity
                **syntactic_metrics,
                
                # Style embedding
                'style_embedding': style_embedding.tolist(),
                
                # Metadata
                'total_sentences': len(sentences),
                'total_words': len(text.split())
            }
            
            return style_fingerprint
        
        except Exception as e:
            logger.error(f"Comprehensive style analysis failed: {e}")
            return self._get_default_style_fingerprint()
    
    def _get_default_style_fingerprint(self) -> Dict[str, Any]:
        """
        Generate a default style fingerprint for edge cases
        
        Returns:
            Dict with default style metrics
        """
        return {
            'avg_sentence_length': 0,
            'sentence_length_std': 0,
            'max_sentence_length': 0,
            'min_sentence_length': 0,
            'vocabulary_diversity': 0,
            'unique_word_ratio': 0,
            'avg_word_length': 0,
            'named_entity_density': 0,
            'named_entity_types': 0,
            'avg_dependency_depth': 0,
            'max_dependency_depth': 0,
            'clause_complexity': 0,
            'style_embedding': [0.0] * 20,
            'total_sentences': 0,
            'total_words': 0
        }
    
    def _analyze_sentence_structure(self, sentences: List[str]) -> Dict[str, float]:
        """
        Analyze advanced sentence structure metrics
        
        Args:
            sentences (List[str]): List of sentences
        
        Returns:
            Dict of sentence structure metrics
        """
        try:
            # Sentence length analysis
            sent_lengths = [len(re.findall(r'\b\w+\b', sent)) for sent in sentences]
            
            # Prevent division by zero and handle empty list
            if not sent_lengths:
                return {
                    'avg_sentence_length': 0,
                    'sentence_length_std': 0,
                    'max_sentence_length': 0,
                    'min_sentence_length': 0
                }
            
            return {
                'avg_sentence_length': float(np.mean(sent_lengths)),
                'sentence_length_std': float(np.std(sent_lengths)),
                'max_sentence_length': float(max(sent_lengths)),
                'min_sentence_length': float(min(sent_lengths))
            }
        except Exception as e:
            logger.error(f"Sentence structure analysis failed: {e}")
            return {
                'avg_sentence_length': 0,
                'sentence_length_std': 0,
                'max_sentence_length': 0,
                'min_sentence_length': 0
            }
    
    def _analyze_vocabulary(self, doc, text: str) -> Dict[str, float]:
        """
        Advanced vocabulary and lexical complexity analysis
        
        Args:
            doc (spaCy Doc): Parsed document
            text (str): Original text
        
        Returns:
            Dict of vocabulary metrics
        """
        try:
            # If no spaCy doc, fallback to basic analysis
            if not doc:
                words = re.findall(r'\b\w+\b', text.lower())
                unique_words = set(words)
                return {
                    'vocabulary_diversity': len(unique_words) / max(1, len(words)),
                    'unique_word_ratio': len(unique_words) / max(1, len(words)),
                    'avg_word_length': np.mean([len(word) for word in words]) if words else 0,
                    'named_entity_density': 0,
                    'named_entity_types': 0
                }
            
            # Advanced vocabulary metrics
            words = [token.text.lower() for token in doc if not token.is_punct and not token.is_stop]
            unique_words = set(words)
            
            # Named entity analysis
            named_entities = [ent.text for ent in doc.ents]
            
            return {
                'vocabulary_diversity': len(unique_words) / max(1, len(words)),
                'unique_word_ratio': len(unique_words) / max(1, len(words)),
                'avg_word_length': np.mean([len(word) for word in words]) if words else 0,
                'named_entity_density': len(named_entities) / max(1, len(words)),
                'named_entity_types': len(set(ent.label_ for ent in doc.ents)) if doc.ents else 0
            }
        except Exception as e:
            logger.error(f"Vocabulary analysis failed: {e}")
            return {
                'vocabulary_diversity': 0,
                'unique_word_ratio': 0,
                'avg_word_length': 0,
                'named_entity_density': 0,
                'named_entity_types': 0
            }
    
    def _analyze_syntax(self, doc) -> Dict[str, float]:
        """
        Analyze syntactic complexity
        
        Args:
            doc (spaCy Doc): Parsed document
        
        Returns:
            Dict of syntactic complexity metrics
        """
        try:
            # Dependency tree depth
            def tree_depth(token):
                depth = 0
                while token.dep_ != 'ROOT' and token.head is not None:
                    token = token.head
                    depth += 1
                return depth
            
            # Safely compute depths
            depths = []
            for token in doc:
                try:
                    if token.dep_ != 'ROOT':
                        depth = tree_depth(token)
                        depths.append(depth)
                except Exception:
                    continue
            
            # Prevent division by zero and handle empty list
            if not depths:
                return {
                    'avg_dependency_depth': 0,
                    'max_dependency_depth': 0,
                    'clause_complexity': 0
                }
            
            # Clause complexity
            try:
                clauses = list(sent.root.subtree for sent in doc.sents)
                clause_lengths = [len(list(clause)) for clause in clauses]
            except Exception:
                clause_lengths = [1]  # Default to 1 if computation fails
            
            return {
                'avg_dependency_depth': float(np.mean(depths)),
                'max_dependency_depth': float(max(depths)),
                'clause_complexity': float(np.mean(clause_lengths)) if clause_lengths else 0
            }
        except Exception as e:
            logger.error(f"Syntax analysis failed: {e}")
            return {
                'avg_dependency_depth': 0,
                'max_dependency_depth': 0,
                'clause_complexity': 0
            }
    
    def _generate_custom_embedding(self, text: str) -> np.ndarray:
        """
        Generate a custom embedding using TF-IDF and feature engineering
        
        Args:
            text (str): Input text to embed
        
        Returns:
            np.ndarray: Custom style embedding vector
        """
        try:
            # Basic text features for embedding
            words = re.findall(r'\b\w+\b', text.lower())
            sentences = re.split(r'[.!?]+', text)
            
            # Compute advanced features
            features = [
                # 1. Average word length
                np.mean([len(word) for word in words]) if words else 0,
                
                # 2. Unique word ratio
                len(set(words)) / max(1, len(words)),
                
                # 3. Sentence complexity (average words per sentence)
                len(words) / max(1, len(sentences)),
                
                # 4. Formality score (ratio of formal words)
                sum(1 for word in words if word in self.formality_markers['formal']) / max(1, len(words)),
                
                # 5. Informal word ratio
                sum(1 for word in words if word in self.formality_markers['informal']) / max(1, len(words)),
                
                # 6. Punctuation complexity
                len(re.findall(r'[,;:]', text)) / max(1, len(words)),
                
                # 7. Verb diversity
                len(set(word for word in words if len(word) > 3)) / max(1, len(words)),
                
                # 8. Noun ratio
                len(set(word for word in words if len(word) > 4)) / max(1, len(words)),
                
                # 9. Adverb/adjective complexity
                len(set(word for word in words if word.endswith(('ly', 'ful', 'ous')))) / max(1, len(words)),
                
                # 10. Text length normalization
                min(1.0, len(text) / 1000),
                
                # 11. Sentence length variation
                np.std([len(re.findall(r'\b\w+\b', sent)) for sent in sentences]) if sentences else 0,
                
                # 12. Vocabulary richness (Type-Token Ratio)
                len(set(words)) / max(1, len(words) ** 0.5),
                
                # 13. Average sentence complexity
                np.mean([len(re.findall(r'\b\w+\b', sent)) for sent in sentences]) if sentences else 0,
                
                # 14. Lexical density
                len(set(word for word in words if len(word) > 3)) / max(1, len(words)),
                
                # 15. Readability proxy (inverse of average word length)
                1 / (np.mean([len(word) for word in words]) + 1),
                
                # 16. Emotional tone proxy (ratio of positive/negative words)
                sum(1 for word in words if word in ['good', 'great', 'excellent', 'positive']) / max(1, len(words)) -
                sum(1 for word in words if word in ['bad', 'terrible', 'worst', 'negative']) / max(1, len(words)),
                
                # 17. Technical vocabulary ratio
                sum(1 for word in words if word in ['algorithm', 'computational', 'quantum', 'technology', 'innovation']) / max(1, len(words)),
                
                # 18. Passive voice proxy
                sum(1 for word in words if word in ['was', 'were', 'been']) / max(1, len(words)),
                
                # 19. Discourse marker complexity
                sum(1 for word in words if word in ['however', 'therefore', 'moreover', 'consequently']) / max(1, len(words)),
                
                # 20. Narrative complexity
                len(sentences) / max(1, len(words) ** 0.5)
            ]
            
            # Normalize features
            features = np.array(features, dtype=np.float32)
            features = (features - features.mean()) / (features.std() + 1e-9)
            
            return features
        except Exception as e:
            logger.error(f"Custom embedding generation failed: {e}")
            return np.zeros(20, dtype=np.float32)
