#!/usr/bin/env python3
"""
Multi-Fallback BFS Crawler with Wayback Machine:
1) BFS domain-limited (max_depth=2), up to max_pages=20
2) If normal requests -> blocked, try headless (Playwright).
3) If still blocked, check the Wayback Machine for a snapshot.
4) Topic-based paragraph filtering.
5) Print snippet + JSON summary
"""

import sys
import json
import time
import random
import re
import logging
import urllib.parse
from collections import deque
import asyncio

import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s'
)
logger = logging.getLogger("WaybackBFS")

class MultiFallbackBFS:
    def __init__(self, topic, max_depth=2, max_pages=20):
        self.topic = topic.lower()
        self.max_depth = max_depth
        self.max_pages = max_pages

        self.visited = set()
        self.pages_crawled = 0

        # Basic requests session w/ retries
        self.session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[403, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)

    def _get_headers(self):
        """
        Return advanced headers to reduce blocking risk
        """
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        }

    def _topic_in_text(self, text):
        return self.topic in text.lower()

    async def fetch_page(self, url):
        """
        Try (1) requests, (2) headless, (3) if both blocked -> Wayback fallback
        Return HTML or None
        """
        # Normal requests approach
        html = self._attempt_requests(url)
        if html:
            return html

        # If still no success, try Playwright
        html2 = await self._attempt_playwright(url)
        if html2:
            return html2

        # If still blocked, try Wayback
        wb_html = self._attempt_wayback(url)
        if wb_html:
            return wb_html

        return None

    def _attempt_requests(self, url):
        """
        1) Normal requests approach
        """
        if self.pages_crawled >= self.max_pages:
            logger.info("Reached max pages limit, skipping requests approach.")
            return None
        try:
            time.sleep(random.uniform(1,3))  # "human-like" delay
            self.pages_crawled += 1
            resp = self.session.get(
                url,
                headers=self._get_headers(),
                timeout=15
            )
            if resp.status_code == 200:
                return resp.text
            logger.warning(f"Requests approach blocked or failed (status={resp.status_code}) for {url}")
            return None
        except Exception as e:
            logger.warning(f"Requests approach error for {url}: {e}")
            return None

    async def _attempt_playwright(self, url):
        """
        2) Headless approach with Playwright
        """
        if self.pages_crawled >= self.max_pages:
            logger.info("Reached max pages limit, skipping playwright approach.")
            return None
        try:
            await asyncio.sleep(random.uniform(1,3))
            self.pages_crawled += 1
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(url, timeout=30000)
                await page.wait_for_load_state('networkidle')
                content = await page.content()
                await browser.close()
                return content
        except Exception as e:
            logger.warning(f"Playwright approach error for {url}: {e}")
            return None

    def _attempt_wayback(self, url):
        """
        3) If still blocked, check Wayback Machine for snapshot
           returns archived HTML or None
        """
        logger.info(f"Trying Wayback fallback for {url}")
        # Query the most recent snapshot
        wayback_api = "http://web.archive.org/__wb/sparkline?url={}&collection=web&output=json"
        try:
            r = self.session.get(wayback_api.format(url), timeout=10)
            if r.status_code != 200:
                logger.warning("Wayback request error.")
                return None
            data = r.json()
            if "first_ts" not in data or not data["first_ts"]:
                logger.warning("No Wayback snapshot found.")
                return None
            # Retrieve the *last* snapshot timestamp
            last_ts = data["last_ts"]
            archived_url = f"http://web.archive.org/web/{last_ts}/{url}"
            logger.info(f"Using archived URL: {archived_url}")
            # Now fetch the archived page
            # This does not count again for BFS pages_crawled, or we can if we want
            # We'll do it to avoid infinite usage
            if self.pages_crawled >= self.max_pages:
                logger.info("Reached max pages limit, skipping archived approach.")
                return None
            self.pages_crawled += 1
            resp = self.session.get(archived_url, headers=self._get_headers(), timeout=15)
            if resp.status_code == 200:
                return resp.text
            logger.warning(f"Archived page blocked or not accessible. status={resp.status_code}")
            return None
        except Exception as e:
            logger.warning(f"Wayback fallback error: {e}")
            return None

    def _extract_text_and_links(self, html, url):
        """
        BFS sublinks (topic-based anchor), paragraph filtering
        """
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script","style","nav","footer","header","aside"]):
            tag.decompose()

        # potential content selectors
        content_selectors = ["article", "main", '[class*="content"]', '[class*="post"]', "body"]
        blocks=[]
        for sel in content_selectors:
            found = soup.select(sel)
            for f in found:
                raw = f.get_text(separator=" ", strip=True)
                if len(raw) > 200:
                    blocks.append(raw)
        if not blocks:
            blocks= [soup.get_text(separator=" ", strip=True)]

        combined= "\n\n".join(blocks)
        # topic paragraph filter
        paragraphs= combined.split("\n")
        relevant= [p for p in paragraphs if self._topic_in_text(p)]
        final_text= "\n".join(relevant) if relevant else combined

        # BFS sublinks
        sublinks=[]
        base_domain = urllib.parse.urlparse(url).netloc
        for a in soup.find_all('a', href=True):
            anchor = a.get_text(strip=True)
            link = urllib.parse.urljoin(url, a["href"])
            ln_dom= urllib.parse.urlparse(link).netloc
            # only queue if same domain and anchor/href mention the topic
            if ln_dom== base_domain and (self._topic_in_text(anchor) or self._topic_in_text(a["href"])):
                sublinks.append(link)

        return final_text, sublinks

    async def bfs_extract(self, start_url):
        """
        BFS domain-limited approach
        """
        from collections import deque
        queue = deque([(start_url, 0)])
        base = urllib.parse.urlparse(start_url).netloc
        gathered=[]

        while queue:
            cur_url, depth = queue.popleft()
            if cur_url in self.visited:
                continue
            self.visited.add(cur_url)

            if depth> self.max_depth:
                break
            if self.pages_crawled>= self.max_pages:
                logger.info("Hit max pages limit, stopping BFS.")
                break

            logger.info(f"Crawling {cur_url} (depth={depth})")
            html= await self.fetch_page(cur_url)
            if not html:
                continue

            text, links= self._extract_text_and_links(html, cur_url)
            if text:
                gathered.append(text)

            if depth< self.max_depth:
                nd= depth+1
                for ln in links:
                    if ln not in self.visited:
                        queue.append((ln, nd))

        return "\n\n".join(gathered)

    async def crawl(self, urls):
        """
        BFS each domain, combine
        """
        entire_corpus=[]
        for url in urls:
            domain_text= await self.bfs_extract(url)
            entire_corpus.append(domain_text)
        return "\n\n".join(entire_corpus)

