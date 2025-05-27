#!/usr/bin/env python3
"""
Workflow Demonstration Script for OpenAI Tone Analyzer Integration

This script simulates a complete workflow using the FastAPI endpoints to:
1. Start a workflow
2. Submit data sources (URLs)
3. Perform tone analysis using the new OpenAI analyzer
4. Generate style samples and collect feedback
5. Generate the final article

"""

import json
import requests
import time
import logging
import sys
import os
from typing import Dict, Any, List, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("openai_workflow_demo")

# Configuration
API_BASE_URL = "http://localhost:8001/api"  # FastAPI server on port 8001
DEMO_TOPICS = {
    "tech": {
        "name": "Artificial Intelligence Ethics",
        "sample_text": """
        As AI systems become more integrated into our daily lives, ethical considerations must be at the forefront of development. The responsible deployment of AI technologies requires balancing innovation with safeguards against potential misuse or unintended consequences. This balance necessitates ongoing dialogue among technologists, ethicists, policymakers, and the broader public to establish frameworks that promote beneficial AI while mitigating risks.
        """,
        "urls": [
            "https://en.wikipedia.org/wiki/Ethics_of_artificial_intelligence",
            "https://plato.stanford.edu/entries/ethics-ai/"
        ]
    },
    "business": {
        "name": "Remote Work Transformation",
        "sample_text": """
        Look, the shift to remote work has totally changed how companies operate! It's crazy how businesses had to adapt overnight when the pandemic hit. Some companies totally nailed it, while others struggled with the whole virtual management thing. The best part? Many workers found they were actually MORE productive at home without the typical office distractions and that long commute. But there's definitely a downside too - it's harder to build team culture when everyone's just a face on Zoom, and some folks really miss the separation between work and home life.
        """,
        "urls": [
            "https://hbr.org/2021/03/what-is-your-organizations-long-term-remote-work-strategy",
            "https://www.mckinsey.com/featured-insights/future-of-work/whats-next-for-remote-work-an-analysis-of-2000-tasks-800-jobs-and-nine-countries"
        ]
    },
    "academic": {
        "name": "Quantum Computing Applications",
        "sample_text": """
        The integration of quantum computing into practical applications represents a significant paradigm shift in computational methodologies. Contemporary research indicates that quantum systems exhibit considerable potential in addressing complex optimization problems that remain intractable for classical computing architectures. The implementation of quantum algorithms in fields such as cryptography, material science, and pharmaceutical development demonstrates remarkable efficacy, particularly when applied to problems characterized by exponential complexity. These advancements, facilitated by developments in quantum coherence maintenance and error correction protocols, suggest an imminent transition toward practical quantum advantage in specific domains.
        """,
        "urls": [
            "https://en.wikipedia.org/wiki/Quantum_computing",
            "https://www.nature.com/articles/s41586-019-1666-5"
        ]
    }
}

