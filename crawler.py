import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import logging
import time
import random
import pickle
import os

# Enhanced Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("crawler_debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("AdvancedLinkedInCrawler")

class LinkedInCrawler:
    def __init__(self):
        """
        Initialize crawler with robust WebDriver setup
        """
        # User-Agent Pool
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15'
        ]
        
        # Secure credential management
        self.linkedin_email = os.getenv("LINKEDIN_EMAIL")
        self.linkedin_password = os.getenv("LINKEDIN_PASSWORD")
        
        # WebDriver setup with error handling
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            
            # Use WebDriver Manager for automatic driver management
            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), 
                options=chrome_options
            )
            
            # Browser configuration to appear more human-like
            self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                })
                """
            })
        
        except Exception as e:
            logger.error(f"WebDriver initialization failed: {e}")
            self.driver = None

    def linkedin_login(self):
        """
        Enhanced LinkedIn login with multiple error handling strategies
        """
        if not self.driver:
            logger.error("WebDriver not initialized")
            return False
        
        try:
            self.driver.get("https://www.linkedin.com/login")
            
            # Wait for elements with explicit waits
            email_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            password_input = self.driver.find_element(By.ID, "password")
            login_button = self.driver.find_element(By.XPATH, "//button[contains(@class, 'btn__primary--large')]")

            email_input.send_keys(self.linkedin_email)
            time.sleep(random.uniform(1, 2))
            password_input.send_keys(self.linkedin_password)
            time.sleep(random.uniform(1, 2))
            login_button.click()

            # More robust login verification
            WebDriverWait(self.driver, 10).until(
                EC.url_contains("feed")
            )
            
            logger.info("✅ LinkedIn login successful")
            return True
        
        except Exception as e:
            logger.error(f"LinkedIn login failed: {e}")
            return False

    def extract_profile_data(self, url, topic):
        """
        Robust LinkedIn profile data extraction
        """
        if not self.linkedin_login():
            logger.error("Cannot extract data without login")
            return None

        try:
            self.driver.get(url)
            time.sleep(random.uniform(3, 5))

            # Extract profile details with robust selectors
            profile_data = {
                "name": self._safe_extract_text("//h1"),
                "headline": self._safe_extract_text("//div[contains(@class, 'text-body-medium')]"),
                "about": self._safe_extract_text("//section[contains(@id, 'about')]"),
                "posts": self._extract_relevant_posts(topic)
            }

            return profile_data

        except Exception as e:
            logger.error(f"Profile extraction error: {e}")
            return None

    def _safe_extract_text(self, xpath, default="Not found"):
        """
        Safe text extraction with fallback
        """
        try:
            element = self.driver.find_element(By.XPATH, xpath)
            return element.text.strip()
        except:
            return default

    def _extract_relevant_posts(self, topic, max_posts=5):
        """
        Extract posts relevant to the given topic
        """
        relevant_posts = []
        try:
            post_elements = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'feed-shared-update')]")
            
            for post in post_elements[:max_posts]:
                post_text = post.text.strip()
                if topic.lower() in post_text.lower():
                    relevant_posts.append(post_text[:500])
                
                if len(relevant_posts) == max_posts:
                    break
            
            return relevant_posts or ["No topic-relevant posts found"]
        
        except Exception as e:
            logger.error(f"Post extraction error: {e}")
            return ["Post extraction failed"]

    def close(self):
        """
        Safely close the WebDriver
        """
        if self.driver:
            self.driver.quit()

def main():
    crawler = LinkedInCrawler()
    
    try:
        url = input("Enter LinkedIn Profile URL: ")
        topic = input("Enter Topic for Extraction: ")
        
        profile_data = crawler.extract_profile_data(url, topic)
        
        if profile_data:
            print("\n=== LinkedIn Profile Data ===")
            for key, value in profile_data.items():
                print(f"\n{key.upper()}:")
                if isinstance(value, list):
                    for item in value:
                        print(f"- {item}")
                else:
                    print(value)
    
    except Exception as e:
        logger.error(f"Crawling process failed: {e}")
    
    finally:
        crawler.close()

if __name__ == "__main__":
    main()
