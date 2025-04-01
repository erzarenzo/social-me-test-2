#!/usr/bin/env python3
import asyncio
import json
import logging
import random
import re
import sys
import time
from typing import Dict, Any, Optional

import requests
import tls_client
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

class HumanLikeLinkedInCrawler:
    def __init__(self, timeout: int = 30):
        """
        Initialize a human-like LinkedIn profile crawler
        """
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger("LinkedInHumanCrawler")
        
        self.timeout = timeout
        
        # Sophisticated User-Agent Pool
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
        ]
        
        # TLS Client for advanced requests
        self.tls_session = tls_client.Session(
            client_identifier="chrome120",
            random_tls_extension_order=True
        )

    def _generate_human_headers(self, url: str) -> Dict[str, str]:
        """
        Generate sophisticated, human-like request headers
        """
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.google.com/search?q=linkedin+profile',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Connection': 'keep-alive'
        }

    async def _playwright_extraction(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Advanced Playwright-based extraction simulating human browsing
        """
        try:
            async with async_playwright() as p:
                # Launch browser with anti-detection
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-infobars'
                    ]
                )
                
                # Create context with realistic fingerprint
                context = await browser.new_context(
                    user_agent=random.choice(self.user_agents),
                    viewport={'width': 1920, 'height': 1080}
                )
                
                # Stealth techniques
                await context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                """)
                
                page = await context.new_page()
                
                # Simulate human-like navigation
                await page.goto(url, wait_until='networkidle', timeout=self.timeout * 1000)
                
                # Extract profile data with JavaScript
                profile_data = await page.evaluate("""() => {
                    const extractText = (selector) => {
                        const element = document.querySelector(selector);
                        return element ? element.innerText.trim() : '';
                    };
                    
                    return {
                        name: extractText('h1.text-heading-xlarge'),
                        headline: extractText('div.text-body-medium'),
                        about: extractText('section[id^="about"] div.inline-show-more-text'),
                        experience: Array.from(
                            document.querySelectorAll('.experience-section li')
                        ).map(exp => exp.innerText).join('\\n')
                    };
                }""")
                
                await browser.close()
                return profile_data
        
        except Exception as e:
            self.logger.warning(f"Playwright extraction failed: {e}")
            return None

    def _requests_extraction(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Requests-based extraction with semantic parsing
        """
        try:
            headers = self._generate_human_headers(url)
            response = requests.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                profile_data = {
                    'name': self._safe_extract(soup, 'h1.text-heading-xlarge'),
                    'headline': self._safe_extract(soup, 'div.text-body-medium'),
                    'about': self._safe_extract(soup, 'section[id^="about"] div.inline-show-more-text'),
                    'meta_description': self._extract_meta_description(soup)
                }
                
                return profile_data
            
            return None
        
        except Exception as e:
            self.logger.warning(f"Requests extraction failed: {e}")
            return None

    def _safe_extract(self, soup, selector: str) -> str:
        """
        Safe text extraction with fallback
        """
        try:
            element = soup.select_one(selector)
            return element.get_text(strip=True) if element else ''
        except:
            return ''

    def _extract_meta_description(self, soup) -> str:
        """
        Extract meta description tags
        """
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        og_desc = soup.find('meta', property='og:description')
        
        descriptions = []
        if meta_desc and meta_desc.get('content'):
            descriptions.append(meta_desc['content'])
        if og_desc and og_desc.get('content'):
            descriptions.append(og_desc['content'])
        
        return ' | '.join(descriptions)

    async def extract_profile(self, url: str) -> Dict[str, Any]:
        """
        Comprehensive profile extraction with multiple strategies
        """
        # Extraction strategies
        strategies = [
            self._playwright_extraction,
            lambda url: self._requests_extraction(url)
        ]
        
        # Try each strategy
        for strategy in strategies:
            try:
                # Add random human-like delay
                await asyncio.sleep(random.uniform(1.0, 3.0))
                
                result = await strategy(url) if asyncio.iscoroutinefunction(strategy) else strategy(url)
                
                if result:
                    return result
            
            except Exception as e:
                self.logger.warning(f"Extraction strategy failed: {e}")
        
        return {"error": "No profile data could be extracted"}

async def main():
    """
    Main execution for LinkedIn profile crawler
    """
    if len(sys.argv) < 2:
        print("Usage: python linkedin_crawler.py <linkedin_profile_url>")
        sys.exit(1)
    
    url = sys.argv[1]
    crawler = HumanLikeLinkedInCrawler()
    
    try:
        # Extract profile
        profile_data = await crawler.extract_profile(url)
        
        # Pretty print results
        print("\n🔍 LinkedIn Profile Extraction Results 🔍")
        print(json.dumps(profile_data, indent=2))
    
    except Exception as e:
        print(f"Extraction failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
