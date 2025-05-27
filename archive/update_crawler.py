#!/usr/bin/env python3

# Read the original file
with open("quantum_universal_crawler.py", "r") as f:
    content = f.read()

# Create a backup
with open("quantum_universal_crawler.py.bak2", "w") as f:
    f.write(content)
    print("Backup created at quantum_universal_crawler.py.bak2")

# Update constructor to use max_pages=5 by default
original_init = """    def __init__(self, topic, max_depth=2, max_pages=20):
        \"\"\"
        Initialize quantum crawler with multi-strategy extraction
        \"\"\"
        self.topic = topic.lower()
        self.max_depth = max_depth
        self.max_pages = max_pages"""

updated_init = """    def __init__(self, topic, max_depth=2, max_pages=5):
        \"\"\"
        Initialize quantum crawler with multi-strategy extraction
        Limited to 5 pages per domain by default for efficiency
        \"\"\"
        self.topic = topic.lower()
        self.max_depth = max_depth
        self.max_pages = max_pages"""

# Replace the constructor
updated_content = content.replace(original_init, updated_init)

# Update the domain tracking in the crawler to ensure we respect 5 pages per domain
original_bfs = """    def bfs_extract(self, start_url):
        \"\"\"
        Breadth-First Search extraction
        \"\"\"
        queue = deque([(start_url, 0)])
        base = urllib.parse.urlparse(start_url).netloc
        gathered = []

        while queue:
            cur_url, depth = queue.popleft()
            
            if cur_url in self.visited:
                continue
            
            self.visited.add(cur_url)

            if depth > self.max_depth:
                break
            
            if self.pages_crawled >= self.max_pages:
                logger.info("Hit max pages limit, stopping BFS.")
                break

            logger.info(f"Crawling {cur_url} (depth={depth})")"""

updated_bfs = """    def bfs_extract(self, start_url):
        \"\"\"
        Breadth-First Search extraction
        Limited to 5 pages per domain for efficiency
        \"\"\"
        queue = deque([(start_url, 0)])
        base = urllib.parse.urlparse(start_url).netloc
        gathered = []
        # Track pages crawled per domain
        domain_pages = {base: 0}

        while queue:
            cur_url, depth = queue.popleft()
            
            if cur_url in self.visited:
                continue
            
            self.visited.add(cur_url)

            if depth > self.max_depth:
                break
            
            # Check overall page limit
            if self.pages_crawled >= self.max_pages:
                logger.info("Hit max pages limit, stopping BFS.")
                break
                
            # Check domain-specific page limit
            cur_domain = urllib.parse.urlparse(cur_url).netloc
            if cur_domain in domain_pages and domain_pages[cur_domain] >= 5:
                logger.info(f"Hit 5 page limit for domain {cur_domain}, skipping.")
                continue

            logger.info(f"Crawling {cur_url} (depth={depth})")"""

# Replace the BFS extract method
updated_content = updated_content.replace(original_bfs, updated_bfs)

# Update domain page tracking in the fetch_page area
original_fetch = """            if not html:
                continue

            text, links = self.extract_text_and_links(html, cur_url)
            
            if text:
                gathered.append(text)"""

updated_fetch = """            if not html:
                continue

            text, links = self.extract_text_and_links(html, cur_url)
            
            if text:
                gathered.append(text)
                
            # Update domain page count
            cur_domain = urllib.parse.urlparse(cur_url).netloc
            if cur_domain in domain_pages:
                domain_pages[cur_domain] += 1
            else:
                domain_pages[cur_domain] = 1"""

# Replace the fetch section
updated_content = updated_content.replace(original_fetch, updated_fetch)

# Update the main function to mention the 5-page limit
original_main = """    crawler = QuantumUniversalCrawler(topic=topic, max_depth=2, max_pages=20)"""
updated_main = """    crawler = QuantumUniversalCrawler(topic=topic, max_depth=2, max_pages=5)"""

# Replace in the main function
updated_content = updated_content.replace(original_main, updated_main)

# Write the updated content back to the file
with open("quantum_universal_crawler.py", "w") as f:
    f.write(updated_content)
    print("Updated crawler script saved to quantum_universal_crawler.py")

print("Update completed. The crawler now limits to 5 pages per domain.")
