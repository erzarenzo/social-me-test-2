import requests
import uuid
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("workflow_api_verification")

class FlaskWorkflowAPIVerifier:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        self.workflow_id = str(uuid.uuid4())
        self.session = requests.Session()

    def verify_workflow(self):
        """
        Comprehensive Flask workflow API verification
        """
        try:
            # 1. Start Workflow
            self.test_start_workflow()
            
            # 2. Submit Topic
            self.test_submit_topic()
            
            # 3. Upload Avatar
            self.test_upload_avatar()
            
            # 4. Add Data Sources
            self.test_add_data_sources()
            
            # 5. Tone Analysis
            self.test_tone_analysis()
            
            # 6. Generate Article
            self.test_generate_article()
            
            # 7. Validate Article
            self.test_validate_article()
            
            logger.info("🟢 ALL WORKFLOW API ENDPOINTS VERIFIED SUCCESSFULLY!")
            return True
        
        except Exception as e:
            logger.error(f"🔴 WORKFLOW API VERIFICATION FAILED: {e}")
            return False

    def test_start_workflow(self):
        response = self.session.post(f"{self.base_url}/api/workflow/start", json={
            "workflow_id": self.workflow_id
        })
        assert response.status_code == 200, "Start workflow failed"
        result = response.json()
        logger.info(f"Workflow started: {result}")

    def test_submit_topic(self):
        response = self.session.post(
            f"{self.base_url}/api/workflow/{self.workflow_id}/topic", 
            json={
                "primary_topic": "AI in Healthcare",
                "secondary_topics": ["Machine Learning", "Medical Diagnostics"]
            }
        )
        assert response.status_code == 200, "Topic submission failed"
        logger.info("Topic submitted successfully")

    def test_upload_avatar(self):
        response = self.session.post(
            f"{self.base_url}/api/workflow/{self.workflow_id}/avatar", 
            json={"avatar_url": "https://example.com/avatar.jpg"}
        )
        assert response.status_code == 200, "Avatar upload failed"
        logger.info("Avatar uploaded successfully")

    def test_add_data_sources(self):
        response = self.session.post(
            f"{self.base_url}/api/workflow/{self.workflow_id}/key-data-sources", 
            json={
                "urls": [
                    "https://www.nature.com/articles/example",
                    "https://www.scientificamerican.com/article/ai-healthcare"
                ]
            }
        )
        assert response.status_code == 200, "Data sources addition failed"
        logger.info("Data sources added successfully")

    def test_tone_analysis(self):
        response = self.session.post(
            f"{self.base_url}/api/workflow/{self.workflow_id}/tone-analysis", 
            json={
                "urls": [
                    "https://www.wired.com/story/ai-medical-breakthroughs",
                    "https://www.scientificamerican.com/article/ai-in-medicine"
                ]
            }
        )
        assert response.status_code == 200, "Tone analysis failed"
        logger.info("Tone analysis completed successfully")

    def test_generate_article(self):
        response = self.session.post(
            f"{self.base_url}/api/workflow/{self.workflow_id}/generate-article"
        )
        assert response.status_code == 200, "Article generation failed"
        result = response.json()
        assert 'article' in result, "No article generated"
        logger.info(f"Article generated (Word count: {len(result['article'].get('text', '').split())})")

    def test_validate_article(self):
        response = self.session.post(
            f"{self.base_url}/api/workflow/{self.workflow_id}/validate-article", 
            json={"edits": {"tone": "More academic"}}
        )
        assert response.status_code == 200, "Article validation failed"
        logger.info("Article validated successfully")

def main():
    verifier = FlaskWorkflowAPIVerifier()
    result = verifier.verify_workflow()
    print("Verification Result:", "PASSED" if result else "FAILED")

if __name__ == "__main__":
    main()
