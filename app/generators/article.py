"""
Article Generator Service

This module provides article generation functionality using LLM integration.
It generates comprehensive articles based on content sources, tone analysis, and content strategy.
"""

import logging
import json
import os
from typing import Dict, List, Any, Optional
import anthropic

logger = logging.getLogger(__name__)

class ArticleGenerator:
    """
    Article Generator creates high-quality articles using advanced LLM techniques.
    
    This service component combines content sources, tone analysis, and content strategy
    to generate comprehensive articles tailored to specific requirements.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Article Generator with API key for LLM services.
        
        Args:
            api_key: API key for Anthropic Claude or other LLM services
        """
        try:
            # Use provided API key or get from environment
            self.api_key = api_key or os.environ.get('CLAUDE_API_KEY')
            
            if not self.api_key:
                logger.warning("No API key provided for Claude. Using simulated generation.")
                self.client = None
            else:
                logger.info("Claude client initialized successfully")
                self.client = anthropic.Anthropic(api_key=self.api_key)
            
        except Exception as e:
            logger.error(f"Error initializing ArticleGenerator: {str(e)}")
            self.client = None
    
    def generate_article(self, 
                         topic: str, 
                         style_profile: Dict[str, Any],
                         source_material: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate a complete article based on the provided parameters.
        
        Args:
            topic: The main topic for the article
            style_profile: Dictionary containing style and tone parameters from neural tone analysis
            source_material: List of dictionaries containing source content and metadata
            
        Returns:
            Dictionary containing the generated article and metadata
        """
        try:
            # Log the generation request
            logger.info(f"Generating article on topic: {topic}")
            logger.info(f"Using {len(source_material)} source materials")
            
            # Format the prompt for article generation
            prompt = self._format_generation_prompt(topic, style_profile, source_material)
            
            # Generate the article content
            if self.client:
                # Use Claude API for generation
                article_content = self._generate_with_claude(prompt)
            else:
                # Use simulated generation for testing
                article_content = self._simulate_article_generation(topic, style_profile, source_material)
            
            # Process and format the article
            article = self._process_article(article_content, topic)
            
            # Add metadata
            article['metadata'] = {
                'topic': topic,
                'word_count': len(article['content'].split()),
                'source_count': len(source_material),
                'generation_method': 'claude' if self.client else 'simulation'
            }
            
            logger.info(f"Article generation complete. Word count: {article['metadata']['word_count']}")
            return article
            
        except Exception as e:
            logger.error(f"Error generating article: {str(e)}")
            return {
                'status': 'error',
                'message': f'Error generating article: {str(e)}',
                'title': f'Error generating article on {topic}',
                'content': '',
                'metadata': {'error': str(e), 'topic': topic}
            }
    
    def _format_generation_prompt(self, 
                                 topic: str, 
                                 style_profile: Dict[str, Any],
                                 source_material: List[Dict[str, Any]]) -> str:
        """
        Format a prompt for article generation based on the provided parameters.
        
        Args:
            topic: The main topic for the article
            style_profile: Dictionary containing style and tone parameters
            source_material: List of dictionaries containing source content and metadata
            
        Returns:
            Formatted prompt string for LLM article generation
        """
        # Extract key style elements for the prompt
        voice_character = style_profile.get('voice_character', {})
        linguistic_patterns = style_profile.get('linguistic_patterns', {})
        content_architecture = style_profile.get('content_architecture', {})
        implementation_guidelines = style_profile.get('implementation_guidelines', {})
        
        # Extract key information from source materials
        source_excerpts = []
        key_insights = []
        
        for source in source_material:
            if 'content' in source and source.get('relevance_score', 0) > 0.5:
                # Truncate content to manageable size
                content = source['content'][:2000] if len(source['content']) > 2000 else source['content']
                source_excerpts.append(f"Source ({source.get('title', 'Untitled')}):\n{content}\n")
            
            if 'insights' in source:
                key_insights.extend(source['insights'][:5])
        
        # Format the do's and don'ts from implementation guidelines
        dos = "\n".join([f"- {do_item}" for do_item in implementation_guidelines.get('do', [])])
        donts = "\n".join([f"- {dont_item}" for dont_item in implementation_guidelines.get('dont', [])])
        
        # Build the prompt
        prompt = f"""
        Please write a comprehensive, high-quality article on the topic of "{topic}".
        
        ## Article Requirements:
        - Create a compelling, professional 4000-word article
        - Format with markdown headings, subheadings, bullet points where appropriate
        - Include an engaging introduction and conclusion
        - Break the content into logical sections with clear headings
        - Include at least 5-7 main sections covering different aspects of the topic
        
        ## Writing Style:
        - Primary tone: {voice_character.get('primary_tone', 'professional')}
        - Style description: {voice_character.get('description', 'Clear, professional, and informative')}
        - Sentence structure: {linguistic_patterns.get('sentence_structure', 'Balanced sentences with moderate complexity')}
        - Content structure: {content_architecture.get('recommended_structure', 'Balanced structure with clear introduction, body, and conclusion')}
        
        ## Writing Guidelines:
        Do:
        {dos}
        
        Don't:
        {donts}
        
        ## Key Insights to Include:
        {chr(10).join([f"- {insight}" for insight in key_insights[:10]])}
        
        ## Source Material Excerpts:
        {chr(10).join(source_excerpts[:5])}
        
        Please create a complete, polished article that could be published immediately. Include a compelling title.
        """
        
        return prompt
    
    def _generate_with_claude(self, prompt: str) -> str:
        """
        Generate article content using Claude API.
        
        Args:
            prompt: The formatted prompt for article generation
            
        Returns:
            Generated article content
        """
        try:
            logger.info("Generating article with Claude API")
            
            # Call the Claude API
            response = self.client.messages.create(
                model="claude-3-opus-20240229",
                max_tokens=12000,
                temperature=0.7,
                system="You are an expert content writer specializing in creating comprehensive, high-quality articles. Your task is to write a well-structured, informative article based on the provided instructions and source materials.",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract and return the generated content
            content = response.content[0].text
            logger.info(f"Claude generation complete: {len(content)} characters")
            return content
            
        except Exception as e:
            logger.error(f"Error with Claude API: {str(e)}")
            raise
    
    def _simulate_article_generation(self, 
                                    topic: str, 
                                    style_profile: Dict[str, Any],
                                    source_material: List[Dict[str, Any]]) -> str:
        """
        Simulate article generation for testing without API calls.
        
        Args:
            topic: The main topic for the article
            style_profile: Dictionary containing style and tone parameters
            source_material: List of dictionaries containing source content and metadata
            
        Returns:
            Simulated article content
        """
        logger.info("Using simulated article generation")
        
        # Generate a simulated article with appropriate length and structure
        sections = [
            f"# The Complete Guide to {topic}",
            f"\n## Introduction\n\nIn today's rapidly evolving landscape, understanding {topic} has become increasingly important. This comprehensive guide explores the key aspects of {topic}, providing insights and practical applications based on current research and best practices.",
            f"\n## Understanding the Fundamentals of {topic}\n\nBefore diving into advanced concepts, it's essential to establish a solid foundation of the core principles behind {topic}. This section explores the fundamental concepts that form the building blocks of our understanding.",
            f"\n## Key Components and Considerations\n\nThe field of {topic} encompasses several critical components that work together to create effective solutions. Each component plays a vital role in the overall system and deserves careful consideration.",
            f"\n## Best Practices for Implementation\n\nImplementing {topic} effectively requires attention to detail and adherence to established best practices. The following guidelines will help ensure successful integration and optimal results.",
            f"\n## Common Challenges and Solutions\n\nEvery implementation of {topic} comes with its own set of challenges. This section addresses the most common obstacles and provides practical solutions based on industry experience.",
            f"\n## Future Trends and Developments\n\nThe landscape of {topic} continues to evolve rapidly. Staying ahead of emerging trends is crucial for maintaining competitive advantage and maximizing potential benefits.",
            f"\n## Case Studies and Real-World Applications\n\nExamining real-world applications provides valuable insights into the practical implementation of {topic}. The following case studies highlight successful approaches and their outcomes.",
            f"\n## Conclusion\n\nAs we've explored throughout this comprehensive guide, {topic} represents a significant opportunity for those who understand its nuances and can effectively implement its principles. By following the guidelines and best practices outlined in this article, you'll be well-positioned to leverage the full potential of {topic} in your specific context."
        ]
        
        # Simulate paragraphs for each section (3-5 paragraphs per section)
        content = []
        for section in sections:
            content.append(section)
            
            # Skip generating paragraphs for the title
            if section.startswith("# "):
                continue
                
            # Generate 3-5 paragraphs for this section
            num_paragraphs = min(5, max(3, hash(section) % 5 + 3))
            
            for _ in range(num_paragraphs):
                # Generate paragraph of 3-6 sentences
                num_sentences = min(6, max(3, hash(section + str(_)) % 6 + 3))
                paragraph = []
                
                for s in range(num_sentences):
                    # Incorporate some source material if available
                    if source_material and hash(section + str(_) + str(s)) % 3 == 0:
                        source_idx = hash(section + str(_) + str(s)) % len(source_material)
                        if 'content' in source_material[source_idx]:
                            source_content = source_material[source_idx]['content']
                            # Extract a random sentence-like chunk from source
                            start = hash(section + str(_) + str(s)) % max(1, len(source_content) - 100)
                            chunk = source_content[start:start+100].split('.')
                            if chunk:
                                paragraph.append(chunk[0] + '.')
                                continue
                    
                    # Otherwise generate a generic sentence
                    sentence_templates = [
                        f"Research indicates that {topic} has significant implications for various applications.",
                        f"Experts in the field recommend a structured approach to implementing {topic}.",
                        f"Understanding the core principles of {topic} is essential for success.",
                        f"Several factors contribute to the effectiveness of {topic} in real-world scenarios.",
                        f"Analyzing the impact of {topic} requires consideration of multiple variables.",
                        f"The evolution of {topic} has been shaped by technological advancements and changing needs.",
                        f"Practical implementation of {topic} often differs from theoretical understanding.",
                        f"Organizations that successfully leverage {topic} typically follow established guidelines.",
                        f"The relationship between {topic} and related disciplines continues to evolve.",
                        f"Measuring the success of {topic} implementations requires defined metrics and evaluation methods."
                    ]
                    
                    sentence_idx = hash(section + str(_) + str(s)) % len(sentence_templates)
                    paragraph.append(sentence_templates[sentence_idx])
                
                content.append("\n" + " ".join(paragraph))
        
        return "\n".join(content)
    
    def _process_article(self, content: str, topic: str) -> Dict[str, Any]:
        """
        Process and format the generated article content.
        
        Args:
            content: The raw generated article content
            topic: The main topic of the article
            
        Returns:
            Dictionary containing the processed article with title and content
        """
        # Extract title from content if present, otherwise create one
        lines = content.strip().split('\n')
        
        if lines and lines[0].startswith('# '):
            title = lines[0].replace('# ', '')
            content_without_title = '\n'.join(lines[1:])
        else:
            title = f"Comprehensive Guide to {topic}"
            content_without_title = content
        
        # Format the article as needed
        article = {
            'title': title,
            'content': content_without_title.strip(),
            'status': 'success'
        }
        
        return article
    
    def format_output(self, raw_content: str) -> Dict[str, Any]:
        """
        Format raw content into structured output with sections.
        
        Args:
            raw_content: The raw generated content
            
        Returns:
            Dictionary containing the formatted content with sections
        """
        try:
            # Split content into sections based on markdown headings
            lines = raw_content.strip().split('\n')
            
            # Extract title (first heading)
            title = lines[0].replace('# ', '') if lines and lines[0].startswith('# ') else "Generated Article"
            
            # Process sections
            sections = []
            current_section = {"title": "", "content": []}
            
            for line in lines[1:]:  # Skip the title
                if line.startswith('## '):
                    # If we have content in the current section, add it to sections
                    if current_section["title"]:
                        current_section["content"] = '\n'.join(current_section["content"])
                        sections.append(current_section)
                    
                    # Start a new section
                    current_section = {
                        "title": line.replace('## ', ''),
                        "content": []
                    }
                else:
                    current_section["content"].append(line)
            
            # Add the last section
            if current_section["title"]:
                current_section["content"] = '\n'.join(current_section["content"])
                sections.append(current_section)
            
            return {
                "title": title,
                "sections": sections,
                "raw_content": raw_content
            }
            
        except Exception as e:
            logger.error(f"Error formatting output: {str(e)}")
            return {
                "title": "Formatting Error",
                "sections": [{"title": "Error", "content": f"Error formatting content: {str(e)}"}],
                "raw_content": raw_content
            }
