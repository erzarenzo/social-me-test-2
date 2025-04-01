from quantum_universal_crawler import QuantumUniversalCrawler
import sys

def test_simple():
    print("Initializing crawler...")
    crawler = QuantumUniversalCrawler(topic="Test")
    print("Crawler initialized. Testing fetch...")
    result = crawler.crawl("https://example.com")
    print(f"Result: {result.status}, Words: {result.word_count}")
    print(result.content[:100] + "..." if result.content else "No content")

if __name__ == "__main__":
    test_simple()
