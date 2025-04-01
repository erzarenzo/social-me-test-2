"""
Comprehensive Test Suite for Advanced Style Fingerprinter

This test suite validates the functionality, robustness, and performance
of the AdvancedStyleFingerprinter class.
"""

import unittest
import logging
import numpy as np
from app.tone_adaptation.advanced_style_fingerprinter import AdvancedStyleFingerprinter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAdvancedStyleFingerprinter(unittest.TestCase):
    def setUp(self):
        """Initialize the AdvancedStyleFingerprinter before each test"""
        self.fingerprinter = AdvancedStyleFingerprinter()
    
    def test_basic_text_analysis(self):
        """Test basic text analysis functionality"""
        text = "Hello world! This is a test sentence to analyze style."
        result = self.fingerprinter.analyze_style(text)
        
        # Validate core metrics exist
        core_metrics = [
            'avg_sentence_length', 'sentence_length_std', 
            'vocabulary_diversity', 'unique_word_ratio', 
            'style_embedding', 'total_sentences', 'total_words'
        ]
        
        for metric in core_metrics:
            self.assertIn(metric, result, f"Missing metric: {metric}")
    
    def test_empty_text_handling(self):
        """Verify handling of empty or invalid text inputs"""
        # Test empty string
        empty_result = self.fingerprinter.analyze_style("")
        self.assertEqual(empty_result['total_sentences'], 0)
        self.assertEqual(empty_result['total_words'], 0)
        
        # Test None input
        none_result = self.fingerprinter.analyze_style(None)
        self.assertEqual(none_result['total_sentences'], 0)
        self.assertEqual(none_result['total_words'], 0)
    
    def test_long_text_handling(self):
        """Test processing of very long text"""
        long_text = "This is a very long text " * 1000  # Repeat text to make it long
        result = self.fingerprinter.analyze_style(long_text)
        
        # Verify basic metrics are computed
        self.assertGreater(result['avg_sentence_length'], 0)
        self.assertGreater(result['total_sentences'], 0)
        self.assertGreater(result['total_words'], 0)
    
    def test_style_embedding_generation(self):
        """Validate style embedding generation"""
        texts = [
            "This is a formal academic writing sample.",
            "Hey, what's up? This is super casual!",
            "The research indicates significant findings in the field."
        ]
        
        embeddings = [self.fingerprinter.analyze_style(text)['style_embedding'] for text in texts]
        
        # Check embedding dimensions
        for embedding in embeddings:
            self.assertEqual(len(embedding), 20)  # Matches custom embedding size
            self.assertTrue(all(isinstance(x, float) for x in embedding))
        
        # Check embeddings are somewhat different for different texts
        # Allow for some similarity due to small sample size
        similarity_threshold = 0.9  # Adjust as needed
        
        def cosine_similarity(a, b):
            """Compute cosine similarity between two vectors"""
            a, b = np.array(a), np.array(b)
            norm_a = np.linalg.norm(a)
            norm_b = np.linalg.norm(b)
            
            # Prevent division by zero
            if norm_a == 0 or norm_b == 0:
                return 0.0
            
            return np.dot(a, b) / (norm_a * norm_b)
        
        # Check pairwise similarities
        similarities = [
            cosine_similarity(embeddings[0], embeddings[1]),
            cosine_similarity(embeddings[1], embeddings[2]),
            cosine_similarity(embeddings[0], embeddings[2])
        ]
        
        # Print similarities for debugging
        print(f"Embedding similarities: {similarities}")
        
        # Ensure at least one pair has low similarity
        self.assertTrue(any(0 <= sim < similarity_threshold for sim in similarities), 
                        f"Embeddings too similar. Similarities: {similarities}")
    
    def test_linguistic_metrics(self):
        """Test advanced linguistic metrics"""
        text = """
        The quantum computing paradigm represents a significant breakthrough 
        in computational complexity theory. Researchers have demonstrated 
        remarkable progress in developing quantum algorithms that can solve 
        complex problems exponentially faster than classical computing methods.
        """
        
        result = self.fingerprinter.analyze_style(text)
        
        # Validate linguistic complexity metrics
        self.assertGreater(result['avg_sentence_length'], 10)
        self.assertGreater(result['vocabulary_diversity'], 0)
        self.assertGreater(result['unique_word_ratio'], 0)
        self.assertGreater(result['avg_word_length'], 3)
    
    def test_error_resilience(self):
        """Verify error handling and resilience"""
        # Test extremely long input
        very_long_text = "x" * 100000
        result = self.fingerprinter.analyze_style(very_long_text)
        
        # Ensure a result is always returned
        self.assertIsNotNone(result)
        self.assertIn('style_embedding', result)
    
    def test_performance(self):
        """Basic performance test"""
        import time
        
        text = "This is a sample text to test performance of style analysis."
        
        start_time = time.time()
        result = self.fingerprinter.analyze_style(text)
        end_time = time.time()
        
        # Ensure analysis takes less than 1 second
        self.assertLess(end_time - start_time, 1.0)

def run_tests():
    """Run the test suite and log results"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestAdvancedStyleFingerprinter)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Log test results
    logger.info(f"Tests run: {result.testsRun}")
    logger.info(f"Errors: {len(result.errors)}")
    logger.info(f"Failures: {len(result.failures)}")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
