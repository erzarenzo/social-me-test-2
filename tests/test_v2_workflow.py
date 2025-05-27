import requests
import json
import logging
import pprint

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

BASE_URL = 'http://38.242.151.92:8003'
pp = pprint.PrettyPrinter(indent=4)

def test_v2_workflow():
    # Step 1: Start V2 Workflow
    logger.info("Testing V2 Workflow Initialization")
    response = requests.get(f'{BASE_URL}/v2/')
    assert response.status_code == 200, "Failed to start V2 workflow"
    logger.info("V2 Workflow initialized successfully")

    # Step 2: Submit Content Strategy
    logger.info("Testing Content Strategy Submission")
    content_strategy = {
        'primary_topic': 'AI and Machine Learning',
        'content_pillars': ['Natural Language Processing', 'Deep Learning', 'Ethical AI'],
        'target_audience': 'Tech Professionals',
        'tone': 'Professional and Insightful'
    }
    response = requests.post(f'{BASE_URL}/submit-content-strategy', json=content_strategy)
    assert response.status_code == 200, "Failed to submit content strategy"
    logger.info("Content Strategy:")
    pp.pprint(content_strategy)

    # Step 3: Add Data Sources
    logger.info("Testing Data Source Addition")
    data_sources = [
        {
            'source_url': 'https://towardsdatascience.com/ai-research',
            'source_type': 'blog',
            'topic_relevance': 'AI Research Trends'
        },
        {
            'source_url': 'https://www.linkedin.com/in/ai-thought-leaders',
            'source_type': 'professional_profile',
            'topic_relevance': 'AI Industry Insights'
        }
    ]
    
    # Add sources one by one
    for source in data_sources:
        response = requests.post(f'{BASE_URL}/add-source-with-topic', data=source)
        assert response.status_code == 200, f"Failed to add data source: {source['source_url']}"
        logger.info(f"Added source: {source['source_url']}")
    
    logger.info("Data sources added successfully")

    # Step 4: Analyze Writing Style
    logger.info("Testing Writing Style Analysis")
    writing_sample = """
    Artificial Intelligence represents a transformative technological paradigm that transcends traditional computational boundaries. 
    By leveraging advanced machine learning algorithms and neural network architectures, AI systems can now interpret, learn, 
    and make decisions with unprecedented sophistication. The ethical implications of these technologies demand rigorous 
    interdisciplinary examination to ensure responsible development and deployment.
    """
    response = requests.post(f'{BASE_URL}/analyze-writing-style', json={'text': writing_sample})
    assert response.status_code == 200, "Failed to analyze writing style"
    tone_analysis = response.json()
    logger.info("Tone Analysis Results:")
    pp.pprint(tone_analysis)

    # Step 5: Topic-Guided Crawl
    logger.info("Testing Topic-Guided Crawl")
    response = requests.post(f'{BASE_URL}/topic-guided-crawl')
    assert response.status_code == 200, "Failed to perform topic-guided crawl"
    crawl_results = response.json()
    logger.info("Topic-guided crawl completed successfully")
    logger.info("Crawled Data Points:")
    pp.pprint(crawl_results)

    # Step 6: Generate Article
    logger.info("Testing Article Generation")
    response = requests.post(f'{BASE_URL}/generate-article-v2')
    assert response.status_code == 200, "Failed to generate article"
    generated_article = response.json()
    logger.info("Generated Article:")
    pp.pprint(generated_article)

    logger.info("All V2 Workflow tests passed successfully!")

if __name__ == '__main__':
    test_v2_workflow()
