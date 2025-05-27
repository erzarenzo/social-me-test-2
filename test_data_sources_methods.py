#!/usr/bin/env python3
"""
Test script for verifying different input methods for data sources
in the SocialMe workflow system.

This script tests:
1. The existing URL-based data sources endpoint
2. Shows how document uploads and pasted text could be implemented
3. Provides extension suggestions to make the system more consistent

Note: Currently, only URL-based extraction is officially supported for data sources.
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

# Sample article for text/document input
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
"""

# Count words in the test article
word_count = len(TEST_ARTICLE.split())
logger.info(f"Test article contains {word_count} words")

# Test URLs
TEST_URLS = [
    "https://en.wikipedia.org/wiki/Artificial_intelligence_in_healthcare",
    "https://www.ibm.com/topics/artificial-intelligence-healthcare"
]

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

def test_url_data_sources(workflow_id):
    """Test the existing URL-based data sources endpoint"""
    logger.info("\n=== Testing URL-based Data Sources ===")
    
    try:
        payload = {
            "urls": TEST_URLS
        }
        
        logger.info(f"Sending {len(payload['urls'])} URLs for processing")
        
        response = requests.post(
            f"{BASE_URL}/{workflow_id}/data/sources",
            json=payload
        )
        
        logger.info(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Success: {result.get('status')} - {result.get('message')}")
            
            # Show word count totals
            data_sources = result.get("data_sources", [])
            total_words = sum(source.get("word_count", 0) for source in data_sources)
            logger.info(f"Extracted {total_words} words from {len(data_sources)} sources")
            
            # Show individual sources
            for i, source in enumerate(data_sources):
                logger.info(f"Source {i+1}: {source.get('url')} - {source.get('word_count')} words")
            
            return True
        else:
            logger.error(f"Error: {response.text}")
            return False
    except Exception as e:
        logger.error(f"Exception during URL data sources test: {str(e)}")
        return False

def test_text_data_sources_simulation(workflow_id):
    """
    Simulate direct text input for data sources
    Note: This endpoint does not officially exist yet
    """
    logger.info("\n=== Simulating Direct Text Input for Data Sources ===")
    
    try:
        # This would be the ideal payload format for text input
        payload = {
            "source_type": "text",
            "content": TEST_ARTICLE,
            "title": "AI in Healthcare - Direct Text Input",
            "settings": {
                "processing_options": {
                    "extract_key_points": True,
                    "prioritize_examples": True
                }
            }
        }
        
        logger.info(f"Would send {len(payload['content'])} characters of text content")
        logger.info("Note: This endpoint doesn't exist yet - showing expected payload format")
        
        # Instead of actually sending the request, we'll just log what the endpoint should do
        logger.info("Expected behavior: System would extract key points and process the text as a data source")
        logger.info("Expected response: Data source added with word count and metadata")
        
        return None  # No actual test result
    except Exception as e:
        logger.error(f"Exception during text data sources simulation: {str(e)}")
        return None

def test_document_data_sources_simulation(workflow_id):
    """
    Simulate document upload for data sources
    Note: This endpoint does not officially exist yet
    """
    logger.info("\n=== Simulating Document Upload for Data Sources ===")
    
    try:
        # This would be the ideal payload format for document upload
        document_content = base64.b64encode(TEST_ARTICLE.encode('utf-8')).decode('utf-8')
        
        # In a real implementation, you'd send a multipart/form-data request with a file
        logger.info(f"Would upload document with {word_count} words")
        logger.info("Note: This endpoint doesn't exist yet - showing expected implementation")
        
        # Instead of actually sending the request, we'll describe how it should be implemented
        logger.info("Expected endpoint: POST /api/workflow/{workflow_id}/data/document")
        logger.info("Expected implementation: File upload endpoint that extracts text from documents")
        logger.info("Expected response: Data source added with extracted text, word count and metadata")
        
        return None  # No actual test result
    except Exception as e:
        logger.error(f"Exception during document data sources simulation: {str(e)}")
        return None

def suggest_implementation_changes():
    """Suggest how to implement additional data source input methods"""
    logger.info("\n=== Implementation Suggestions ===")
    
    # Model suggestions
    logger.info("1. Extended DataSourcesRequest Model:")
    logger.info("""
    class ExtendedDataSourcesRequest(BaseModel):
        urls: Optional[List[str]] = None
        text_content: Optional[str] = None
        document_content: Optional[str] = None
        source_type: str = "url"  # Options: "url", "text", "document"
        title: Optional[str] = None
        settings: Optional[Dict[str, Any]] = None
        
        @validator('source_type')
        def validate_source_type(cls, v):
            if v not in ["url", "text", "document"]:
                raise ValueError(f"Invalid source_type: {v}. Must be 'url', 'text', or 'document'")
            return v
            
        @root_validator
        def check_source_provided(cls, values):
            source_type = values.get('source_type')
            if source_type == 'url' and not values.get('urls'):
                raise ValueError('URLs must be provided when source_type is url')
            elif source_type == 'text' and not values.get('text_content'):
                raise ValueError('Text content must be provided when source_type is text')
            elif source_type == 'document' and not values.get('document_content'):
                raise ValueError('Document content must be provided when source_type is document')
            return values
    """)
    
    # Endpoint suggestions
    logger.info("\n2. New Endpoints:")
    logger.info("""
    @workflow_router.post("/{workflow_id}/data/text")
    async def submit_text_data_source(workflow_id: str, request: TextDataSourceRequest):
        \"\"\"
        Submit text content as a data source for the workflow.
        \"\"\"
        # Implementation would extract content from the text
        # and add it to the workflow data sources
        
    @workflow_router.post("/{workflow_id}/data/document")
    async def submit_document_data_source(workflow_id: str, file: UploadFile = File(...)):
        \"\"\"
        Submit a document file as a data source for the workflow.
        \"\"\"
        # Implementation would extract text from the document
        # and add it to the workflow data sources
    """)
    
    # Integration suggestions
    logger.info("\n3. Integration with QuantumUniversalCrawler:")
    logger.info("""
    # Extend the crawler to process text content
    def extract_from_text(self, text_content, title="Direct Text Input"):
        # Process the text similar to how URL content is processed
        # Extract key points, entities, etc.
        # Return in the same format as extract_from_urls
        
    # Update the submit_data_sources function to handle different source types
    async def submit_data_sources(workflow_id: str, request: ExtendedDataSourcesRequest):
        if request.source_type == "url":
            # Current URL processing logic
        elif request.source_type == "text":
            # New text processing logic
        elif request.source_type == "document":
            # New document processing logic
    """)

def main():
    """Run the tests"""
    logger.info("Starting SocialMe Data Sources Methods Test")
    
    # Test existing URL-based data sources
    workflow_id = create_workflow()
    if workflow_id:
        url_test_result = test_url_data_sources(workflow_id)
        
        # Simulate text input for data sources
        test_text_data_sources_simulation(workflow_id)
        
        # Simulate document upload for data sources
        test_document_data_sources_simulation(workflow_id)
        
        # Suggest implementation changes
        suggest_implementation_changes()
        
        # Print summary
        logger.info("\n=== Test Results Summary ===")
        if url_test_result is not None:
            status = "✅ PASSED" if url_test_result else "❌ FAILED"
            logger.info(f"URL-based Data Sources: {status}")
        logger.info(f"Text-based Data Sources: ⚠️ NOT IMPLEMENTED")
        logger.info(f"Document-based Data Sources: ⚠️ NOT IMPLEMENTED")
        logger.info("\nSee implementation suggestions above for extending the system.")

if __name__ == "__main__":
    main()
