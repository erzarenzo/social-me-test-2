#!/usr/bin/env python3
import requests
import json
import time
import sys

# Base URL - change if needed
BASE_URL = "http://localhost:8003"

# Session to maintain cookies across requests
session = requests.Session()

def save_to_file(data, filename):
    """Save data to a file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if isinstance(data, dict) or isinstance(data, list):
                json.dump(data, f, indent=2)
            else:
                f.write(str(data))
        print(f"Data saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving to {filename}: {e}")
        return False

def extract_crawled_data():
    """Extract and save crawled data"""
    print("Extracting crawled data...")
    
    # Add some sample sources first
    sources = [
        {"url": "https://techcrunch.com/category/artificial-intelligence/", "type": "news"},
        {"url": "https://www.linkedin.com/in/andrew-ng-stanford/", "type": "linkedin"},
        {"url": "https://twitter.com/ylecun", "type": "twitter"}
    ]
    
    for source in sources:
        session.post(
            f"{BASE_URL}/add-source", 
            data={"source_url": source["url"], "source_type": source["type"]}
        )
    
    # Crawl and analyze
    response = session.post(f"{BASE_URL}/crawl-and-analyze")
    
    if response.status_code == 200:
        crawled_data = response.json()
        save_to_file(crawled_data, "crawled_data.txt")
        return crawled_data
    else:
        print(f"Error extracting crawled data: {response.status_code}")
        print(response.text[:200])
        return None

def extract_tone_analysis():
    """Extract and save tone analysis"""
    print("Extracting tone analysis...")
    
    # Sample text for analysis
    sample_text = """
    The Evolution of Artificial Intelligence: From Rule-Based Systems to Deep Learning
    
    Artificial intelligence has undergone a remarkable transformation over the past few decades. What began as simple rule-based expert systems has evolved into sophisticated neural networks capable of recognizing patterns, understanding natural language, and even generating creative content.
    
    The early days of AI were characterized by symbolic approaches, where human experts would encode knowledge as explicit rules. These systems excelled at well-defined tasks but struggled with ambiguity and couldn't learn from experience. The limitations became apparent in the 1980s, leading to what's known as the "AI winter" - a period of reduced funding and interest.
    
    The renaissance of AI began with the resurgence of machine learning in the 1990s and early 2000s. Rather than hard-coding rules, these systems learned patterns from data. Support Vector Machines and Random Forests became popular for classification tasks, while recommendation systems began to appear in e-commerce platforms.
    
    The true breakthrough came with deep learning, particularly after 2012 when AlexNet demonstrated the power of convolutional neural networks for image recognition. Suddenly, AI systems could outperform humans at specific perceptual tasks. The development of architectures like recurrent neural networks and transformers further expanded capabilities into language processing, leading to models like GPT and BERT.
    
    Today, we're witnessing the emergence of multimodal AI systems that can process and generate content across different formats - text, images, audio, and video. These systems are increasingly integrated into our daily lives, from voice assistants to content recommendation engines.
    
    The future of AI likely involves more sophisticated reasoning capabilities, better alignment with human values, and increased transparency in how decisions are made. As these systems become more powerful, ensuring they remain beneficial, safe, and accessible becomes a critical societal challenge.
    """
    
    response = session.post(
        f"{BASE_URL}/analyze-content",
        data={"type": "text", "content": sample_text}
    )
    
    if response.status_code == 200:
        tone_analysis = response.json()
        save_to_file(tone_analysis, "tone_analysis.txt")
        return tone_analysis
    else:
        print(f"Error extracting tone analysis: {response.status_code}")
        print(response.text[:200])
        return None

def extract_generated_article():
    """Extract and save generated article"""
    print("Extracting generated article...")
    
    # Set up content strategy
    strategy = {
        "primary_topic": "The Future of AI in Healthcare",
        "content_focus": "How AI is transforming medical diagnostics, treatment planning, and patient care",
        "target_audience": "Healthcare professionals, technology leaders, and policy makers"
    }
    
    session.post(
        f"{BASE_URL}/save-strategy",
        json=strategy,
        headers={"Content-Type": "application/json"}
    )
    
    # Generate article
    response = session.post(
        f"{BASE_URL}/generate-article",
        data={"generator_type": "advanced"}
    )
    
    if response.status_code == 200:
        article_data = response.json()
        save_to_file(article_data, "generated_article.txt")
        
        # Extract just the article text for easier reading
        if article_data.get('success') and article_data.get('article'):
            article = article_data['article']
            article_text = f"""
TITLE: {article.get('title', 'No Title')}

SUBTITLE: {article.get('subtitle', 'No Subtitle')}

INTRODUCTION:
{article.get('introduction', 'No Introduction')}

CONTENT:
"""
            if article.get('sections'):
                for i, section in enumerate(article.get('sections')):
                    article_text += f"\n--- SECTION {i+1} ---\n"
                    article_text += f"Heading: {section.get('heading', 'No Heading')}\n"
                    article_text += f"{section.get('content', 'No Content')}\n"
            
            article_text += f"""
CONCLUSION:
{article.get('conclusion', 'No Conclusion')}
"""
            save_to_file(article_text, "article_text.txt")
        
        return article_data
    else:
        print(f"Error generating article: {response.status_code}")
        print(response.text[:200])
        return None

def main():
    """Extract all workflow data"""
    print("EXTRACTING WORKFLOW DATA")
    print("=======================\n")
    
    # Initialize session
    session.get(f"{BASE_URL}/")
    
    # Extract data
    crawled_data = extract_crawled_data()
    tone_analysis = extract_tone_analysis()
    article_data = extract_generated_article()
    
    print("\nEXTRACTION COMPLETE")
    print("==================")
    print("Files created:")
    print("1. crawled_data.txt - Raw data from sources")
    print("2. tone_analysis.txt - Writing style analysis")
    print("3. generated_article.txt - Full article data (JSON)")
    print("4. article_text.txt - Formatted article text (readable)")

if __name__ == "__main__":
    main()
