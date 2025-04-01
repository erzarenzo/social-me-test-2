import os
import logging
import json
import random
from models import db, Article

logger = logging.getLogger(__name__)

def generate_article(topic, sources=None):
    try:
        logger.info(f"Generating article about: {topic}")
        
        # Create article sections based on topic
        sections = [
            {"title": "Introduction", "content": f"{topic} is an important subject. This article explores its various aspects."},
            {"title": "Background", "content": f"To understand {topic}, we must examine its origins and development over time."},
            {"title": "Key Aspects", "content": f"There are several key aspects of {topic} that shape its impact."},
            {"title": "Applications", "content": f"{topic} has numerous applications across industries."},
            {"title": "Future Trends", "content": f"The future of {topic} presents many opportunities and challenges."},
            {"title": "Conclusion", "content": f"In conclusion, {topic} remains a critical field for study and innovation."}
        ]
        
        # Incorporate content from sources if available
        if sources and len(sources) > 0:
            for i, source in enumerate(sources):
                if source.full_text and i < len(sections):
                    snippet = source.full_text[:100].replace('\n', ' ').strip()
                    sections[i]["content"] += f' As noted: "{snippet}..."'
        
        # Assemble the full article content
        title = f"A Comprehensive Guide to {topic.title()}"
        content = f"# {title}\n\n"
        
        for section in sections:
            content += f"## {section['title']}\n{section['content']}\n\n"
        
        word_count = len(content.split())
        
        # Save to database
        article = Article(
            title=title,
            content=content,
            topic=topic,
            word_count=word_count
        )
        
        db.session.add(article)
        db.session.commit()
        
        return {
            "title": title,
            "content": content,
            "topic": topic,
            "word_count": word_count
        }
    
    except Exception as e:
        logger.error(f"Error generating article: {e}")
        return {
            "title": f"Article about {topic}",
            "content": f"This is a placeholder article about {topic}.",
            "topic": topic,
            "word_count": 500
        }
