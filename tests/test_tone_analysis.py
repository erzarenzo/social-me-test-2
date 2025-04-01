import logging
import sys
sys.path.append('/root/socialme/social-me-test-2')

from app.tone_adaptation.tone_adapter import AdvancedToneAdapter, extract_tone_metrics
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fetch_web_content(url):
    """
    Fetch content from a web URL
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
        # Check response status
        logger.info(f"Response Status for {url}: {response.status_code}")
        
        # Parse the content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract text content
        text_content = soup.get_text()
        logger.info(f"Text Length: {len(text_content)}")
        
        return text_content
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

def test_tone_analysis():
    """
    Comprehensive test for tone analysis
    """
    # Initialize tone adapter
    tone_adapter = AdvancedToneAdapter()
    
    # Test scenarios
    test_cases = [
        # Basic string input
        [{'sample_content': 'This is a test sentence about technology and innovation.'}],
        
        # Web content input
        [{'sample_content': fetch_web_content('https://forbes.com')}],
        
        # Multiple sources
        [
            {'sample_content': 'First test sentence about business.'},
            {'sample_content': 'Second test sentence about entrepreneurship.'}
        ],
        
        # Edge cases
        [{'sample_content': ''}],
        [{'sample_content': None}]
    ]
    
    # Run tests
    for i, case in enumerate(test_cases, 1):
        logger.info(f"\n--- Test Case {i} ---")
        logger.info(f"Input: {case}")
        
        try:
            # Use both methods to test
            # 1. Direct method call
            direct_result = tone_adapter.process_tone_sources(case)
            logger.info("Direct Method Result:")
            logger.info(direct_result)
            
            # 2. Convenience function
            function_result = extract_tone_metrics(case)
            logger.info("Convenience Function Result:")
            logger.info(function_result)
            
            # Validate results
            assert 'formality' in direct_result
            assert 'complexity' in direct_result
            assert 'sentiment' in direct_result
            
            # Check value ranges
            assert 0 <= direct_result['formality'] <= 1
            assert 0 <= direct_result['complexity'] <= 1
            assert -1 <= direct_result['sentiment'] <= 1
        
        except Exception as e:
            logger.error(f"Error in test case {i}: {e}")
            raise

if __name__ == '__main__':
    test_tone_analysis()
