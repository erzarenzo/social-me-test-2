#!/usr/bin/env python3
"""
OpenAI Tone Analyzer Integration Verification Script

This script provides a comprehensive test of the OpenAI tone analyzer integration,
including the style samples and feedback endpoints. It verifies:
1. Creating a workflow
2. Submitting a text sample for tone analysis
3. Generating style samples
4. Providing feedback on samples
5. Regenerating samples based on feedback
6. Generating an article with the preferred style

Note: This script requires an active FastAPI server running on port 8001
"""

import requests
import json
import time
import logging
import sys
import os
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("openai_tone_integration_verification")

# Configuration
API_BASE_URL = "http://localhost:8001/api"

# Sample text for analysis
SAMPLE_TEXT = """
The integration of quantum computing into practical applications represents a significant 
paradigm shift in computational methodologies. Contemporary research indicates that quantum 
systems exhibit considerable potential in addressing complex optimization problems that 
remain intractable for classical computing architectures. The implementation of quantum 
algorithms in fields such as cryptography, material science, and pharmaceutical development 
demonstrates remarkable efficacy, particularly when applied to problems characterized by 
exponential complexity.
"""

class OpenAIToneIntegrationVerifier:
    """Verification class for OpenAI tone analyzer integration"""
    
    def __init__(self):
        self.session = requests.Session()
        self.workflow_id = None
        self.style_samples = None
        self.selected_sample_id = None
    
    def run_verification(self) -> bool:
        """Run the complete verification process"""
        try:
            logger.info("===== Starting OpenAI Tone Analyzer Integration Verification =====")
            
            # Step 1: Create a workflow
            self.create_workflow()
            if not self.workflow_id:
                logger.error("Failed to create workflow")
                return False
            
            # Step 2: Submit tone analysis
            success = self.submit_tone_analysis()
            if not success:
                logger.error("Failed to submit tone analysis")
                return False
            
            # Step 3: Generate style samples
            self.generate_style_samples()
            if not self.style_samples:
                logger.error("Failed to generate style samples")
                return False
            
            # Step 4: Provide feedback on samples
            success = self.provide_sample_feedback(upvote=True)
            if not success:
                logger.error("Failed to provide sample feedback")
                return False
            
            # Step 5: Regenerate samples based on feedback
            success = self.regenerate_samples()
            if not success:
                logger.error("Failed to regenerate samples")
                return False
            
            # Step 6: Generate article with preferred style
            success = self.generate_article()
            if not success:
                logger.error("Failed to generate article")
                return False
            
            logger.info("✅ Verification COMPLETED SUCCESSFULLY")
            return True
            
        except Exception as e:
            logger.error(f"Verification failed: {str(e)}")
            return False
    
    def create_workflow(self) -> bool:
        """Create a new workflow"""
        try:
            logger.info("Creating new workflow...")
            response = self.session.post(
                f"{API_BASE_URL}/workflow/start",
                json={
                    "topic": "OpenAI Tone Integration Test",
                    "title": "Testing OpenAI Tone Analysis Integration",
                    "settings": {
                        "target_word_count": 3000
                    }
                }
            )
            
            response.raise_for_status()
            result = response.json()
            self.workflow_id = result.get("workflow_id")
            logger.info(f"✓ Workflow created: {self.workflow_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating workflow: {str(e)}")
            return False
    
    def submit_tone_analysis(self) -> bool:
        """Submit text for tone analysis"""
        try:
            logger.info("Submitting tone analysis...")
            response = self.session.post(
                f"{API_BASE_URL}/workflow/{self.workflow_id}/tone-analysis",
                json={
                    "source_type": "text",
                    "sample_text": SAMPLE_TEXT
                }
            )
            
            response.raise_for_status()
            result = response.json()
            logger.info(f"✓ Tone analysis submitted successfully: {result.get('message', 'No message')}")
            return True
            
        except Exception as e:
            logger.error(f"Error submitting tone analysis: {str(e)}")
            return False
    
    def generate_style_samples(self) -> bool:
        """Generate writing style samples"""
        try:
            logger.info("Generating style samples...")
            response = self.session.post(
                f"{API_BASE_URL}/workflow/{self.workflow_id}/style-samples",
                json={
                    "sample_text": SAMPLE_TEXT,
                    "num_samples": 2,
                    "target_length": 200
                }
            )
            
            response.raise_for_status()
            self.style_samples = response.json()
            
            # Log the style analysis results
            if "style_analysis" in self.style_samples:
                analysis = self.style_samples["style_analysis"]
                logger.info("✓ Style analysis received:")
                
                if "key_characteristics" in analysis:
                    logger.info("Key characteristics:")
                    for i, char in enumerate(analysis["key_characteristics"], 1):
                        logger.info(f"  {i}. {char}")
                
                if "distinctive_patterns" in analysis:
                    logger.info("Distinctive patterns:")
                    for i, pattern in enumerate(analysis["distinctive_patterns"], 1):
                        logger.info(f"  {i}. {pattern}")
            
            # Log the sample count and preview
            if "samples" in self.style_samples:
                samples = self.style_samples["samples"]
                logger.info(f"✓ Received {len(samples)} style samples:")
                
                for i, sample in enumerate(samples, 1):
                    preview = sample.get("sample_text", "")[:100] + "..."
                    logger.info(f"  Sample {i} (ID: {sample.get('id')}): {preview}")
                    
                    # Store the first sample ID for feedback
                    if i == 1 and "id" in sample:
                        self.selected_sample_id = sample["id"]
            
            return True
            
        except Exception as e:
            logger.error(f"Error generating style samples: {str(e)}")
            return False
    
    def provide_sample_feedback(self, upvote: bool = True) -> bool:
        """Provide feedback on a style sample"""
        if not self.selected_sample_id:
            logger.error("No sample ID selected for feedback")
            return False
        
        try:
            rating = "upvote" if upvote else "downvote"
            logger.info(f"Providing {rating} feedback for sample {self.selected_sample_id}...")
            
            response = self.session.post(
                f"{API_BASE_URL}/workflow/{self.workflow_id}/style-sample-feedback",
                json={
                    "sample_id": self.selected_sample_id,
                    "rating": rating,
                    "comments": "Verification test feedback",
                    "regenerate": False
                }
            )
            
            response.raise_for_status()
            result = response.json()
            logger.info(f"✓ Feedback submitted: {result.get('message', 'No message')}")
            return True
            
        except Exception as e:
            logger.error(f"Error providing sample feedback: {str(e)}")
            return False
    
    def regenerate_samples(self) -> bool:
        """Regenerate style samples based on feedback"""
        try:
            logger.info("Requesting sample regeneration...")
            response = self.session.post(
                f"{API_BASE_URL}/workflow/{self.workflow_id}/style-sample-feedback",
                json={
                    "sample_id": self.selected_sample_id,
                    "rating": "upvote",
                    "regenerate": True,
                    "num_samples": 2
                }
            )
            
            response.raise_for_status()
            result = response.json()
            
            if "samples" in result and len(result["samples"]) > 0:
                samples = result["samples"]
                logger.info(f"✓ Regenerated {len(samples)} style samples:")
                
                for i, sample in enumerate(samples, 1):
                    preview = sample.get("sample_text", "")[:100] + "..."
                    logger.info(f"  Sample {i} (ID: {sample.get('id')}): {preview}")
                    
                    # Update the selected sample ID to the first regenerated sample
                    if i == 1 and "id" in sample:
                        self.selected_sample_id = sample["id"]
                        logger.info(f"  Selected new sample ID: {self.selected_sample_id}")
            else:
                logger.warning("No samples were regenerated")
            
            return True
            
        except Exception as e:
            logger.error(f"Error regenerating samples: {str(e)}")
            return False
    
    def generate_article(self) -> bool:
        """Generate an article using the preferred style"""
        try:
            logger.info("Generating article with preferred style...")
            
            # Submit one more feedback to ensure the style is selected
            if self.selected_sample_id:
                self.provide_sample_feedback(upvote=True)
            
            response = self.session.post(
                f"{API_BASE_URL}/workflow/{self.workflow_id}/article/generate",
                json={
                    "settings": {
                        "target_word_count": 3000,
                        "format": "markdown"
                    }
                }
            )
            
            if response.status_code == 202:
                logger.info("✓ Article generation started (asynchronous)")
                
                # Poll for completion
                max_attempts = 10
                attempt = 0
                while attempt < max_attempts:
                    attempt += 1
                    logger.info(f"Polling for article completion (attempt {attempt}/{max_attempts})...")
                    
                    try:
                        status_response = self.session.get(
                            f"{API_BASE_URL}/workflow/{self.workflow_id}/article"
                        )
                        
                        if status_response.status_code == 200:
                            article_data = status_response.json()
                            logger.info(f"✓ Article generated successfully")
                            logger.info(f"  Title: {article_data.get('title', 'No title')}")
                            
                            word_count = article_data.get("word_count", 0)
                            logger.info(f"  Word count: {word_count}")
                            
                            content_preview = article_data.get("content", "")[:200] + "..."
                            logger.info(f"  Content preview: {content_preview}")
                            
                            return True
                    except Exception:
                        pass
                    
                    time.sleep(30)  # Wait 30 seconds between attempts
                
                logger.warning("Article generation did not complete within the timeout period")
                return False
            
            elif response.status_code == 200:
                # Synchronous completion
                article_data = response.json()
                logger.info(f"✓ Article generated successfully (synchronous)")
                logger.info(f"  Title: {article_data.get('title', 'No title')}")
                
                word_count = article_data.get("word_count", 0)
                logger.info(f"  Word count: {word_count}")
                
                content_preview = article_data.get("content", "")[:200] + "..."
                logger.info(f"  Content preview: {content_preview}")
                
                return True
            
            else:
                error_data = response.json()
                logger.error(f"Article generation failed: {error_data.get('detail', 'Unknown error')}")
                return False
            
        except Exception as e:
            logger.error(f"Error generating article: {str(e)}")
            return False

def main():
    """Run the verification script"""
    # Check if the API server is reachable
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code != 200:
            logger.error(f"API server not available at {API_BASE_URL}. Status: {response.status_code}")
            return
    except Exception as e:
        logger.error(f"Error connecting to API server: {e}")
        logger.error(f"Make sure the FastAPI server is running on port 8001")
        return
    
    verifier = OpenAIToneIntegrationVerifier()
    success = verifier.run_verification()
    
    if success:
        logger.info("\n✅✅✅ OpenAI Tone Analyzer Integration VERIFIED SUCCESSFULLY ✅✅✅")
        sys.exit(0)
    else:
        logger.error("\n❌❌❌ OpenAI Tone Analyzer Integration VERIFICATION FAILED ❌❌❌")
        sys.exit(1)

if __name__ == "__main__":
    main()
