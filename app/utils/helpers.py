"""
Utility helper functions for SocialMe platform
"""

import re
from typing import List, Dict, Any

def extract_topics(text: str, top_n: int = 5) -> List[str]:
    """
    Extract key topics from a given text
    
    Args:
        text (str): Input text to extract topics from
        top_n (int): Number of top topics to return
    
    Returns:
        List[str]: List of extracted topics
    """
    # Simple implementation using basic NLP techniques
    # In a real-world scenario, this would use more advanced NLP libraries
    
    # Remove punctuation and convert to lowercase
    cleaned_text = re.sub(r'[^\w\s]', '', text.lower())
    
    # Split into words and remove common stop words
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    words = [word for word in cleaned_text.split() if word not in stop_words]
    
    # Count word frequencies
    word_freq = {}
    for word in words:
        if len(word) > 3:  # Only consider words longer than 3 characters
            word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top N topics
    return sorted(word_freq, key=word_freq.get, reverse=True)[:top_n]

def extract_key_insights(text: str, num_insights: int = 3) -> List[str]:
    """
    Extract key insights from a given text
    
    Args:
        text (str): Input text to extract insights from
        num_insights (int): Number of insights to extract
    
    Returns:
        List[str]: List of extracted key insights
    """
    # Simple implementation of key insight extraction
    # Sentences are considered insights if they contain important keywords
    
    # Split text into sentences
    sentences = re.split(r'[.!?]', text)
    
    # Define important keywords that might indicate an insight
    insight_keywords = {
        'important', 'key', 'crucial', 'significant', 
        'fundamental', 'critical', 'essential'
    }
    
    # Score sentences based on keyword presence and length
    scored_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        # Calculate insight score
        score = sum(1 for word in sentence.lower().split() if word in insight_keywords)
        score += 1 if len(sentence.split()) > 10 else 0
        
        scored_sentences.append((sentence, score))
    
    # Sort by score and return top insights
    return [
        sentence for sentence, _ in 
        sorted(scored_sentences, key=lambda x: x[1], reverse=True)
    ][:num_insights]

def extract_supporting_data(sources: List[str]) -> Dict[str, Any]:
    """
    Extract supporting data from multiple sources
    
    Args:
        sources (List[str]): List of source URLs or text content
    
    Returns:
        Dict[str, Any]: Dictionary of extracted supporting data
    """
    # Placeholder implementation for supporting data extraction
    supporting_data = {
        "sources": sources,
        "total_sources": len(sources),
        "data_points": [],
        "metadata": {}
    }
    
    # Basic extraction logic
    for source in sources:
        # In a real implementation, this would involve web scraping or content analysis
        supporting_data["data_points"].append({
            "source": source,
            "extracted_content": f"Sample content from {source}",
            "confidence_score": 0.7
        })
    
    return supporting_data
