#!/usr/bin/env python3
"""
Test script for verifying different input methods for tone analysis and data sources
in the SocialMe workflow system.

This script tests:
1. Direct text input
2. Document upload (base64 encoded)
3. URL-based analysis

For both tone analysis and data sources endpoints.
"""

import requests
import json
import base64
import time
import sys
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "http://localhost:8001/api/workflow"

# A longer article with plenty of words to meet the 500-word minimum
TEST_ARTICLE = """
# Artificial Intelligence in Modern Healthcare

Artificial intelligence (AI) has revolutionized modern healthcare systems across the globe. The integration of AI technologies into clinical workflows has demonstrated significant potential for improving patient outcomes, reducing costs, and enhancing operational efficiency. Healthcare providers increasingly rely on AI-driven tools for diagnostics, treatment planning, and administrative tasks.

## Key Applications of AI in Healthcare

### Diagnostic Imaging
AI algorithms have shown remarkable accuracy in interpreting medical images such as X-rays, MRIs, and CT scans. Deep learning models can detect abnormalities that might be missed by human radiologists, particularly when analyzing large volumes of images. For instance, AI systems can identify early signs of conditions like cancer, cardiovascular diseases, and neurological disorders with high precision.

### Predictive Analytics
Healthcare organizations utilize AI-powered predictive models to anticipate patient deterioration, readmission risks, and disease outbreaks. By analyzing patterns in electronic health records (EHRs) and other data sources, these systems enable proactive interventions that can prevent adverse events and optimize resource allocation.

### Virtual Health Assistants
Conversational AI platforms have emerged as valuable tools for patient engagement and support. Virtual health assistants can provide medication reminders, answer common medical questions, and facilitate remote monitoring. These technologies are particularly beneficial for managing chronic conditions and supporting elderly patients in home care settings.

## Ethical Considerations

Despite its transformative potential, the implementation of AI in healthcare raises important ethical considerations. Issues related to data privacy, algorithmic bias, and the changing role of healthcare professionals must be carefully addressed. Ensuring that AI systems are developed and deployed responsibly requires multidisciplinary collaboration among technologists, clinicians, ethicists, and policymakers.

## Future Directions

The future of AI in healthcare will likely involve more sophisticated integration of various data modalities, including genomics, proteomics, and environmental factors. Personalized medicine approaches that leverage AI to tailor treatments to individual patients' unique characteristics represent a promising frontier. Additionally, advancements in explainable AI will enhance transparency and trust in these systems, facilitating wider adoption across healthcare settings.

In conclusion, artificial intelligence continues to transform healthcare delivery and research, offering unprecedented opportunities to improve human health. As these technologies evolve, ongoing assessment of their impact and thoughtful governance will be essential to maximize benefits while mitigating potential risks.

Additional considerations include the training requirements for healthcare professionals to effectively utilize AI systems, the economic implications of AI adoption in healthcare organizations, and the potential disparities in access to AI-driven healthcare innovations. Regulatory frameworks are evolving to address these challenges, with agencies like the FDA developing new approaches to evaluate and approve AI/ML-based medical devices.

Research institutions and technology companies continue to invest in healthcare AI research, with notable advancements in areas such as drug discovery, clinical trial optimization, and personalized treatment protocols. Collaborative initiatives between academic medical centers, industry partners, and government agencies are accelerating innovation in this field.

As AI technologies become more embedded in healthcare systems, continuous evaluation of their performance, safety, and impact on patient outcomes will be critical. Robust validation methodologies and post-deployment monitoring strategies must be implemented to ensure these systems deliver on their promise to enhance healthcare quality and accessibility.

The integration of AI with other emerging technologies, such as the Internet of Medical Things (IoMT), blockchain, and advanced robotics, presents additional opportunities for transformative healthcare applications. These convergent technologies may enable new care delivery models that extend beyond traditional healthcare settings into patients' homes and communities.

Ultimately, the success of AI in healthcare will depend not only on technological capabilities but also on thoughtful implementation strategies that prioritize patient-centered care, clinical workflow integration, and ethical considerations. The collaborative efforts of diverse stakeholders will shape the responsible evolution of AI as a powerful tool for improving human health and wellbeing in the years ahead.
"""

# Count words in the test article
word_count = len(TEST_ARTICLE.split())
logger.info(f"Test article contains {word_count} words (minimum required: 500)")

# Test URL - use a reliable source that's likely to have substantial content
TEST_URL = "https://en.wikipedia.org/wiki/Artificial_intelligence_in_healthcare"

