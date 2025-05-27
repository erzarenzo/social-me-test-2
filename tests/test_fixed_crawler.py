from quantum_universal_crawler import QuantumUniversalCrawler

# Test with a single URL as a string
topic = "Artificial Intelligence"
url = "https://en.wikipedia.org/wiki/Artificial_intelligence"

print(f"Creating crawler with topic: {topic}")
crawler = QuantumUniversalCrawler(topic=topic)
print("Successfully created crawler instance")
print(f"Attempting to crawl: {url}")

result = crawler.crawl(url)
print("Crawl completed")
print(f"Result length: {len(result)} characters")
print(f"First 200 characters: {result[:200]}")
