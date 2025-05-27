"""
Enhanced QuantumUniversalCrawler with improved content extraction capabilities.
As per memory: lowered confidence thresholds from 0.3 to 0.1, implemented multiple fallback extraction methods,
targeted content-rich domains, and improved HTML parsing.
"""
import re
import httpx
import logging
import tls_client
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional, Tuple, Set
import json
import random
import time
import urllib.parse
from urllib.parse import urlparse, urljoin, quote_plus

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('crawler')

class QuantumUniversalCrawler:
    """
    Enhanced web crawler that extracts content from URLs with multiple fallback methods.
    Capable of collecting 18,000+ words of content as mentioned in the memory.
    """
    
    def __init__(self, confidence_threshold: float = 0.1):
        """
        Initialize the crawler with a lower confidence threshold (0.1 instead of 0.3).
        """
        self.confidence_threshold = confidence_threshold
        self.session = tls_client.Session(
            client_identifier="chrome112",
            random_tls_extension_order=True
        )
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "DNT": "1"
        }
        
    def extract_from_urls(self, urls: List[str], min_word_target: int = 12000, topic: Optional[str] = None) -> Dict[str, Any]:
        """
        Extract content from multiple URLs, ensuring a minimum word count is reached.
        If a topic is provided, it will also enrich the URLs with topic-specific content.
        
        Args:
            urls: List of URLs to extract content from
            min_word_target: Minimum number of words to extract (default 12000)
            topic: Optional topic to focus the content extraction (enriches URLs)
            
        Returns:
            Dictionary with processed sources and statistics
        """
        results = {
            "processed_sources": [],
            "total_word_count": 0,
            "successful_extractions": 0,
            "failed_extractions": 0
        }
        
        # Enrich URLs based on topic if provided
        if topic and urls:
            logger.info(f"Enriching URLs with topic: {topic}")
            enriched_urls = self.enrich_urls_with_topic(urls, topic)
            # Combine original and enriched URLs, prioritizing enriched ones
            all_urls = list(enriched_urls) + [url for url in urls if url not in enriched_urls]
            logger.info(f"Added {len(enriched_urls) - len(set(urls).intersection(enriched_urls))} topic-specific URLs")
        else:
            all_urls = urls
        
        # Prioritize content-rich domains
        prioritized_urls = self._prioritize_content_rich_domains(all_urls)
        
        # Keep track of processed domains to avoid duplicates
        processed_domains = set()
        
        for url in prioritized_urls:
            try:
                # Skip if we've already processed content from this domain and have enough words
                domain = urlparse(url).netloc
                if domain in processed_domains and results["total_word_count"] >= min_word_target * 0.5:
                    logger.info(f"Skipping additional URL from already processed domain: {domain}")
                    continue
                
                logger.info(f"Extracting content from: {url}")
                content, metadata = self._extract_with_fallbacks(url)
                
                # Skip if extraction failed or content is too short
                if not content or len(content.split()) < 100:
                    logger.warning(f"Insufficient content extracted from {url}")
                    results["failed_extractions"] += 1
                    continue
                    
                word_count = len(content.split())
                
                source_data = {
                    "url": url,
                    "content": content,
                    "word_count": word_count,
                    "metadata": metadata
                }
                
                results["processed_sources"].append(source_data)
                results["total_word_count"] += word_count
                results["successful_extractions"] += 1
                processed_domains.add(domain)
                
                logger.info(f"Successfully extracted {word_count} words from {url}")
                
                # Add a small delay to avoid being blocked
                time.sleep(random.uniform(1, 3))
                
                # If we've reached our target, we can stop
                if results["total_word_count"] >= min_word_target:
                    logger.info(f"Reached target of {min_word_target} words, stopping extraction")
                    break
                    
            except Exception as e:
                logger.error(f"Error extracting from {url}: {str(e)}")
                results["failed_extractions"] += 1
        
        logger.info(f"Extraction complete. Total words: {results['total_word_count']}")
        return results
    
    def _prioritize_content_rich_domains(self, urls: List[str]) -> List[str]:
        """
        Prioritize content-rich domains like Wikipedia, IBM, and NVIDIA.
        """
        # Define content-rich domains with higher priority
        priority_domains = ["wikipedia.org", "ibm.com", "nvidia.com", "blog", "research", "article", "docs"]
        
        # Sort URLs by priority
        def get_priority(url):
            domain = urlparse(url).netloc
            for i, priority_domain in enumerate(priority_domains):
                if priority_domain in domain:
                    return i
            return len(priority_domains)
        
        return sorted(urls, key=get_priority)
    
    def _extract_with_fallbacks(self, url: str) -> Tuple[str, Dict[str, Any]]:
        """
        Extract content using multiple fallback methods.
        
        Returns:
            Tuple containing (extracted_content, metadata)
        """
        metadata = {"extraction_method": "unknown", "confidence": 0.0}
        
        # Ensure URL has protocol prefix
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
            logger.info(f"Added https:// prefix to URL: {url}")
        
        # Try TLS client first (anti-bot protection)
        try:
            # Set follow_redirects=True to handle 301/302 redirects
            response = self.session.get(url, headers=self.headers, allow_redirects=True)
            if response.status_code == 200:
                html = response.text
                # Log the final URL after potential redirects
                if response.url != url:
                    logger.info(f"Followed redirect from {url} to {response.url}")
                    url = response.url  # Update URL to the final redirected URL
            else:
                logger.warning(f"TLS client request failed with status {response.status_code}")
                raise Exception("TLS client request failed")
        except Exception as e:
            logger.warning(f"TLS client failed, falling back to httpx: {str(e)}")
            try:
                # Use follow_redirects=True in httpx as well
                response = httpx.get(url, headers=self.headers, timeout=15, follow_redirects=True)
                if response.status_code == 200:
                    html = response.text
                    # Log the final URL after potential redirects
                    if str(response.url) != url:
                        logger.info(f"Followed redirect from {url} to {response.url}")
                        url = str(response.url)  # Update URL to the final redirected URL
                else:
                    logger.error(f"Failed to fetch {url}: HTTP {response.status_code}")
                    return "", metadata
            except Exception as e:
                logger.error(f"Failed to fetch {url}: {str(e)}")
                return "", metadata
        
        # Multiple content extraction methods
        content = ""
        confidence = 0.0
        
        # Method 1: Extract from article tags (highest confidence)
        article_content, article_confidence = self._extract_from_article_tags(html)
        if article_confidence > confidence:
            content = article_content
            confidence = article_confidence
            metadata["extraction_method"] = "article_tags"
        
        # Method 2: Extract from main content div
        main_content, main_confidence = self._extract_from_main_content(html)
        if main_confidence > confidence:
            content = main_content
            confidence = main_confidence
            metadata["extraction_method"] = "main_content"
        
        # Method 3: Extract from p tags
        p_content, p_confidence = self._extract_from_p_tags(html)
        if p_confidence > confidence:
            content = p_content
            confidence = p_confidence
            metadata["extraction_method"] = "p_tags"
        
        # Method 4: Last resort - extract all text
        if confidence < self.confidence_threshold:
            all_text, all_confidence = self._extract_all_text(html)
            if all_confidence > confidence:
                content = all_text
                confidence = all_confidence
                metadata["extraction_method"] = "all_text"
        
        metadata["confidence"] = confidence
        metadata["word_count"] = len(content.split())
        
        return content, metadata
    
    def _extract_from_article_tags(self, html: str) -> Tuple[str, float]:
        """Extract content from article tags."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            article_tags = soup.find_all('article')
            
            if not article_tags:
                return "", 0.0
            
            # Get the largest article tag by content length
            article_content = max([tag.get_text(separator=' ', strip=True) for tag in article_tags], 
                                 key=len, default="")
            
            # Calculate confidence based on content length
            word_count = len(article_content.split())
            confidence = min(0.9, 0.5 + (word_count / 2000))
            
            return article_content, confidence
        except Exception as e:
            logger.error(f"Error extracting from article tags: {str(e)}")
            return "", 0.0
    
    def _extract_from_main_content(self, html: str) -> Tuple[str, float]:
        """Extract content from main content div."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for common content div IDs and classes
            content_selectors = [
                '#content', '#main-content', '#article-content', '.content', '.article', 
                'main', '[role="main"]', '.post-content', '.entry-content', '.main-content'
            ]
            
            for selector in content_selectors:
                content_div = None
                if selector.startswith('#'):
                    content_div = soup.find(id=selector[1:])
                elif selector.startswith('.'):
                    content_div = soup.find(class_=selector[1:])
                elif selector.startswith('['):
                    attr, value = selector[1:-1].split('=')
                    content_div = soup.find(attrs={attr.strip(): value.strip('"')})
                else:
                    content_div = soup.find(selector)
                
                if content_div:
                    content = content_div.get_text(separator=' ', strip=True)
                    word_count = len(content.split())
                    
                    if word_count > 200:
                        confidence = min(0.8, 0.3 + (word_count / 1500))
                        return content, confidence
            
            return "", 0.0
        except Exception as e:
            logger.error(f"Error extracting from main content: {str(e)}")
            return "", 0.0
    
    def _extract_from_p_tags(self, html: str) -> Tuple[str, float]:
        """Extract content from p tags."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            p_tags = soup.find_all('p')
            
            if not p_tags:
                return "", 0.0
            
            # Join all p tag content
            p_content = ' '.join([p.get_text(strip=True) for p in p_tags if len(p.get_text(strip=True)) > 20])
            
            # Calculate confidence based on content length
            word_count = len(p_content.split())
            confidence = min(0.7, 0.2 + (word_count / 2000))
            
            return p_content, confidence
        except Exception as e:
            logger.error(f"Error extracting from p tags: {str(e)}")
            return "", 0.0
    
    def _extract_all_text(self, html: str) -> Tuple[str, float]:
        """Extract all text as a last resort."""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Remove script, style, and other non-content tags
            for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
                tag.decompose()
            
            # Extract all text
            text = soup.get_text(separator=' ', strip=True)
            
            # Clean up the text
            text = re.sub(r'\s+', ' ', text)
            
            # Calculate confidence (lowest confidence method)
            word_count = len(text.split())
            confidence = min(0.4, 0.1 + (word_count / 3000))
            
            return text, confidence
        except Exception as e:
            logger.error(f"Error extracting all text: {str(e)}")
            return "", 0.0

    def enrich_urls_with_topic(self, base_urls: List[str], topic: str) -> Set[str]:
        """
        Enriches the provided URLs with topic-specific content using search APIs and 
        domain-specific path generation. This makes the crawler more autonomous by 
        finding relevant content without requiring specific article URLs.
        
        Args:
            base_urls: List of base domain URLs to enrich
            topic: The topic to focus on for URL enrichment
            
        Returns:
            Set of enriched URLs (including original ones if they're relevant)
        """
        enriched_urls = set()
        
        # 1. Add original URLs to the set
        for url in base_urls:
            enriched_urls.add(url)
        
        try:
            # 2. Generate domain-specific paths for common domains
            domain_specific_urls = self._generate_domain_specific_paths(base_urls, topic)
            enriched_urls.update(domain_specific_urls)
            
            # 3. Use search APIs to find relevant URLs
            search_results = self._search_topic(topic, max_results=15)
            enriched_urls.update(search_results)
            
            # 4. Find topic-specific paths on Wikipedia (often high-quality content)
            wiki_urls = self._find_wikipedia_articles(topic)
            enriched_urls.update(wiki_urls)
            
            logger.info(f"URL enrichment complete. Found {len(enriched_urls)} URLs relevant to topic: {topic}")
            return enriched_urls
            
        except Exception as e:
            logger.error(f"Error during URL enrichment: {str(e)}")
            # Return original URLs if enrichment fails
            return set(base_urls)
    
    def _generate_domain_specific_paths(self, base_urls: List[str], topic: str) -> Set[str]:
        """
        Generate domain-specific paths for common domains based on the topic.
        """
        topic_slug = topic.lower().replace(' ', '-')
        topic_words = topic.lower().split()
        topic_query = quote_plus(topic)
        
        domain_paths = {
            'ibm.com': [
                f'/topics/{topic_slug}',
                f'/blogs/research/category/{topic_slug}',
                f'/search?query={topic_query}'
            ],
            'nvidia.com': [
                f'/en-us/research/{topic_slug}',
                f'/en-us/industries/{topic_slug}',
                f'/blog/ai-{topic_slug}'
            ],
            'medium.com': [
                f'/search?q={topic_query}',
                f'/tag/{topic_slug}'
            ],
            'techcrunch.com': [
                f'/search/{topic_query}',
                f'/tag/{topic_slug}'
            ],
            'wikipedia.org': [
                f'/wiki/{topic.title().replace(" ", "_")}',
                f'/wiki/Category:{topic.title().replace(" ", "_")}'
            ],
            'forbes.com': [
                f'/search/?q={topic_query}',
                f'/sites/{topic_slug}'
            ],
            'wired.com': [
                f'/search/?q={topic_query}',
                f'/tag/{topic_slug}'
            ],
            'theverge.com': [
                f'/search?q={topic_query}',
                f'/tag/{topic_slug}'
            ],
            'substack.com': [
                f'/search?q={topic_query}'
            ],
            'arxiv.org': [
                f'/search/?query={topic_query}&searchtype=all'
            ],
            'reddit.com': [
                f'/search/?q={topic_query}',
                f'/r/{topic_words[0]}'
            ],
            'github.com': [
                f'/search?q={topic_query}'
            ],
            'perplexity.ai': [
                f'/search?q={topic_query}'
            ]
        }
        
        result_urls = set()
        
        for url in base_urls:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
            
            # Handle URLs without domain
            if not domain and '/' not in url:
                domain = url
            
            # If domain is in our mapping, generate paths
            for known_domain, paths in domain_paths.items():
                if known_domain in domain:
                    # Ensure URL has protocol
                    if not parsed_url.scheme:
                        base = f"https://{domain}"
                    else:
                        base = f"{parsed_url.scheme}://{domain}"
                    
                    # Add each path variation
                    for path in paths:
                        full_url = urljoin(base, path)
                        result_urls.add(full_url)
        
        return result_urls
    
    def _search_topic(self, topic: str, max_results: int = 15) -> Set[str]:
        """
        Use a public search API to find URLs relevant to the topic.
        """
        result_urls = set()
        
        # Try multiple methods to find relevant URLs
        try:
            # Method 1: Use DuckDuckGo's HTML results
            encoded_query = quote_plus(f"{topic} research article")
            ddg_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            
            response = self.session.get(ddg_url, headers=self.headers, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract result links
            results = soup.select('.result__url')
            for result in results[:max_results]:
                link = result.text.strip()
                if link and not link.startswith('ad|'):
                    # Normalize URL
                    if not link.startswith(('http://', 'https://')):
                        link = 'https://' + link
                    result_urls.add(link)
        except Exception as e:
            logger.warning(f"Error using DuckDuckGo search: {str(e)}")
        
        # If we didn't get enough results, try another method
        if len(result_urls) < max_results / 2:
            try:
                # Method 2: Use an alternative API
                encoded_query = quote_plus(topic)
                search_url = f"https://api.serper.dev/search?q={encoded_query}"
                
                # Try with a generic request (no API key)
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
                }
                
                response = httpx.get(search_url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    data = response.json()
                    organic_results = data.get('organic', [])
                    
                    for result in organic_results[:max_results]:
                        link = result.get('link')
                        if link:
                            result_urls.add(link)
            except Exception as e:
                logger.warning(f"Error using serper.dev search: {str(e)}")
        
        return result_urls
    
    def _find_wikipedia_articles(self, topic: str) -> Set[str]:
        """
        Find relevant Wikipedia articles for the topic.
        """
        result_urls = set()
        
        try:
            # Use Wikipedia's API to search for relevant articles
            encoded_query = quote_plus(topic)
            wiki_url = f"https://en.wikipedia.org/w/api.php?action=opensearch&search={encoded_query}&limit=10&namespace=0&format=json"
            
            response = httpx.get(wiki_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if len(data) >= 4:  # Wikipedia API returns a list with 4 elements
                    article_urls = data[3]  # The 4th element contains the URLs
                    result_urls.update(article_urls)
        except Exception as e:
            logger.warning(f"Error finding Wikipedia articles: {str(e)}")
        
        return result_urls
    
    def extract_tone_data(self, url: str) -> Dict[str, Any]:
        """
        Extract content and perform basic tone analysis metrics, such as average sentence length.
        """
        content, metadata = self._extract_with_fallbacks(url)
        if not content:
            return {"content": "", "tone_metrics": {}, "metadata": metadata}
        sentences = content.split('. ')
        tone_metrics = {
            "average_sentence_length": sum(len(s.split()) for s in sentences) / len(sentences) if sentences else 0,
            "formality_score": 0.5  # Placeholder; can be enhanced with AI for more accuracy
        }
        return {"content": content, "tone_metrics": tone_metrics, **metadata}
