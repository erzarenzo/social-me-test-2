#!/usr/bin/env python3
"""
Connects the LLM capability to the article generator.
This enhances the improved_article_generator.py by adding
Claude API-powered paragraph and section generation.
"""

import os
import logging
import anthropic
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)
logger = logging.getLogger("SocialMeLLM")

class SocialMeLLM:
    """Handles LLM operations for the SocialMe article generator."""
    
    def __init__(self):
        """Initialize the LLM integration."""
        # Get API key from environment
        self.api_key = os.getenv('ANTHROPIC_API_KEY', '').strip()
        
        if not self.api_key or not self.api_key.startswith('sk-ant-'):
            logger.error("Invalid API key format or missing API key")
            raise ValueError("Invalid or missing Anthropic API key. Check your .env file.")
        
        # Initialize Anthropic client
        self.client = anthropic.Anthropic(api_key=self.api_key)
        logger.info("Anthropic API client initialized successfully")
    
    def expand_key_point(self, key_point: str, sources: List[Dict[str, Any]] = None) -> str:
        """
        Generate a paragraph that expands a key point.
        
        Args:
            key_point: The key point to expand
            sources: Relevant source information
            
        Returns:
            A generated paragraph
        """
        # Create source context
        source_context = ""
        if sources and len(sources) > 0:
            relevant_sources = []
            for source in sources:
                if "content" in source and source["content"]:
                    # Add a preview of relevant source content
                    snippet = source["content"][:300].replace("\n", " ").strip()
                    relevant_sources.append(f"Source: {snippet}...")
            
            if relevant_sources:
                source_context = "\n\nHere is some relevant information from sources:\n" + "\n".join(relevant_sources)
        
        # Create the prompt
        prompt = (
            f'Write a thoughtful, insightful paragraph (around 150 words) that expands on this key point:\n\n'
            f'"{key_point}"\n\n'
            'The paragraph should be well-structured, informative, and engaging. '
            'Include specific examples, explanations, or evidence where relevant.'
            f'{source_context}'
        )
        
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=500,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Error generating paragraph: {e}")
            # Fallback to a basic paragraph
            return f"{key_point} This is an important consideration in today's rapidly evolving landscape, with implications for individuals, organizations, and society as a whole."
    
    def generate_section(self, heading: str, key_points: List[str], sources: List[Dict[str, Any]] = None) -> str:
        """
        Generate a complete article section.
        
        Args:
            heading: The section heading
            key_points: List of key points to cover
            sources: Relevant source information
            
        Returns:
            Generated section content
        """
        # Create source context
        source_context = ""
        if sources and len(sources) > 0:
            relevant_sources = []
            for source in sources:
                if "content" in source and source["content"]:
                    # Add a preview of relevant source content
                    snippet = source["content"][:300].replace("\n", " ").strip()
                    relevant_sources.append(f"Source: {snippet}...")
            
            if relevant_sources:
                source_context = "\n\nHere is some relevant information from sources:\n" + "\n".join(relevant_sources)
        
        # Create the prompt
        prompt = (
            f'Write a comprehensive article section with the heading "{heading}".\n\n'
            'The section should address the following key points:\n'
            + "\n".join([f"- {point}" for point in key_points]) + "\n\n"
            'The section should be well-structured with clear paragraphs, smooth transitions, and engaging content. '
            'It should be around 500-700 words in length.'
            f'{source_context}\n\n'
            'NOTE: Do not include the section heading in your response. I will add it separately.'
        )
        
        try:
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=1500,
                temperature=0.7,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Error generating section: {e}")
            # Fallback to basic content
            return "\n\n".join([f"{point}\n\nThis is an important aspect to consider in the context of {heading.lower()}." for point in key_points])

# Function to get an instance of the LLM helper
def get_llm():
    """Get an instance of the SocialMeLLM class."""
    try:
        return SocialMeLLM()
    except Exception as e:
        logger.error(f"Error initializing LLM integration: {e}")
        return None

if __name__ == "__main__":
    # Test the LLM integration
    llm = get_llm()
    if llm:
        print("Testing paragraph generation:")
        paragraph = llm.expand_key_point("AI systems are transforming traditional work environments")
        print(paragraph)
        
        print("\nTesting section generation:")
        section = llm.generate_section(
            "The Future of Work in the AI Era",
            ["How AI changes job requirements", "Skills that remain valuable", "Preparing for an AI-driven workplace"]
        )
        print(section)
    else:
        print("Failed to initialize LLM integration. Check your API key and environment.")
