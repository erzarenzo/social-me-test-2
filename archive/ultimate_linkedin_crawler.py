#!/usr/bin/env python3
"""
Ultimate LinkedIn Profile Crawler

A masterpiece of web scraping engineering that transforms 
digital boundaries into pathways of knowledge.
"""

import asyncio
import json
import logging
import random
import sys
from typing import Dict, Any, Optional

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

class LinkedInSoulExtractor:
    """
    A philosophical approach to digital information retrieval.
    We don't just crawl; we commune with the data.
    """

    def __init__(self, patience: int = 30, soul_depth: int = 3):
        """
        Construct a digital bridge between human networks
        
        Args:
            patience (int): Maximum wait time for page interactions
            soul_depth (int): Depth of information extraction
        """
        # Ethereal logging configuration
        logging.basicConfig(
            level=logging.INFO,
            format='✨ %(asctime)s - %(levelname)s: %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('linkedin_soul_extraction.log')
            ]
        )
        self.logger = logging.getLogger("LinkedInSoulExtractor")
        
        # Browser's digital camouflage
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15'
        ]
        
        self.patience = patience
        self.soul_depth = soul_depth
        self.driver = None

    def _prepare_stealth_chrome(self) -> webdriver.Chrome:
        """
        Craft an undetectable digital vessel
        
        Returns:
            Chrome: Stealthily configured WebDriver
        """
        # Chrome options with advanced stealth techniques
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(f"user-agent={random.choice(self.user_agents)}")
        
        # Headless mode with window size
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")

        # Setup Chrome driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Stealth script injection
        driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            window.navigator.chrome = {
                runtime: {}
            };
            delete Object.prototype.WebDriver;
            """
        })
        
        return driver

    async def extract_profile_essence(self, url: str) -> Dict[str, Any]:
        """
        Extract the soul of a LinkedIn profile
        
        Args:
            url (str): LinkedIn profile URL
        
        Returns:
            Dict[str, Any]: Extracted profile information
        """
        try:
            # Initialize our digital medium
            self.driver = self._prepare_stealth_chrome()
            
            # Simulate human arrival
            await asyncio.sleep(random.uniform(1.5, 3.5))
            
            # Navigate with intention
            self.driver.get(url)
            
            # Wait for the profile's digital aura to stabilize
            wait = WebDriverWait(self.driver, self.patience)
            
            # Sacred information gathering
            profile_essence = {
                "name": self._extract_text_safely(wait, "h1.text-heading-xlarge"),
                "headline": self._extract_text_safely(wait, "div.text-body-medium"),
                "about": self._extract_about_section(wait),
                "experience": self._extract_experience(wait),
                "education": self._extract_education(wait),
                "skills": self._extract_skills(wait)
            }
            
            return {k: v for k, v in profile_essence.items() if v}
        
        except Exception as cosmic_interference:
            self.logger.error(f"Extraction ritual interrupted: {cosmic_interference}")
            return {"error": str(cosmic_interference)}
        
        finally:
            # Gracefully close our digital portal
            if self.driver:
                self.driver.quit()

    def _extract_text_safely(self, wait, selector: str) -> Optional[str]:
        """
        Safely extract text with zen-like patience
        
        Args:
            wait (WebDriverWait): Selenium wait object
            selector (str): CSS selector for extraction
        
        Returns:
            Optional[str]: Extracted text or None
        """
        try:
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
            return element.text.strip()
        except (TimeoutException, WebDriverException):
            return None

    def _extract_about_section(self, wait) -> Optional[str]:
        """
        Dive deep into the profile's narrative essence
        
        Args:
            wait (WebDriverWait): Selenium wait object
        
        Returns:
            Optional[str]: About section text
        """
        try:
            # Expand "see more" if exists
            more_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'See more')]")
            for button in more_buttons:
                try:
                    button.click()
                    asyncio.sleep(0.5)
                except:
                    pass
            
            about_section = wait.until(
                EC.presence_of_element_located((By.XPATH, "//section[contains(@id, 'about')]"))
            )
            return about_section.text.strip()
        
        except Exception:
            return None

    def _extract_experience(self, wait) -> list:
        """
        Weave professional journey threads
        
        Args:
            wait (WebDriverWait): Selenium wait object
        
        Returns:
            list: Extracted experience details
        """
        try:
            experiences = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".experience-section li"))
            )
            return [exp.text.strip() for exp in experiences[:self.soul_depth]]
        
        except Exception:
            return []

    def _extract_education(self, wait) -> list:
        """
        Unravel educational constellations
        
        Args:
            wait (WebDriverWait): Selenium wait object
        
        Returns:
            list: Extracted education details
        """
        try:
            education = wait.until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".education-section li"))
            )
            return [edu.text.strip() for edu in education[:self.soul_depth]]
        
        except Exception:
            return []

    def _extract_skills(self, wait) -> list:
        """
        Capture professional skill signatures
        
        Args:
            wait (WebDriverWait): Selenium wait object
        
        Returns:
            list: Extracted skills
        """
        try:
            skills_section = wait.until(
                EC.presence_of_element_located((By.XPATH, "//section[contains(@id, 'skills')]"))
            )
            skills = skills_section.find_elements(By.CSS_SELECTOR, ".skills-section-item")
            return [skill.text.strip() for skill in skills[:self.soul_depth]]
        
        except Exception:
            return []

async def main():
    """
    Orchestrate the digital soul extraction ritual
    """
    if len(sys.argv) < 2:
        print("🌐 Usage: python ultimate_linkedin_crawler.py <linkedin_profile_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    extractor = LinkedInSoulExtractor()
    
    # Perform the extraction
    profile_essence = await extractor.extract_profile_essence(url)
    
    # Illuminate the gathered wisdom
    print("\n🔮 LinkedIn Profile Essence 🔮")
    print(json.dumps(profile_essence, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
