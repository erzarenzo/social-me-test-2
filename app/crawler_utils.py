"""
Crawler utilities to extend the QuantumUniversalCrawler functionality.
These helper methods provide topic extraction, key insights extraction, 
and supporting data extraction capabilities for the article generation workflow.
"""

import re
from typing import Dict, List, Any, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("crawler_utils")

def extract_topics(crawler, content: str, main_topic: str) -> List[str]:
    """
    Extract key topics from the content, related to the main topic
    """
    if not content or len(content) < 100:
        return [main_topic]
    
    # Simple topic extraction based on frequency and relevance to main topic
    paragraphs = content.split('\n\n')
    # Use the crawler's existing relevance scorer 
    relevance_scorer = crawler.relevance_scorer
    
    # Track potential topics
    potential_topics = {}
    
    # Process each paragraph
    for paragraph in paragraphs:
        # Skip short paragraphs
        if len(paragraph) < 50:
            continue
            
        # Find potential topic phrases (2-3 word phrases)
        words = paragraph.split()
        for i in range(len(words) - 2):
            phrase2 = f"{words[i]} {words[i+1]}".lower()
            phrase3 = f"{phrase2} {words[i+2]}".lower() if i+2 < len(words) else ""
            
            # Skip common words and phrases
            if any(common in phrase2.lower() for common in ['the', 'and', 'that', 'this', 'with', 'from']):
                continue
                
            # Score the phrases
            score2 = relevance_scorer.score_paragraph(phrase2)
            if score2 > 0.3:
                potential_topics[phrase2] = potential_topics.get(phrase2, 0) + score2
                
            if phrase3:
                score3 = relevance_scorer.score_paragraph(phrase3)
                if score3 > 0.4:  # Higher threshold for 3-word phrases
                    potential_topics[phrase3] = potential_topics.get(phrase3, 0) + score3
    
    # Sort topics by score
    sorted_topics = sorted(potential_topics.items(), key=lambda x: x[1], reverse=True)
    
    # Prepare the final topics list
    topics = [main_topic]  # Always include the main topic
    
    # Add up to 4 additional topics
    for topic, _ in sorted_topics[:4]:
        # Only add if it's not too similar to existing topics
        if all(not _topics_similar(topic, existing) for existing in topics):
            # Capitalize each word properly
            topics.append(" ".join(word.capitalize() for word in topic.split()))
    
    return topics

def _topics_similar(topic1: str, topic2: str) -> bool:
    """Check if two topics are semantically similar"""
    # Simple implementation - check word overlap
    words1 = set(topic1.lower().split())
    words2 = set(topic2.lower().split())
    
    # If one is a subset of the other, they're similar
    if words1.issubset(words2) or words2.issubset(words1):
        return True
        
    # Check overlap percentage
    overlap = len(words1.intersection(words2))
    min_size = min(len(words1), len(words2))
    
    return min_size > 0 and overlap / min_size > 0.5

def extract_key_insights(crawler, content: str, topic: str) -> List[str]:
    """
    Extract key insights from the content related to the topic
    """
    if not content or len(content) < 100:
        return ["No insights found in the provided content"]
    
    # Split into paragraphs for analysis
    paragraphs = content.split('\n\n')
    relevance_scorer = crawler.relevance_scorer
    
    # Score paragraphs by relevance
    scored_paragraphs = [(p, relevance_scorer.score_paragraph(p)) for p in paragraphs if len(p) > 80]
    
    # Sort by relevance score
    sorted_paragraphs = sorted(scored_paragraphs, key=lambda x: x[1], reverse=True)
    
    # Extract insights from the most relevant paragraphs
    insights = []
    
    for paragraph, score in sorted_paragraphs[:10]:  # Consider top 10 paragraphs
        if score < 0.2:  # Skip low relevance paragraphs
            continue
            
        # Extract sentences
        sentences = re.split(r'(?<=[.!?])\s+', paragraph)
        
        for sentence in sentences:
            # Look for insightful sentences (statements, facts, conclusions)
            if len(sentence) > 40 and len(sentence) < 160:
                # Skip sentences that don't end properly or are questions
                if not sentence.endswith(('.', '!')) or sentence.endswith('?'):
                    continue
                    
                # Skip sentences with first-person pronouns
                if re.search(r'\b(I|we|our|my)\b', sentence, re.IGNORECASE):
                    continue
                    
                # Add insight if it passes filters
                insights.append(sentence.strip())
                
            # Stop if we have enough insights
            if len(insights) >= 5:
                break
                
        if len(insights) >= 5:
            break
    
    # Return unique insights
    unique_insights = []
    for insight in insights:
        if not any(_text_similarity(insight, existing) > 0.6 for existing in unique_insights):
            unique_insights.append(insight)
    
    # If no insights found, provide a fallback
    if not unique_insights:
        return ["No clear insights found in the provided content"]
    
    return unique_insights[:5]  # Return up to 5 insights

def _text_similarity(text1: str, text2: str) -> float:
    """Calculate simple text similarity score"""
    words1 = set(re.findall(r'\b\w+\b', text1.lower()))
    words2 = set(re.findall(r'\b\w+\b', text2.lower()))
    
    if not words1 or not words2:
        return 0.0
    
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union)

def extract_supporting_data(crawler, content: str, topic: str) -> Dict[str, List[str]]:
    """
    Extract supporting data (statistics, case studies, quotes) from the content
    """
    if not content or len(content) < 100:
        return {
            "statistics": [], 
            "case_studies": [],
            "quotes": []
        }
    
    # Initialize result structure
    result = {
        "statistics": [],
        "case_studies": [],
        "quotes": []
    }
    
    # Find statistics (sentences with numbers, percentages, etc.)
    statistics_patterns = [
        r'\b\d+%\b',  # Percentages
        r'\b\d+\s*out of\s*\d+\b',  # X out of Y
        r'\b\d+\s*times\b',  # X times
        r'\b\d+\s*million\b',  # X million
        r'\b\d+\s*billion\b',  # X billion
        r'\bincreased by\s*\d+\b',  # increased by X
        r'\bdecreased by\s*\d+\b',  # decreased by X
    ]
    
    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', content)
    
    # Find statistics
    for sentence in sentences:
        if any(re.search(pattern, sentence) for pattern in statistics_patterns):
            # Clean up the sentence
            clean_sentence = sentence.strip()
            if clean_sentence and len(clean_sentence) > 20 and len(clean_sentence) < 150:
                if not any(_text_similarity(clean_sentence, existing) > 0.5 for existing in result["statistics"]):
                    result["statistics"].append(clean_sentence)
    
    # Find case studies (paragraphs mentioning companies, examples, case studies)
    case_study_patterns = [
        r'\bcase study\b',
        r'\bexample of\b',
        r'\bsuccess story\b',
        r'\bimplemented by\b',
        r'\b(company|organization)\s+\w+\b'
    ]
    
    paragraphs = content.split('\n\n')
    for paragraph in paragraphs:
        if any(re.search(pattern, paragraph, re.IGNORECASE) for pattern in case_study_patterns):
            # Summarize the paragraph
            summary = " ".join(paragraph.split()[:20]) + "..."
            if summary and len(summary) > 30:
                result["case_studies"].append(summary)
    
    # Find quotes (text in quotation marks)
    quotes = re.findall(r'"([^"]+)"', content)
    for quote in quotes:
        if 20 < len(quote) < 150:
            result["quotes"].append(quote)
    
    # Limit each category to 3 items
    for key in result:
        result[key] = result[key][:3]
    
    return result
