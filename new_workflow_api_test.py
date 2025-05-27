import os
import sys
import uuid
import logging
import requests
import json
import threading
import time
import pytest
from dotenv import load_dotenv

# Import port finding and server running functions
from complete_workflow_test import find_free_port, run_flask_server, app as workflow_app

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("new_workflow_api_test.log")
    ]
)
logger = logging.getLogger("new_workflow_api_test")

class NewWorkflowAPITest:
    def __init__(self, base_url=None):
        """
        Initialize the New Workflow API Test
        
        Args:
            base_url (str): Base URL for the Flask application
        """
        # Find a free port if no base_url is provided
        if base_url is None:
            port = find_free_port()
            base_url = f"http://localhost:{port}"
            
            # Start Flask server in a separate thread
            self.server_thread = threading.Thread(
                target=run_flask_server, 
                args=(workflow_app, port), 
                daemon=True
            )
            self.server_thread.start()
            
            # Wait for server to start
            time.sleep(2)
        
        self.base_url = base_url
        self.session = requests.Session()
        self.workflow_id = None
        
        # Load environment variables
        load_dotenv()
        
        # Configure logging
        self.logger = logger
        self.logger.info(f"New Workflow API Test initialized with base URL: {self.base_url}")

    def start_workflow(self):
        """
        Start a new workflow session
        """
        try:
            response = self.session.post(f"{self.base_url}/api/workflow/start")
            response.raise_for_status()
            result = response.json()
            
            self.workflow_id = result['workflow_id']
            self.logger.info(f"Workflow started: {self.workflow_id}")
            
            # Log initial configuration
            self.logger.info(f"Workflow Configuration: {json.dumps(result.get('initial_config', {}), indent=2)}")
            
            return result
        except requests.RequestException as e:
            self.logger.error(f"Failed to start workflow: {e}")
            raise

    def submit_topic(self):
        """
        Submit primary and secondary topics
        """
        try:
            data = {
                "primary_topic": "AI in Healthcare Innovations",
                "secondary_topics": [
                    "Machine Learning in Medical Diagnostics", 
                    "Ethical Considerations of AI in Medicine"
                ]
            }
            
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/topic", 
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            self.logger.info("Topic submission successful")
            self.logger.info(f"Submitted Topics: {json.dumps(data, indent=2)}")
            
            return result
        except requests.RequestException as e:
            self.logger.error(f"Failed to submit topic: {e}")
            raise

    def upload_avatar(self):
        """
        Upload or select user avatar
        """
        try:
            data = {
                "avatar_url": "https://example.com/medical-ai-researcher.jpg"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/avatar", 
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            self.logger.info("Avatar upload successful")
            self.logger.info(f"Avatar Details: {json.dumps(data, indent=2)}")
            
            return result
        except requests.RequestException as e:
            self.logger.error(f"Failed to upload avatar: {e}")
            raise

    def add_data_sources(self):
        """
        Add key data sources for content generation
        """
        try:
            data = {
                "urls": [
                    "https://www.nature.com/articles/s41746-023-00890-4",
                    "https://www.scientificamerican.com/article/how-ai-is-transforming-medical-diagnostics/",
                    "https://www.who.int/publications/i/item/AI-in-healthcare-global-report"
                ]
            }
            
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/key-data-sources", 
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            self.logger.info("Data sources added successfully")
            self.logger.info(f"Data Sources: {json.dumps(data, indent=2)}")
            
            return result
        except requests.RequestException as e:
            self.logger.error(f"Failed to add data sources: {e}")
            raise

    def perform_tone_analysis(self):
        """
        Add sources for tone and style analysis
        """
        try:
            data = {
                "urls": [
                    "https://www.wired.com/story/ai-transforming-medical-research/",
                    "https://www.technologyreview.com/2023/ai-in-medicine-breakthrough/"
                ]
            }
            
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/tone-analysis", 
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            self.logger.info("Tone analysis sources added successfully")
            self.logger.info(f"Tone Analysis Sources: {json.dumps(data, indent=2)}")
            
            return result
        except requests.RequestException as e:
            self.logger.error(f"Failed to perform tone analysis: {e}")
            raise

    def generate_article(self):
        """
        Generate article based on collected data and tone
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/generate-article"
            )
            response.raise_for_status()
            result = response.json()
            
            self.logger.info("Article generation successful")
            self.logger.info(f"Article Word Count: {result.get('word_count', 0)}")
            
            return result
        except requests.RequestException as e:
            self.logger.error(f"Failed to generate article: {e}")
            raise

    def validate_article(self):
        """
        Validate and potentially edit the generated article
        """
        try:
            data = {
                "edits": {
                    "tone": "More academic and research-oriented",
                    "length": "Expand to 1000 words"
                }
            }
            
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/validate-article",
                json=data
            )
            response.raise_for_status()
            result = response.json()
            
            self.logger.info("Article validation successful")
            self.logger.info(f"Validation Edits: {json.dumps(data, indent=2)}")
            
            return result
        except requests.RequestException as e:
            self.logger.error(f"Failed to validate article: {e}")
            raise

def test_complete_workflow():
    """
    Test the complete content generation workflow
    """
    # Initialize the test
    test = NewWorkflowAPITest()
    
    # Run through the workflow steps
    try:
        # Start workflow
        start_result = test.start_workflow()
        assert 'workflow_id' in start_result, "Workflow start failed"
        
        # Submit topic
        topic_result = test.submit_topic()
        assert topic_result['status'] == 'success', "Topic submission failed"
        
        # Upload avatar
        avatar_result = test.upload_avatar()
        assert avatar_result['status'] == 'success', "Avatar upload failed"
        
        # Add data sources
        sources_result = test.add_data_sources()
        assert sources_result['status'] == 'success', "Data sources addition failed"
        
        # Perform tone analysis
        tone_result = test.perform_tone_analysis()
        assert tone_result['status'] == 'success', "Tone analysis failed"
        
        # Generate article
        article_result = test.generate_article()
        assert 'article' in article_result, "Article generation failed"
        
        # Validate article
        validate_result = test.validate_article()
        assert validate_result['status'] == 'success', "Article validation failed"
        
        print("✅ Complete Workflow Test Successful!")
    except Exception as e:
        pytest.fail(f"Workflow test failed: {e}")