def main():
    """
    usage: python3 universal_crawler.py <topic> <url1> <url2> ... <urlN>
    BFS domain-limited, multi-fallback:
      1) requests approach
      2) playwright approach
      3) wayback fallback
    paragraphs with <topic> or entire text if none match
    """
    if len(sys.argv)<3:
        print("Usage: python3 universal_crawler.py <topic> <url1> <url2> ... <urlN>", file=sys.stderr)
        sys.exit(1)

    topic= sys.argv[1]
    urls= sys.argv[2:]
    if len(urls)>12:
        urls= urls[:12]
        logger.info("Truncating to 12 URLs max")

    crawler= MultiFallbackBFS(topic=topic, max_depth=2, max_pages=20)

    loop= asyncio.get_event_loop()
    corpus= loop.run_until_complete(crawler.crawl(urls))

    # snippet
    snippet= corpus[:2000]
    if len(corpus)>2000:
        snippet+="..."

    print("\n=== BFS Extraction Snippet ===\n")
    print(snippet)

    # JSON summary
    wc= len(corpus.split())
    res= {
        "topic": topic,
        "word_count": wc,
        "extracted_text": corpus
    }
    print("\n=== JSON Summary ===\n")
    print(json.dumps(res, indent=2))

if __name__=="__main__":
    loop= asyncio.get_event_loop()
    main()
