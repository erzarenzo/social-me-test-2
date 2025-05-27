import requests
from bs4 import BeautifulSoup
import random
import logging
import time
from urllib.parse import urlparse
from app.socialme_app import app, db, Source

# Configure advanced logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

# User-Agent pool
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    # Add more user agents as needed
]

# Session to maintain cookies
session = requests.Session()

def create_robust_request(url, timeout=20, retry_count=2, delay=3):
    """
    Robust request with retry and randomized headers
    """
    headers = {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
    }
    
    # Retry mechanism for robustness
    for attempt in range(retry_count):
        try:
            response = session.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return response
            logger.warning(f"Retry {attempt+1}/{retry_count} failed.")
            time.sleep(delay)
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(delay)
    
    return None

def add_source_with_content(url):
    """
    Extract content from URL and add to database
    """
    with app.app_context():
        response = create_robust_request(url)
        if not response:
            logger.warning(f"Failed to fetch {url}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text(strip=True)
        
        if len(content) > 200:  # Arbitrary check for meaningful content
            source = Source(link=url, source_type="article")
            db.session.add(source)
            db.session.commit()
            logger.info(f"Source {url} added successfully.")
        else:
            logger.warning(f"Not enough content at {url}")
