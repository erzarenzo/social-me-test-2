"""
Enhanced Comprehensive Workflow Test for SocialMe Application:
Demonstrates the full content generation workflow using the new API-driven approach
"""

import os
import json
import logging
import datetime
import random
import requests
import uuid
import sys
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("enhanced_workflow_test_2.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("enhanced_workflow_test_2")

# Optional dependencies with graceful fallback
try:
    from termcolor import colored
except ImportError:
    def colored(text, color=None, on_color=None, attrs=None):
        return text

# Add requirements to requirements.txt
def add_requirements():
    requirements = [
        'requests',
        'python-dotenv',
        'termcolor'
    ]
    
    with open('requirements.txt', 'a') as f:
        for req in requirements:
            f.write(f"{req}\n")

# Attempt to add requirements
try:
    add_requirements()
except Exception as e:
    logger.warning(f"Could not update requirements: {e}")

class EnhancedWorkflowAPITest:
    def __init__(self, base_url="http://localhost:8004"):
        """
        Initialize the Enhanced Workflow API Test
        
        Args:
            base_url (str): Base URL for the workflow API
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.workflow_id = None
        
        logger.info(colored(f"Initializing Workflow Test with base URL: {self.base_url}", "green"))
    
    def start_workflow(self):
        """
        Start a new workflow session
        
        Returns:
            dict: Workflow initialization response
        """
        try:
            # Full URL debug print
            full_url = f"{self.base_url}/api/workflow/start"
            logger.info(colored(f"Attempting to start workflow at FULL URL: {full_url}", "blue"))
            
            response = self.session.post(full_url)
            
            # Add debug print for response
            logger.info(colored(f"Response status code: {response.status_code}", "yellow"))
            logger.info(f"Response headers: {response.headers}")
            logger.info(f"Response content: {response.text}")
            
            response.raise_for_status()
            workflow_data = response.json()
            
            # Explicitly extract workflow_id
            self.workflow_id = workflow_data.get('workflow_id')
            
            logger.info(colored(f"Workflow Started: {self.workflow_id}", "green"))
            logger.info("Workflow Configuration:")
            logger.info(json.dumps(workflow_data.get('initial_config', {}), indent=2))
            
            return workflow_data
        except requests.RequestException as e:
            logger.error(colored(f"Failed to start workflow: {e}", "red"))
            raise
    
    def submit_topic(self, primary_topic, secondary_topics=None):
        """
        Submit topics for the workflow
        
        Args:
            primary_topic (str): Primary topic for content generation
            secondary_topics (list, optional): List of secondary topics
        
        Returns:
            dict: Topic submission response
        """
        if not self.workflow_id:
            raise ValueError("Workflow not started. Call start_workflow() first.")
        
        # Default secondary topics if not provided
        if secondary_topics is None:
            secondary_topics = [
                "Emerging Trends in Technology",
                "Ethical Considerations of Innovation"
            ]
        
        topic_data = {
            "primary_topic": primary_topic,
            "secondary_topics": secondary_topics
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/topic", 
                json=topic_data
            )
            response.raise_for_status()
            topic_response = response.json()
            
            logger.info(colored("Topic Submission Successful", "green"))
            logger.info("Submitted Topics:")
            logger.info(json.dumps(topic_data, indent=2))
            
            return topic_response
        except requests.RequestException as e:
            logger.error(colored(f"Failed to submit topics: {e}", "red"))
            raise
    
    def upload_avatar(self, avatar_url=None):
        """
        Upload or select a user avatar
        
        Args:
            avatar_url (str, optional): URL of the avatar image
        
        Returns:
            dict: Avatar upload response
        """
        if not self.workflow_id:
            raise ValueError("Workflow not started. Call start_workflow() first.")
        
        # Default avatar if not provided
        if avatar_url is None:
            avatar_url = "https://example.com/tech-innovator-avatar.jpg"
        
        avatar_data = {
            "avatar_url": avatar_url
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/avatar", 
                json=avatar_data
            )
            response.raise_for_status()
            avatar_response = response.json()
            
            logger.info(colored("Avatar Upload Successful", "green"))
            logger.info("Avatar Details:")
            logger.info(json.dumps(avatar_data, indent=2))
            
            return avatar_response
        except requests.RequestException as e:
            logger.error(colored(f"Failed to upload avatar: {e}", "red"))
            raise
    
    def add_data_sources(self, urls=None):
        """
        Add data sources for content generation
        
        Args:
            urls (list, optional): List of URLs to use as data sources
        
        Returns:
            dict: Data sources addition response
        """
        if not self.workflow_id:
            raise ValueError("Workflow not started. Call start_workflow() first.")
        
        # Default URLs if not provided
        if urls is None:
            urls = [
                "https://www.wired.com/story/ai-innovation-trends",
                "https://www.techcrunch.com/emerging-tech",
                "https://www.scientificamerican.com/tech-insights"
            ]
        
        data_sources = {
            "urls": urls
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/key-data-sources", 
                json=data_sources
            )
            response.raise_for_status()
            sources_response = response.json()
            
            logger.info(colored("Data Sources Added Successfully", "green"))
            logger.info("Data Sources:")
            logger.info(json.dumps(data_sources, indent=2))
            
            return sources_response
        except requests.RequestException as e:
            logger.error(colored(f"Failed to add data sources: {e}", "red"))
            raise
    
    def add_tone_sources(self, urls=None):
        """
        Add tone sources for style analysis
        
        Args:
            urls (list, optional): List of URLs to use for tone analysis
        
        Returns:
            dict: Tone sources addition response
        """
        if not self.workflow_id:
            raise ValueError("Workflow not started. Call start_workflow() first.")
        
        # Default URLs if not provided
        if urls is None:
            urls = [
                "https://www.newyorker.com/tech-writing-style",
                "https://www.economist.com/technology-analysis"
            ]
        
        tone_sources = {
            "urls": urls
        }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/tone-analysis", 
                json=tone_sources
            )
            response.raise_for_status()
            tone_response = response.json()
            
            logger.info(colored("Tone Analysis Sources Added Successfully", "green"))
            logger.info("Tone Analysis Sources:")
            logger.info(json.dumps(tone_sources, indent=2))
            
            # Verbose Tone Analysis Output
            tone_analysis = self._perform_detailed_tone_analysis(urls)
            logger.info("\n🔍 Detailed Tone Analysis Results:")
            logger.info(json.dumps(tone_analysis, indent=2))
            
            return tone_response
        except requests.RequestException as e:
            logger.error(colored(f"Failed to add tone sources: {e}", "red"))
            raise
    
    def _perform_detailed_tone_analysis(self, urls):
        """
        Perform a detailed tone analysis on the provided sources
        
        Args:
            urls (list): List of URLs to analyze
        
        Returns:
            dict: Detailed tone analysis results
        """
        # Simulated detailed tone analysis
        return {
            "overall_tone": {
                "formality": 0.75,  # High formality
                "complexity": 0.65,  # Moderately complex
                "sentiment": 0.3    # Slightly positive
            },
            "source_specific_analysis": [
                {
                    "url": urls[0],
                    "tone_characteristics": {
                        "academic_level": "Graduate",
                        "narrative_style": "Analytical",
                        "emotional_tone": "Objective"
                    }
                },
                {
                    "url": urls[1],
                    "tone_characteristics": {
                        "academic_level": "Professional",
                        "narrative_style": "Investigative",
                        "emotional_tone": "Neutral"
                    }
                }
            ],
            "recommended_writing_style": {
                "target_formality": "Professional",
                "suggested_vocabulary": "Technical, precise",
                "sentence_structure": "Complex, with clear logical progression"
            }
        }
    
    def generate_article(self):
        """
        Generate an article based on the workflow configuration
        
        Returns:
            dict: Article generation response
        """
        if not self.workflow_id:
            raise ValueError("Workflow not started. Call start_workflow() first.")
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/generate-article"
            )
            response.raise_for_status()
            article_response = response.json()
            
            logger.info(colored("Article Generation Successful", "green"))
            logger.info("Article Details:")
            logger.info(json.dumps(article_response, indent=2))
            
            return article_response
        except requests.RequestException as e:
            logger.error(colored(f"Failed to generate article: {e}", "red"))
            raise
    
    def validate_article(self, edits=None):
        """
        Validate and potentially edit the generated article
        
        Args:
            edits (dict, optional): Suggested edits for the article
        
        Returns:
            dict: Article validation response
        """
        if not self.workflow_id:
            raise ValueError("Workflow not started. Call start_workflow() first.")
        
        # Default edits if not provided
        if edits is None:
            edits = {
                "tone": "More academic and research-oriented",
                "length": "Expand to 4000 words",
                "technical_depth": "Increase technical terminology"
            }
        
        try:
            response = self.session.post(
                f"{self.base_url}/api/workflow/{self.workflow_id}/validate-article", 
                json={"edits": edits}
            )
            response.raise_for_status()
            validation_response = response.json()
            
            logger.info(colored("Article Validation Successful", "green"))
            logger.info("Validation Edits:")
            logger.info(json.dumps(edits, indent=2))
            
            return validation_response
        except requests.RequestException as e:
            logger.error(colored(f"Failed to validate article: {e}", "red"))
            raise
    
    def run_comprehensive_workflow(self):
        """
        Run the entire content generation workflow
        """
        try:
            # Step 1: Start Workflow
            self.start_workflow()
            
            # Step 2: Submit Topics
            self.submit_topic("AI in Technology: Future Trends")
            
            # Step 3: Upload Avatar
            self.upload_avatar()
            
            # Step 4: Add Data Sources
            self.add_data_sources()
            
            # Step 5: Add Tone Sources with Verbose Analysis
            self.add_tone_sources()
            
            # Step 6: Generate Article
            article_response = self.generate_article()
            
            # Step 7: Validate Article
            self.validate_article()
            
            logger.info(colored("✅ Comprehensive Workflow Test Completed Successfully!", "green"))
        
        except Exception as e:
            logger.error(colored(f"Workflow Test Failed: {e}", "red"))
            raise

def main():
    """
    Main function to run the enhanced workflow test
    """
    try:
        workflow_test = EnhancedWorkflowAPITest()
        workflow_test.run_comprehensive_workflow()
    except Exception as e:
        logger.error(colored(f"Workflow Test Execution Error: {e}", "red"))
        sys.exit(1)

if __name__ == "__main__":
    main()
