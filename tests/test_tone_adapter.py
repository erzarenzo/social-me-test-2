import spacy
from app.tone_adaptation.tone_adapter import AdvancedToneAdapter

def test_process_tone_sources():
    # Initialize the tone adapter
    tone_adapter = AdvancedToneAdapter()
    
    # Test scenarios
    test_cases = [
        # Basic string input
        [{'sample_content': 'This is a test sentence.'}],
        
        # Multiple string inputs
        [
            {'sample_content': 'First test sentence.'},
            {'sample_content': 'Second test sentence.'}
        ],
        
        # SpaCy Span input (simulated)
        [{'sample_content': tone_adapter.nlp('SpaCy Span test sentence.')}],
        
        # Mixed input types
        [
            {'sample_content': 'String input'},
            {'sample_content': tone_adapter.nlp('SpaCy Span input')}
        ],
        
        # Edge cases
        [{'sample_content': None}],
        [{'sample_content': ''}],
        []
    ]
    
    # Run tests
    for case in test_cases:
        print(f"\nTesting case: {case}")
        try:
            result = tone_adapter.process_tone_sources(case)
            print("Result:", result)
            
            # Validate result structure
            assert 'formality' in result
            assert 'complexity' in result
            assert 'sentiment' in result
            assert all(0 <= val <= 1 for val in [result['formality'], result['complexity']])
            assert -1 <= result['sentiment'] <= 1
        except Exception as e:
            print(f"Error processing case: {e}")
            raise

# Run the test
if __name__ == '__main__':
    test_process_tone_sources()
