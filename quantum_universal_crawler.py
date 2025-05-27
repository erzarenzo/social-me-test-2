#!/usr/bin/env python3
"""
Enhanced Quantum Universal Crawler v2.0
Features:
- Topic-prioritized content extraction
- Multi-fallback system with confidence scoring
- Parallel processing capabilities
- Smarter rate limiting and stealth
- Standardized API responses
- In-memory caching
- Limited to 5 pages per domain
"""

import sys
import json
import time
import random
import re
import logging
import urllib.parse
from collections import deque
import concurrent.futures
import math
from datetime import datetime
import hashlib
from typing import Dict, List, Tuple, Union, Optional, Any
from bs4 import Comment

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
import tls_client

# Optional imports - fail gracefully if not available
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import WebDriverException
    SELENIUM_AVAILABLE = True
except ImportError:
    SELENIUM_AVAILABLE = False

# Configure advanced logging
logging.basicConfig(
    level=logging.INFO,
    format='🕵️ %(asctime)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger("QuantumUniversalCrawler")

class CrawlResult:
    """
    Represents the result of a web crawling operation.
    Provides a standardized interface for crawled content.
    """
    def __init__(self, url: str, content: str, confidence: float = 0.5):
        """
        Initialize a CrawlResult object.
        
        Args:
            url (str): The source URL of the content
            content (str): The extracted content
            confidence (float): Confidence score of the extraction, default 0.5
        """
        self.url = url
        self.content = content
        self.confidence = confidence
        self.word_count = len(content.split())
    
    def __iter__(self):
        """
        Make the object iterable to support legacy code.
        
        Yields:
            Tuple of attributes in a specific order
        """
        yield self.url
        yield self.content
        yield self.confidence
        yield self.word_count
    
    def __len__(self):
        """
        Return the number of words in the content.
        
        Returns:
            int: Number of words
        """
        return self.word_count
    
    def __repr__(self):
        """
        String representation of the CrawlResult.
        
        Returns:
            str: Descriptive string of the crawl result
        """
        return f"CrawlResult(url='{self.url}', words={self.word_count}, confidence={self.confidence})"

class RateLimit:
    """Dynamic rate limiting to prevent detection (KP4)"""
    def __init__(self, initial_delay: float = 2.0, max_delay: float = 10.0):
        self.delays = {}  # domain -> delay mapping
        self.initial_delay = initial_delay
        self.max_delay = max_delay
    
    def wait(self, url: str) -> None:
        """Wait appropriate time for domain"""
        domain = urllib.parse.urlparse(url).netloc
        delay = self.delays.get(domain, self.initial_delay)
        
        # Add some randomness to seem more human-like
        jitter = random.uniform(0.5, 1.5)
        actual_delay = delay * jitter
        
        logger.debug(f"Rate limit: Waiting {actual_delay:.2f}s for {domain}")
        time.sleep(actual_delay)
    
    def adjust(self, url: str, success: bool) -> None:
        """Dynamically adjust rate limiting"""
        domain = urllib.parse.urlparse(url).netloc
        current_delay = self.delays.get(domain, self.initial_delay)
        
        if success:
            # Gradually decrease delay on success
            new_delay = max(self.initial_delay, current_delay * 0.8)
        else:
            # Exponential backoff on failure
            new_delay = min(self.max_delay, current_delay * 1.5)
        
        self.delays[domain] = new_delay
        logger.debug(f"Rate limiting for {domain} adjusted to {new_delay:.2f}s")

class ContentCache:
    """Caching mechanism for crawled content (KP18)"""
    def __init__(self, expiry: int = 86400): # Default: 24 hours
        self.expiry = expiry
        self.memory_cache = {}
    
    def _get_key(self, url: str, topic: str) -> str:
        """Generate cache key from URL and topic"""
        return hashlib.md5(f"{url}:{topic}".encode()).hexdigest()
    
    def get(self, url: str, topic: str) -> Optional[CrawlResult]:
        """Retrieve from cache"""
        key = self._get_key(url, topic)
                
        # Check memory cache
        if key in self.memory_cache:
            timestamp, data = self.memory_cache[key]
            if time.time() - timestamp < self.expiry:
                return CrawlResult(**data)
            else:
                # Expired
                del self.memory_cache[key]
                
        return None
    
    def set(self, url: str, topic: str, result: CrawlResult) -> None:
        """Store in cache"""
        key = self._get_key(url, topic)
        result_dict = {
            "url": result.url,
            "content": result.content,
            "confidence": result.confidence
        }
        
        # Store in memory cache
        self.memory_cache[key] = (time.time(), result_dict)
        
        # Simple cleanup of memory cache (avoid memory leaks)
        if len(self.memory_cache) > 1000:  # Max entries
            now = time.time()
            expired_keys = [k for k, (timestamp, _) in self.memory_cache.items() 
                           if now - timestamp >= self.expiry]
            for k in expired_keys:
                del self.memory_cache[k]

class TopicRelevanceScorer:
    """Evaluates content relevance to topic (KP7-KP9)"""
    def __init__(self, topic: str):
        self.topic = topic.lower()
        # Generate keywords from topic (simple)
        self.keywords = set(re.findall(r'\w+', self.topic))
        # Add variations
        expanded = set()
        for word in self.keywords:
            expanded.add(word)
            if len(word) > 3:
                # Add singular/plural variations
                expanded.add(word + 's')
                expanded.add(word + 'es')
                if word.endswith('y'):
                    expanded.add(word[:-1] + 'ies')
        self.keywords = expanded
        logger.debug(f"Topic keywords: {self.keywords}")
    
    def score_paragraph(self, text: str) -> float:
        """Score paragraph relevance (0.0-1.0) with improved phrase matching"""
        if not text or len(text) < 20:
            return 0.0
            
        text_lower = text.lower()
        words = set(re.findall(r'\w+', text_lower))
        
        # Direct topic phrase matching (stronger signal)
        if self.topic in text_lower:
            base_score = 0.8  # Increased from 0.7
        else:
            # Check for partial phrase matches
            topic_parts = self.topic.split()
            if len(topic_parts) > 1:
                # For multi-word topics, check if most parts are present
                matches = sum(1 for part in topic_parts if part in text_lower)
                if matches / len(topic_parts) >= 0.7:  # 70% of topic words present
                    base_score = 0.6
                else:
                    base_score = 0.0
            else:
                base_score = 0.0
        
        # Count keyword matches with weighting for important terms
        matches = words.intersection(self.keywords)
        
        # Create importance weights for keywords
        keyword_importance = {}
        for word in self.keywords:
            # Words from the original topic get higher weight
            if word in self.topic.split():
                keyword_importance[word] = 2.0
            else:
                keyword_importance[word] = 1.0
                
        # Calculate weighted match score
        total_weight = sum(keyword_importance.get(word, 1.0) for word in self.keywords)
        if total_weight > 0:
            weighted_matches = sum(keyword_importance.get(word, 1.0) for word in matches)
            match_score = weighted_matches / total_weight
        else:
            match_score = 0.0
        
        # Calculate density (matches per word)
        word_count = len(text.split())
        density = len(matches) / (word_count or 1)
        density_score = min(1.0, density * 25)  # Increased multiplier
        
        # Combined score with adjusted weights
        final_score = (base_score * 0.5) + (match_score * 0.3) + (density_score * 0.2)
        return min(1.0, final_score)  # Ensure 0.0-1.0 range
    
    def filter_paragraphs(self, paragraphs: List[str], min_confidence: float = 0.3) -> Tuple[List[str], float]:
        """Filter and return relevant paragraphs with average confidence"""
        if not paragraphs:
            return [], 0.0
            
        scored_paragraphs = [(p, self.score_paragraph(p)) for p in paragraphs]
        
        # Keep paragraphs above threshold
        relevant = [(p, score) for p, score in scored_paragraphs if score >= min_confidence]
        
        if not relevant:
            # If nothing is relevant enough, return highest scoring paragraphs
            sorted_paragraphs = sorted(scored_paragraphs, key=lambda x: x[1], reverse=True)
            top_n = min(3, len(sorted_paragraphs))
            relevant = sorted_paragraphs[:top_n]
        
        if not relevant:
            return [], 0.0
            
        filtered_paragraphs = [p for p, _ in relevant]
        avg_confidence = sum(score for _, score in relevant) / len(relevant)
        
        return filtered_paragraphs, avg_confidence

class QuantumUniversalCrawler:
    def __init__(self, topic: str, max_depth: int = 2, max_pages: int = 5):
        """
        Initialize enhanced crawler with topic prioritization and fallbacks
        Limited to 5 pages per domain by default
        """
        self.topic = topic.lower()
        self.max_depth = max_depth
        self.max_pages = max_pages
        
        # Topic relevance scoring system (KP7-KP9)
        self.relevance_scorer = TopicRelevanceScorer(topic)
        
        # Rate limiting (KP4)
        self.rate_limiter = RateLimit()
        
        # Caching (KP18)
        self.cache = ContentCache()
        
        # Advanced request session with smarter retry logic (KP5)
        self.session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[403, 429, 500, 502, 503, 504],
            allowed_methods=["GET", "HEAD"]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

        # TLS Client for stealth requests (KP6)
        self.tls_session = tls_client.Session(
            client_identifier="chrome120",
            random_tls_extension_order=True
        )

        # User Agent Pool with realistic browser profiles
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1'
        ]

        # Selenium webdriver if available (KP3)
        self.selenium_available = SELENIUM_AVAILABLE
        self.driver = None
        
        # State tracking
        self.visited = set()
        self.pages_crawled = 0

    def _sanitize_url(self, url: str) -> str:
        """
        Sanitize and normalize URLs, removing fragments and cleaning up parameters.
        
        Args:
            url (str): The input URL to sanitize
        
        Returns:
            str: A cleaned and normalized URL
        """
        try:
            # Parse the URL
            parsed_url = urllib.parse.urlparse(url)
            
            # Remove fragment and specific problematic parameters
            cleaned_url = parsed_url._replace(fragment='')
            
            # Optionally remove specific query parameters that might be tracking or unnecessary
            query_params = urllib.parse.parse_qs(parsed_url.query)
            filtered_params = {k: v for k, v in query_params.items() 
                               if k not in ['utm_source', 'utm_medium', 'utm_campaign', 'ref', 'text']}
            
            # Reconstruct the URL without fragment and unnecessary parameters
            cleaned_url = cleaned_url._replace(query=urllib.parse.urlencode(filtered_params, doseq=True))
            
            return urllib.parse.urlunparse(cleaned_url)
        except Exception as e:
            logger.warning(f"Error sanitizing URL {url}: {e}")
            return url

    def _robust_url_fetch(self, url: str, timeout: int = 10, max_retries: int = 3) -> str:
        """
        Fetch HTML content from a URL using multiple strategies.
        
        Args:
            url (str): URL to fetch
            timeout (int, optional): Request timeout in seconds. Defaults to 10.
            max_retries (int, optional): Maximum number of retry attempts. Defaults to 3.
        
        Returns:
            str: HTML content of the page
        """
        # Sanitize URL first
        url = self._sanitize_url(url)
        
        # List of fetching strategies
        strategies = [
            self._fetch_with_requests,
            self._fetch_with_tls_client,
            self._fetch_with_selenium
        ]
        
        # Try each strategy
        for strategy in strategies:
            try:
                # Attempt to fetch with current strategy
                html_content = strategy(url, timeout)
                
                # Validate content
                if html_content and len(html_content) > 100:
                    return html_content
            
            except Exception as e:
                logger.warning(f"Fetch strategy {strategy.__name__} failed: {e}")
        
        # If all strategies fail
        logger.error(f"Failed to fetch content from {url}")
        return ""

    def _fetch_with_requests(self, url: str, timeout: int = 10) -> str:
        """
        Fetch URL content using requests library with advanced configurations.
        
        Args:
            url (str): The URL to fetch
            timeout (int, optional): Request timeout in seconds. Defaults to 10.
        
        Returns:
            str: Fetched content or None
        """
        try:
            # Advanced retry strategy
            retry_strategy = Retry(
                total=3,
                backoff_factor=0.3,
                status_forcelist=[429, 500, 502, 503, 504]
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            
            # Create session with retry strategy
            session = requests.Session()
            session.mount("https://", adapter)
            session.mount("http://", adapter)
            
            # Randomize user agent
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept-Language': "en-US,en;q=0.9",
                'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
                'DNT': "1",
                'Upgrade-Insecure-Requests': "1",
                'Cache-Control': "max-age=0"
            }
            
            # Fetch with timeout and advanced settings
            response = session.get(
                url, 
                headers=headers, 
                timeout=timeout, 
                allow_redirects=True
            )
            
            # Raise exception for bad status
            response.raise_for_status()
            
            return response.text
        except requests.RequestException as e:
            logger.warning(f"Requests fetch failed for {url}: {e}")
            return None

    def _fetch_with_tls_client(self, url: str, timeout: int = 10) -> str:
        """
        Fetch URL content using TLS Client for stealth requests.
        
        Args:
            url (str): The URL to fetch
            timeout (int, optional): Request timeout in seconds. Defaults to 10.
        
        Returns:
            str: Fetched content or None
        """
        try:
            response = self.tls_session.get(
                url, 
                headers=self._get_headers(url), 
                timeout_seconds=timeout
            )
            return response.text if response.status_code == 200 else None
        except Exception as e:
            logger.warning(f"TLS Client fetch failed for {url}: {e}")
            return None

    def _fetch_with_selenium(self, url: str, timeout: int = 10) -> str:
        """
        Fetch URL content using Selenium for JavaScript-heavy pages.
        
        Args:
            url (str): The URL to fetch
            timeout (int, optional): Request timeout in seconds. Defaults to 10.
        
        Returns:
            str: Fetched content or None
        """
        if not self.selenium_available:
            return None
            
        try:
            # Initialize driver if needed
            if not self.driver:
                options = Options()
                options.add_argument("--headless")
                options.add_argument("--disable-gpu")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument(f"user-agent={random.choice(self.user_agents)}")
                self.driver = webdriver.Chrome(options=options)
                
            # Load the page
            self.driver.get(url)
            # Wait for dynamic content to load
            time.sleep(3 + random.uniform(1, 3))
            
            # Get the page source
            html = self.driver.page_source
            return html
        except WebDriverException as e:
            logger.warning(f"Selenium fetch failed for {url}: {e}")
            # Try to recover the driver
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
                self.driver = None
            return None
        except Exception as e:
            logger.warning(f"Selenium general error for {url}: {e}")
            return None

    def _get_headers(self, url: str) -> Dict[str, str]:
        """
        Generate context-aware, human-like headers
        """
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc
        
        # Base headers all requests should have
        headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "Cache-Control": "max-age=0"
        }
        
        # Add sensible referer based on the domain
        if random.random() < 0.7:  # 70% of the time
            headers["Referer"] = f"https://www.google.com/search?q={urllib.parse.quote(self.topic + ' ' + domain)}"
        else:
            # Alternative referers
            alt_referers = [
                f"https://duckduckgo.com/?q={urllib.parse.quote(self.topic + ' ' + domain)}&t=h_",
                f"https://www.bing.com/search?q={urllib.parse.quote(self.topic + ' ' + domain)}",
                None  # Sometimes no referer
            ]
            referer = random.choice(alt_referers)
            if referer:
                headers["Referer"] = referer
                
        return headers

    def fetch_page(self, url: str) -> Optional[Tuple[str, str]]:
        """
        Multi-strategy page fetching with fallbacks:
        1. Check cache
        2. Standard requests
        3. TLS Client
        4. Selenium (if available)
        5. Wayback Machine fallback
        
        Returns (html_content, source) or None if all methods fail
        """
        if self.pages_crawled >= self.max_pages:
            logger.info("Reached max pages limit")
            return None
            
        # Check cache first (KP18)
        cached = self.cache.get(url, self.topic)
        if cached and cached.content:
            logger.info(f"Cache hit for {url}")
            self.pages_crawled += 1
            return cached.content, "cache"
            
        # Apply rate limiting (KP4)
        self.rate_limiter.wait(url)

        # Robust URL fetch with fallbacks
        html = self._robust_url_fetch(url)
        if html:
            self.rate_limiter.adjust(url, True)
            return html, "robust_fetch"

        # Wayback Machine fallback (KP11)
        html, source = self._attempt_wayback(url)
        if html:
            self.rate_limiter.adjust(url, True)
            return html, source
            
        # All methods failed
        self.rate_limiter.adjust(url, False)
        logger.warning(f"All extraction methods failed for {url}")
        return None

    def _attempt_wayback(self, url: str) -> Tuple[Optional[str], str]:
        """Wayback Machine snapshot retrieval (KP11)"""
        logger.info(f"Attempting Wayback Machine fallback for {url}")
        wayback_api = "http://web.archive.org/__wb/sparkline?url={}&collection=web&output=json"
        
        try:
            # Query latest snapshot
            r = self.session.get(wayback_api.format(url), timeout=10)
            if r.status_code != 200:
                return None, ""
            
            data = r.json()
            if not data.get("last_ts"):
                return None, ""
            
            # Retrieve the last snapshot
            last_ts = data["last_ts"]
            archived_url = f"http://web.archive.org/web/{last_ts}/{url}"
            
            logger.info(f"Using archived URL: {archived_url}")
            
            # Fetch archived page
            response = self.session.get(archived_url, headers=self._get_headers(url), timeout=15)
            return (response.text if response.status_code == 200 else None, "wayback_machine")
        
        except Exception as e:
            logger.warning(f"Wayback fallback failed: {e}")
            return None, ""

    def deduplicate_paragraphs(self, paragraphs: List[str]) -> List[str]:
        """
        Remove duplicate and nearly-duplicate paragraphs from content
        """
        if not paragraphs:
            return []
            
        # Helper function to calculate similarity between two texts
        def similarity(text1, text2):
            # Simple similarity: what percentage of words in the shorter text appear in the longer text
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            
            # If either set is empty, they're not similar
            if not words1 or not words2:
                return 0.0
                
            # Calculate Jaccard similarity
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            return intersection / union if union > 0 else 0.0
        
        unique_paragraphs = []
        
        for paragraph in paragraphs:
            # Check if this paragraph is similar to any already selected paragraph
            is_duplicate = False
            for existing in unique_paragraphs:
                if similarity(paragraph, existing) > 0.8:  # 80% similarity threshold
                    is_duplicate = True
                    break
                    
            if not is_duplicate:
                unique_paragraphs.append(paragraph)
        
        return unique_paragraphs

    def extract_text_and_links(self, html: str, url: str) -> Tuple[List[str], List[str], List[str]]:
        """
        Extract content and BFS links with improved filtering
        Returns (topic_paragraphs, general_paragraphs, links)
        """
        soup = BeautifulSoup(html, "html.parser")
        
        # Remove non-content tags
        for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'noscript']):
            tag.decompose()
        
        # Content extraction with priority on article content (KP1)
        content_selectors = [
            "article", "main", "div.content", "div.post-content", "div.entry-content",
            ".article-body", ".post-body", '[class*="content"]', '[class*="post"]', 
            "div#content", "div.page", ".markdown-body"
        ]
        
        blocks = []
        
        # Try content selectors first
        for sel in content_selectors:
            found = soup.select(sel)
            for f in found:
                # Skip tiny elements
                if len(f.get_text(strip=True)) < 100:
                    continue
                blocks.append(f.get_text(separator="\n", strip=True))
        
        # If no content found with selectors, fall back to paragraphs
        if not blocks:
            paragraphs = []
            for p in soup.find_all('p'):
                text = p.get_text(strip=True)
                if len(text) > 50:  # Skip very short paragraphs
                    paragraphs.append(text)
            
            if paragraphs:
                blocks = paragraphs
        
        # If still no content, use the body text as last resort (KP2)
        if not blocks:
            body = soup.find('body')
            if body:
                blocks = [body.get_text(separator="\n", strip=True)]
                
        # If somehow still no content, use entire page
        if not blocks:
            blocks = [soup.get_text(separator="\n", strip=True)]
        
        # Split blocks into paragraphs
        all_paragraphs = []
        for block in blocks:
            paragraphs = re.split(r'\n+', block)
            for p in paragraphs:
                p = p.strip()
                if p and len(p) > 50:  # Skip very short paragraphs
                    all_paragraphs.append(p)
        
        # Score and filter paragraphs based on topic relevance (KP7-KP9)
        topic_paragraphs, confidence = self.relevance_scorer.filter_paragraphs(all_paragraphs)
        
        # Keep a copy of all paragraphs for fallback (KP2)
        general_paragraphs = all_paragraphs
        
        # Extract BFS links for crawling
        sublinks = []
        base_domain = urllib.parse.urlparse(url).netloc
        
        for a in soup.find_all('a', href=True):
            try:
                anchor = a.get_text(strip=True)
                link = a["href"]
                
                # Skip anchors, javascript links, and other non-HTTP links
                if link.startswith('#') or link.startswith('javascript:') or link.startswith('mailto:'):
                    continue
                    
                # Convert relative to absolute URLs
                link = urllib.parse.urljoin(url, link)
                ln_dom = urllib.parse.urlparse(link).netloc
                
                # Only keep same-domain links
                if ln_dom == base_domain:
                    # Prioritize links with topic mentions (KP1)
                    if self.relevance_scorer.score_paragraph(anchor) > 0.3:
                        sublinks.insert(0, link)  # Prioritize
                    else:
                        sublinks.append(link)
            except Exception as e:
                logger.debug(f"Error processing link: {e}")
                continue
        
        # Remove duplicates while preserving order
        unique_links = []
        seen = set()
        for link in sublinks:
            if link not in seen:
                unique_links.append(link)
                seen.add(link)
        
        return topic_paragraphs, general_paragraphs, unique_links

    def _preprocess_html(self, html_content: str) -> str:
        """
        Preprocess HTML content to clean and prepare for text extraction.
        
        Args:
            html_content (str): Raw HTML content
        
        Returns:
            str: Cleaned and preprocessed HTML
        """
        try:
            # Use BeautifulSoup for parsing
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script, style, and other non-content tags
            for script_or_style in soup(["script", "style", "head", "header", "footer", "nav", "meta", "input", "textarea"]):
                script_or_style.decompose()
            
            # Remove comments
            for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
                comment.extract()
            
            # Remove empty tags
            for empty_tag in soup.find_all(lambda tag: not tag.contents and tag.name not in ['img', 'br', 'hr']):
                empty_tag.decompose()
            
            # Normalize whitespace
            text = soup.get_text(separator=' ', strip=True)
            
            # Remove excessive whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            return text
        
        except Exception as e:
            logger.warning(f"Error preprocessing HTML: {e}")
            return html_content

    def _extract_text(self, url: str, html_content: str, extraction_source: str = "direct_crawl") -> CrawlResult:
        """
        Extract text from HTML content using multiple strategies.
        
        Args:
            url (str): The source URL
            html_content (str): Raw HTML content
            extraction_source (str, optional): Source of extraction. Defaults to "direct_crawl".
        
        Returns:
            CrawlResult: Extracted text with metadata
        """
        # Validate inputs
        if not html_content:
            return CrawlResult(
                url=url,
                content="No content found.",
                confidence=0.0
            )
        
        # Preprocessing
        html_content = self._preprocess_html(html_content)
        
        # Try multiple extraction strategies
        extraction_strategies = [
            self._extract_main_content,
            self._extract_article_content,
            self._extract_text_from_paragraphs,
            self._fallback_text_extraction
        ]
        
        final_text = ""
        confidence = 0.0
        
        for strategy in extraction_strategies:
            try:
                text, strategy_confidence = strategy(html_content)
                
                # If text is found and confidence is higher, use it
                if text and strategy_confidence > confidence:
                    final_text = text
                    confidence = strategy_confidence
                    
                    # If confidence is high enough, break
                    if confidence > 0.7:
                        break
            except Exception as e:
                logger.warning(f"Text extraction strategy failed: {strategy.__name__}: {e}")
        
        # Final validation
        if not final_text:
            result = CrawlResult(
                url=url,
                content="No relevant content found on this page.",
                confidence=0.0
            )
        else:
            # Truncate very long text to prevent excessive memory usage
            max_words = 5000
            words = final_text.split()
            if len(words) > max_words:
                final_text = " ".join(words[:max_words])
                confidence *= 0.9  # Slightly reduce confidence for truncation
            
            result = CrawlResult(
                url=url,
                content=final_text,
                confidence=confidence
            )
            
        # Cache the result
        if REDIS_AVAILABLE and self.cache:
            self.cache.set(url, self.topic, result)
        
        return result

    def _extract_main_content(self, html_content: str) -> Tuple[str, float]:
        """
        Extract main content from HTML using BeautifulSoup.
        
        Args:
            html_content (str): Preprocessed HTML content
        
        Returns:
            Tuple[str, float]: Extracted text and confidence score
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Try various selectors for main content
            main_selectors = [
                'main', 'article', 'div.main-content', 'div.content', 
                'div#main', 'div#content', 'section.content'
            ]
            
            for selector in main_selectors:
                main_content = soup.select_one(selector)
                if main_content:
                    text = main_content.get_text(separator=' ', strip=True)
                    
                    # Basic confidence scoring
                    confidence = min(1.0, len(text.split()) / 100)
                    
                    return text, confidence
            
            # Fallback: return full text
            text = soup.get_text(separator=' ', strip=True)
            return text, 0.3
        
        except Exception as e:
            logger.warning(f"Error extracting main content: {e}")
            return "", 0.0

    def _extract_article_content(self, html_content: str) -> Tuple[str, float]:
        """
        Extract article content from HTML using BeautifulSoup.
        
        Args:
            html_content (str): Preprocessed HTML content
        
        Returns:
            Tuple[str, float]: Extracted text and confidence score
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Try various article-specific selectors
            article_selectors = [
                'article', 'div.article-body', 'div.post-content', 
                'div.entry-content', 'section.article-content'
            ]
            
            for selector in article_selectors:
                article_content = soup.select_one(selector)
                if article_content:
                    text = article_content.get_text(separator=' ', strip=True)
                    
                    # Confidence scoring based on text length
                    confidence = min(1.0, len(text.split()) / 150)
                    
                    return text, confidence
            
            return "", 0.0
        
        except Exception as e:
            logger.warning(f"Error extracting article content: {e}")
            return "", 0.0

    def _extract_text_from_paragraphs(self, html_content: str) -> Tuple[str, float]:
        """
        Extract text from paragraphs in HTML.
        
        Args:
            html_content (str): Preprocessed HTML content
        
        Returns:
            Tuple[str, float]: Extracted text and confidence score
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find all paragraph tags
            paragraphs = soup.find_all(['p', 'div'])
            
            # Filter paragraphs by length and content
            filtered_paragraphs = [
                p.get_text(strip=True) for p in paragraphs 
                if len(p.get_text(strip=True).split()) > 5
            ]
            
            # Combine paragraphs
            text = " ".join(filtered_paragraphs)
            
            # Confidence scoring
            confidence = min(1.0, len(filtered_paragraphs) / 10)
            
            return text, confidence
        
        except Exception as e:
            logger.warning(f"Error extracting paragraphs: {e}")
            return "", 0.0

    def _fallback_text_extraction(self, html_content: str) -> Tuple[str, float]:
        """
        Fallback method to extract text from HTML.
        
        Args:
            html_content (str): Preprocessed HTML content
        
        Returns:
            Tuple[str, float]: Extracted text and confidence score
        """
        try:
            # If all other methods fail, use the preprocessed text
            text = html_content
            
            # Very low confidence for fallback
            confidence = 0.1
            
            return text, confidence
        
        except Exception as e:
            logger.warning(f"Error in fallback text extraction: {e}")
            return "", 0.0

    def bfs_extract(self, start_url: str) -> CrawlResult:
        """
        Breadth-First Search extraction with improved priority scoring
        
        Args:
            start_url (str): Initial URL to start crawling
        
        Returns:
            CrawlResult: Extracted content with metadata
        """
        # Sanitize and validate URL
        start_url = self._sanitize_url(start_url)
        
        # Initialize BFS variables
        visited = set()
        queue = deque([(start_url, 0)])
        results = []
        
        # Limit total pages to prevent infinite crawling
        max_pages = 5
        
        while queue and len(results) < max_pages:
            current_url, depth = queue.popleft()
            
            # Skip if already visited
            if current_url in visited:
                continue
            
            visited.add(current_url)
            
            try:
                # Fetch page content
                html_content = self._robust_url_fetch(current_url)
                
                # Extract text
                result = self._extract_text(current_url, html_content)
                
                # If content is relevant, add to results
                if result.confidence > 0.3:
                    results.append(result)
                
                # If not at max depth, find and queue new links
                if depth < 1:  # Limit to 1 level deep
                    _, _, links = self.extract_text_and_links(html_content, current_url)
                    
                    # Add new unique links to queue
                    for link in links:
                        if link not in visited and len(queue) < max_pages:
                            queue.append((link, depth + 1))
            
            except Exception as e:
                logger.error(f"Error crawling {current_url}: {e}")
                error_result = CrawlResult(
                    url=current_url,
                    content="",
                    confidence=0.0
                )
                results.append(error_result)
        
        # Combine results
        if not results:
            return CrawlResult(
                url=start_url,
                content="No relevant content found.",
                confidence=0.0
            )
        
        # Combine text from all results
        combined_text = " ".join(result.content for result in results)
        combined_confidence = sum(result.confidence for result in results) / len(results)
        
        return CrawlResult(
            url=start_url,
            content=combined_text,
            confidence=combined_confidence
        )

    def crawl(self, urls: Union[str, List[str]]) -> Union[CrawlResult, List[CrawlResult]]:
        """
        Crawl multiple URLs with threading support
        """
        # Handle case where urls is a single string
        if isinstance(urls, str):
            urls = [urls]
            
        results = []
        
        # Use parallel processing for multiple URLs (KP16)
        if len(urls) > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_to_url = {executor.submit(self.bfs_extract, url): url for url in urls}
                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        logger.error(f"Error crawling {url}: {e}")
                        error_result = CrawlResult(
                            url=url,
                            content="",
                            confidence=0.0
                        )
                        results.append(error_result)
            return results
        else:
            # Single URL case
            return self.bfs_extract(urls[0])

def main():
    """
    Quantum Universal Crawler Entry Point
    """
    if len(sys.argv) < 3:
        print("Usage: python quantum_universal_crawler.py <topic> <url1> <url2> ...", file=sys.stderr)
        sys.exit(1)

    topic = sys.argv[1]
    urls = sys.argv[2:]
    
    if len(urls) > 12:
        urls = urls[:12]
        logger.info("Truncating to 12 URLs max")

    crawler = QuantumUniversalCrawler(topic=topic, max_depth=2, max_pages=5)
    
    results = crawler.crawl(urls)
    
    if isinstance(results, list):
        # Multiple results
        for i, result in enumerate(results):
            print(f"\n=== Result {i+1}/{len(results)} - {result.url} ===\n")
            snippet = result.content[:1000] + "..." if len(result.content) > 1000 else result.content
            print(snippet)
            print(f"\nWord count: {len(result)}, Confidence: {result.confidence:.2f}")
        
        # Summary
        total_words = sum(len(r) for r in results)
        print(f"\n=== Summary ===\n")
        print(f"Topic: {topic}")
        print(f"URLs crawled: {len(results)}")
        print(f"Total word count: {total_words}")
        print(f"Average confidence: {sum(r.confidence for r in results) / len(results):.2f}")
    else:
        # Single result
        result = results
        print("\n=== Extraction Result ===\n")
        snippet = result.content[:2000] + "..." if len(result.content) > 2000 else result.content
        print(snippet)
        
        print("\n=== JSON Summary ===\n")
        print(json.dumps({"url": result.url, "content": result.content, "confidence": result.confidence}, indent=2))

if __name__ == "__main__":
    main()

async def crawl_page(url, topic="AI"):
    """
    Asynchronous wrapper function for FastAPI.
    Fetches a single webpage and extracts content.
    """
    crawler = QuantumUniversalCrawler(topic=topic)
    result = crawler.crawl(url)
    return {"url": result.url, "content": result.content, "confidence": result.confidence} if isinstance(result, CrawlResult) else result[0].to_dict()