class OpenAIWorkflowDemo:
    """Demonstrates the complete workflow with OpenAI tone analyzer"""
    
    def __init__(self):
        self.session = requests.Session()
        self.workflow_id = None
        self.selected_style_sample = None
    
    def run_complete_workflow(self, topic_key: str) -> Dict[str, Any]:
        """Run complete workflow demonstration"""
        topic_data = DEMO_TOPICS[topic_key]
        
        logger.info(f"\n{'='*80}\nDEMONSTRATING COMPLETE WORKFLOW FOR: {topic_data['name']}\n{'='*80}\n")
        
        try:
            # STEP 1: Start a new workflow
            self.workflow_id = self.start_workflow(topic_data["name"])
            logger.info(f"Started workflow with ID: {self.workflow_id}")
            
            # STEP 2: Submit URLs for content extraction
            self.submit_urls(topic_data["urls"])
            logger.info(f"Submitted {len(topic_data['urls'])} URLs for content extraction")
            
            # STEP 3: Analyze tone with OpenAI tone analyzer
            tone_result = self.analyze_tone(topic_data["sample_text"])
            logger.info("Tone analysis completed successfully")
            self.display_tone_analysis(tone_result)
            
            # STEP 4: Generate style samples
            style_samples = self.generate_style_samples(topic_data["sample_text"])
            logger.info(f"Generated {len(style_samples.get('samples', []))} style samples")
            self.display_style_samples(style_samples)
            
            # STEP 5: Provide feedback on style sample
            if style_samples.get("samples") and len(style_samples.get("samples", [])) > 0:
                self.selected_style_sample = style_samples["samples"][0]["id"]
                feedback_result = self.submit_sample_feedback(
                    sample_id=self.selected_style_sample,
                    rating="upvote",
                    comments="This writing style matches my preferences perfectly."
                )
                logger.info("Feedback submitted successfully")
            
            # STEP 6: Generate article
            article = self.generate_article()
            logger.info("Article generation completed")
            self.display_article(article)
            
            # Save the results
            self.save_results(topic_key, {
                "workflow_id": self.workflow_id,
                "topic": topic_data["name"],
                "tone_analysis": tone_result,
                "style_samples": style_samples,
                "article": article
            })
            
            return {
                "status": "success",
                "workflow_id": self.workflow_id,
                "article": article
            }
            
        except Exception as e:
            logger.error(f"Error in workflow demonstration: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def start_workflow(self, topic: str) -> str:
        """Start a new workflow"""
        url = f"{API_BASE_URL}/workflow/start"
        payload = {
            "topic": topic,
            "title": f"Article about {topic}",
            "settings": {
                "target_word_count": 1500,
                "tone": "informative"
            }
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("workflow_id")
    
    def submit_urls(self, urls: List[str]) -> Dict[str, Any]:
        """Submit URLs for content extraction"""
        url = f"{API_BASE_URL}/workflow/{self.workflow_id}/data/sources"
        payload = {
            "urls": urls,
            "settings": {
                "depth": "comprehensive",
                "extract_quotes": True,
                "include_metadata": True
            }
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def analyze_tone(self, sample_text: str) -> Dict[str, Any]:
        """Analyze tone using the new OpenAI tone analyzer"""
        url = f"{API_BASE_URL}/workflow/{self.workflow_id}/tone-analysis"
        payload = {
            "source_type": "text",
            "sample_text": sample_text
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def generate_style_samples(self, sample_text: str, num_samples: int = 2) -> Dict[str, Any]:
        """Generate writing style samples based on the sample text"""
        url = f"{API_BASE_URL}/workflow/{self.workflow_id}/style-samples"
        payload = {
            "sample_text": sample_text,
            "num_samples": num_samples,
            "target_length": 250
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def submit_sample_feedback(self, sample_id: int, rating: str, comments: str = "") -> Dict[str, Any]:
        """Submit feedback on a style sample"""
        url = f"{API_BASE_URL}/workflow/{self.workflow_id}/style-sample-feedback"
        payload = {
            "sample_id": sample_id,
            "rating": rating,
            "comments": comments,
            "regenerate": False
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def generate_article(self) -> Dict[str, Any]:
        """Generate the article based on the workflow data"""
        url = f"{API_BASE_URL}/workflow/{self.workflow_id}/article/generate"
        payload = {
            "settings": {
                "target_word_count": 1500,
                "format": "markdown",
                "include_sections": True
            }
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    
    def display_tone_analysis(self, tone_result: Dict[str, Any]):
        """Display the tone analysis results"""
        logger.info("\n" + "-"*40)
        logger.info("TONE ANALYSIS RESULTS")
        logger.info("-"*40)
        
        if tone_result.get("status") == "success":
            analysis = tone_result.get("analysis", {})
            logger.info(f"Formality score: {analysis.get('formality_score', 'N/A')}")
            
            if analysis.get("formal_indicators"):
                logger.info("Formal indicators: " + ", ".join(analysis.get("formal_indicators", [])[:3]))
            
            if analysis.get("informal_indicators"):
                logger.info("Informal indicators: " + ", ".join(analysis.get("informal_indicators", [])[:3]))
            
            if analysis.get("primary_style"):
                logger.info(f"Primary style: {analysis.get('primary_style', 'N/A')}")
            
            if analysis.get("reasoning_style"):
                logger.info(f"Reasoning style: {analysis.get('reasoning_style', 'N/A')}")
            
            if analysis.get("primary_domain"):
                logger.info(f"Primary domain: {analysis.get('primary_domain', 'N/A')}")
        else:
            logger.error(f"Tone analysis failed: {tone_result.get('message', 'Unknown error')}")
    
    def display_style_samples(self, style_samples: Dict[str, Any]):
        """Display the generated style samples"""
        logger.info("\n" + "-"*40)
        logger.info("STYLE SAMPLES")
        logger.info("-"*40)
        
        if style_samples.get("status") == "success":
            # Display style analysis
            style_analysis = style_samples.get("style_analysis", {})
            
            if style_analysis.get("key_characteristics"):
                logger.info("Key characteristics:")
                for i, char in enumerate(style_analysis.get("key_characteristics", [])[:5], 1):
                    logger.info(f"  {i}. {char}")
            
            if style_analysis.get("distinctive_patterns"):
                logger.info("\nDistinctive patterns:")
                for i, pattern in enumerate(style_analysis.get("distinctive_patterns", [])[:3], 1):
                    logger.info(f"  {i}. {pattern}")
            
            # Display samples
            samples = style_samples.get("samples", [])
            for i, sample in enumerate(samples, 1):
                logger.info(f"\nSample {i} (Topic: {sample.get('topic', 'Unknown')})")
                preview = sample.get('sample_text', '')[:200]
                logger.info(f"Preview: {preview}...")
        else:
            logger.error(f"Style sample generation failed: {style_samples.get('message', 'Unknown error')}")
    
    def display_article(self, article_result: Dict[str, Any]):
        """Display the generated article"""
        logger.info("\n" + "-"*40)
        logger.info("GENERATED ARTICLE")
        logger.info("-"*40)
        
        if article_result.get("status") == "success":
            article = article_result.get("article", {})
            logger.info(f"Title: {article.get('title', 'No title')}")
            
            if article.get("subtitle"):
                logger.info(f"Subtitle: {article.get('subtitle')}")
            
            if article.get("introduction"):
                logger.info("\nIntroduction:")
                logger.info(article.get("introduction")[:300] + "...")
            
            if article.get("body"):
                logger.info(f"\nNumber of sections: {len(article.get('body', []))}")
                for i, section in enumerate(article.get("body", [])[:3], 1):
                    logger.info(f"\nSection {i}: {section.get('subheading', 'Unnamed section')}")
                    content_preview = section.get("content", "")[:150]
                    logger.info(f"{content_preview}...")
                
                if len(article.get("body", [])) > 3:
                    logger.info(f"\n... plus {len(article.get('body', [])) - 3} more sections")
            
            if article.get("conclusion"):
                logger.info("\nConclusion preview:")
                logger.info(article.get("conclusion")[:150] + "...")
        else:
            logger.error(f"Article generation failed: {article_result.get('message', 'Unknown error')}")
    
    def save_results(self, topic_key: str, results: Dict[str, Any]):
        """Save the workflow results to a file"""
        results_dir = os.path.join(os.path.dirname(__file__), "results")
        os.makedirs(results_dir, exist_ok=True)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"openai_tone_workflow_{topic_key}_{timestamp}.json"
        filepath = os.path.join(results_dir, filename)
        
        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"\nWorkflow results saved to: {filepath}")

def main():
    """Run the workflow demo"""
    logger.info("OpenAI Tone Analyzer Workflow Demonstration")
    logger.info("==========================================")
    
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
    
    # Create the workflow demo instance
    demo = OpenAIWorkflowDemo()
    
    # Run demonstrations for different style types
    results = {}
    for topic_key in DEMO_TOPICS.keys():
        logger.info(f"\nRunning demonstration for: {topic_key.upper()}")
        result = demo.run_complete_workflow(topic_key)
        results[topic_key] = result
        
        # Add a delay between workflows
        if topic_key != list(DEMO_TOPICS.keys())[-1]:
            logger.info("\nWaiting 5 seconds before next demonstration...")
            time.sleep(5)
    
    # Summary of results
    success_count = sum(1 for r in results.values() if r.get("status") == "success")
    logger.info(f"\n\nDemonstration completed: {success_count}/{len(results)} workflows successful")

if __name__ == "__main__":
    main()