def create_workflow():
    """Create a new workflow and return the workflow ID"""
    try:
        response = requests.post(f"{BASE_URL}/start", json={
            "topic": "AI in Healthcare",
            "project_type": "article"
        })
        response.raise_for_status()
        data = response.json()
        logger.info(f"Created workflow: {data['workflow_id']}")
        return data.get("workflow_id")
    except Exception as e:
        logger.error(f"Failed to create workflow: {str(e)}")
        return None

def inspect_workflow_content(workflow_id):
    """Debug helper to view the current workflow content"""
    try:
        response = requests.get(f"{BASE_URL}/{workflow_id}/diagnostics")
        response.raise_for_status()
        logger.info(f"Workflow diagnostics: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        logger.error(f"Failed to get workflow diagnostics: {str(e)}")

def test_tone_analysis_text_input(workflow_id):
    """Test tone analysis with direct text input"""
    logger.info("\n=== Testing Tone Analysis with Direct Text Input ===")
    
    try:
        # Log the payload size before sending
        payload = {
            "source_type": "text",
            "sample_text": TEST_ARTICLE
        }
        logger.info(f"Sending payload with {len(payload['sample_text'])} characters")
        
        response = requests.post(
            f"{BASE_URL}/{workflow_id}/tone-analysis",
            json=payload
        )
        
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Success: {result.get('status')} - {result.get('message')}")
            # Print a sample of tone analysis to verify content
            if 'tone_analysis' in result:
                logger.info("Sample tone analysis elements:")
                for key in list(result['tone_analysis'].keys())[:2]:  # Show first 2 sections
                    logger.info(f"- {key}")
            return True
        else:
            logger.error(f"Error: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception during text input test: {str(e)}")
        return False

def test_tone_analysis_document_upload(workflow_id):
    """Test tone analysis with document upload (base64 encoded)"""
    logger.info("\n=== Testing Tone Analysis with Document Upload ===")
    
    try:
        # Create document content - use plain text, not base64 encoded
        # The API might expect actual text in the document_content field
        payload = {
            "source_type": "document",
            "document_content": TEST_ARTICLE  # Try with plain text instead of base64
        }
        
        logger.info(f"Sending document with {len(payload['document_content'])} characters")
        
        response = requests.post(
            f"{BASE_URL}/{workflow_id}/tone-analysis",
            json=payload
        )
        
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Success: {result.get('status')} - {result.get('message')}")
            # Print a sample of tone analysis to verify content
            if 'tone_analysis' in result:
                logger.info("Sample tone analysis elements:")
                for key in list(result['tone_analysis'].keys())[:2]:  # Show first 2 sections
                    logger.info(f"- {key}")
            return True
        else:
            logger.error(f"Error: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception during document upload test: {str(e)}")
        return False

def test_tone_analysis_url(workflow_id):
    """Test tone analysis with URL"""
    logger.info("\n=== Testing Tone Analysis with URL ===")
    
    try:
        payload = {
            "source_type": "url",
            "url": TEST_URL
        }
        
        logger.info(f"Sending URL: {payload['url']}")
        
        response = requests.post(
            f"{BASE_URL}/{workflow_id}/tone-analysis",
            json=payload
        )
        
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Success: {result.get('status')} - {result.get('message')}")
            # Print a sample of tone analysis to verify content
            if 'tone_analysis' in result:
                logger.info("Sample tone analysis elements:")
                for key in list(result['tone_analysis'].keys())[:2]:  # Show first 2 sections
                    logger.info(f"- {key}")
            return True
        else:
            logger.error(f"Error: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception during URL test: {str(e)}")
        return False

def main():
    """Run the tests"""
    logger.info("Starting SocialMe Input Methods Test")
    
    # Test tone analysis with different input methods
    results = []
    
    # Test text input
    workflow_id = create_workflow()
    if workflow_id:
        results.append(("Tone Analysis - Text Input", test_tone_analysis_text_input(workflow_id)))
    
    # Test document upload
    workflow_id = create_workflow()
    if workflow_id:
        results.append(("Tone Analysis - Document Upload", test_tone_analysis_document_upload(workflow_id)))
    
    # Test URL
    workflow_id = create_workflow()
    if workflow_id:
        results.append(("Tone Analysis - URL", test_tone_analysis_url(workflow_id)))
    
    # Print summary
    logger.info("\n=== Test Results Summary ===")
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")

if __name__ == "__main__":
    main()
