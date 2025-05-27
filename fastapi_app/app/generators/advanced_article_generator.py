import json
import random
import requests
import os
import logging
import re
import time
from typing import Dict, List, Any, Optional
import sys
from pathlib import Path

# Add parent directories to path to ensure imports work reliably
parent_dir = Path(__file__).parent.parent
app_dir = parent_dir.parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

# First try to use our more robust configuration system
try:
    from app.config.api_config import get_openai_api_key, get_anthropic_api_key
    OPENAI_API_KEY = get_openai_api_key()
    ANTHROPIC_API_KEY = get_anthropic_api_key()
    
    if OPENAI_API_KEY:
        os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY  # Set env var for compatibility
    if ANTHROPIC_API_KEY:
        os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY  # Set env var for compatibility

except ImportError:
    # Fallback to traditional dotenv if config module isn't available
    from dotenv import load_dotenv
    load_dotenv()

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("article_generator")

# Dynamically check dependencies
try:
    import openai
    OPENAI_AVAILABLE = True
    logger.info("OpenAI package found")
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("OpenAI package not found - some features will be limited")

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
    logger.info("Anthropic package found")
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logger.warning("Anthropic package not found - some features will be limited")

# Check for API keys - First check if they were already set by our config system
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not found in environment variables")
else:
    logger.info("OpenAI API key found and will be used for article generation")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_API_KEY:
    ANTHROPIC_API_KEY = os.getenv("CLAUDE_API_KEY")  # Check alternative name
    if ANTHROPIC_API_KEY:
        logger.info("Using CLAUDE_API_KEY for Anthropic API access")
    else:
        logger.warning("No Anthropic API key found in environment variables")
        
# Add additional safeguards for key validity
def is_valid_api_key(key, provider="openai"):
    """Check if an API key appears to be valid based on standard patterns"""
    if not key or len(key) < 10:  # Basic length check
        return False
        
    # OpenAI keys typically start with 'sk-'
    if provider == "openai" and key.startswith("sk-"):
        return True
    # Anthropic keys typically start with 'sk-ant-'
    elif provider == "anthropic" and key.startswith("sk-ant-"):
        return True
    # Conservative fallback - consider it potentially valid if it seems complex enough
    elif len(key) >= 20 and any(c.isdigit() for c in key) and any(c.isalpha() for c in key):
        logger.warning(f"Using API key with non-standard format for {provider}")
        return True
        
    logger.error(f"Invalid {provider} API key format detected")
    return False

# Validate keys
OPENAI_KEY_VALID = is_valid_api_key(OPENAI_API_KEY, "openai")
ANTHROPIC_KEY_VALID = is_valid_api_key(ANTHROPIC_API_KEY, "anthropic")

class FallbackArticleGenerator:
    """
    Fallback article generator for when LLM APIs are unavailable or fail
    """
    def __init__(self, topic: str, source_material: Optional[List[Dict]] = None, 
                 target_word_count: int = 4000, tone_profile: Optional[Dict] = None):
        """Initialize with given parameters"""
        self.topic = topic
        self.source_material = source_material or []
        self.target_word_count = target_word_count
        self.tone_profile = tone_profile or {}
        logger.info(f"Initialized FallbackArticleGenerator for topic: {topic}")
    
    def generate_article(self) -> Dict[str, Any]:
        """Generate a template-based article without API calls"""
        logger.info(f"Generating fallback article for topic: {self.topic}")
        
        # Create article structure
        article = {
            "title": f"The Complete Guide to {self.topic}",
            "text": self._generate_article_text(),
            "word_count": 0,  # Will be calculated later
            "sources_used": len(self.source_material),
            "fallback_activated": True,
            "provider": "fallback"
        }
        
        # Calculate word count
        article["word_count"] = len(article["text"].split())
        
        return article
    
    def _generate_article_text(self) -> str:
        """Generate the article text content"""
        # Create a well-structured article with markdown
        content = f"# The Complete Guide to {self.topic}\n\n"
        
        # Create an introduction
        content += "## Introduction\n\n"
        content += f"{self.topic} is a significant area with important implications across various domains. "
        content += "This comprehensive guide examines key aspects, applications, challenges, and future directions "
        content += f"of {self.topic}, providing insights for researchers, practitioners, and enthusiasts alike.\n\n"
        
        # Generate sections based on common article structure
        sections = [
            f"Understanding {self.topic}",
            f"Historical Development of {self.topic}",
            f"Key Concepts in {self.topic}",
            f"Core Components of {self.topic}",
            f"Applications of {self.topic}",
            f"Current Challenges in {self.topic}",
            f"Best Practices for {self.topic}",
            f"Case Studies in {self.topic}",
            f"Future Directions for {self.topic}",
            f"Ethical Considerations in {self.topic}"
        ]
        
        # Add each section with template content
        for section in sections:
            content += f"## {section}\n\n"
            content += f"This section explores {section.lower()} in detail. "
            
            # Add paragraph 1
            content += f"The field of {self.topic} has seen significant developments in this area. "
            content += f"Understanding {section.lower()} provides crucial insights into the broader landscape. "
            content += "Various approaches and methodologies have emerged, each with distinct advantages and limitations.\n\n"
            
            # Add paragraph 2
            content += f"Research in {section.lower()} has revealed important patterns and principles. "
            content += "These findings have implications for both theory and practice, informing decision-making "
            content += f"and strategy development across the {self.topic} ecosystem. Further investigation continues "
            content += "to refine our understanding and open new possibilities for innovation.\n\n"
        
        # Add conclusion
        content += "## Conclusion\n\n"
        content += f"In conclusion, {self.topic} represents a dynamic and evolving field with profound implications "
        content += "for technology, industry, and society. The concepts, applications, and challenges examined in "
        content += "this guide illustrate the complexity and potential of this domain. As research and development "
        content += f"continue to advance, {self.topic} will likely play an increasingly important role in shaping "
        content += "our future landscape and addressing key challenges of our time.\n\n"
        
        return content

class ArticleGenerator:
    """
    Advanced article generator using OpenAI and Anthropic APIs with fallback mechanisms
    """
    def __init__(self, openai_api_key=None, anthropic_api_key=None):
        """Initialize with API keys"""
        self.openai_api_key = openai_api_key or OPENAI_API_KEY
        self.anthropic_api_key = anthropic_api_key or ANTHROPIC_API_KEY
        self.openai_client = None
        self.anthropic_client = None
        self.logger = logger
        
        # Initialize OpenAI client (primary)
        if OPENAI_AVAILABLE and self.openai_api_key:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=self.openai_api_key)
                self.logger.info("OpenAI client initialized successfully")
            except Exception as e:
                self.logger.error(f"Error initializing OpenAI client: {e}")
        
        # Initialize Anthropic client (secondary/fallback)
        if ANTHROPIC_AVAILABLE and self.anthropic_api_key:
            try:
                from anthropic import Anthropic
                self.anthropic_client = Anthropic(api_key=self.anthropic_api_key)
                self.logger.info("Anthropic client initialized successfully")
            except Exception as e:
                self.logger.error(f"Error initializing Anthropic client: {e}")
        
        # Check if we have at least one client
        if not self.openai_client and not self.anthropic_client:
            self.logger.warning("No LLM clients available - will use fallback generator")
    
    def generate_article(self, topic: str, style_profile: Dict = None, source_material: List[Dict] = None) -> Dict:
        """Generate a complete article"""
        # Initialize parameters
        style_profile = style_profile or {}
        source_material = source_material or []
        
        self.logger.info(f"Generating article for topic: {topic}")
        
        try:
            # Prepare source material for use in prompts
            prepared_sources = self._prepare_source_material(source_material)
            
            # Create article structure with sections
            structure = self._create_article_structure(topic, prepared_sources)
            
            # Generate the complete article with the appropriate API
            if self.openai_client:
                try:
                    self.logger.info("Attempting to generate article with OpenAI")
                    article = self._generate_article_with_openai(topic, style_profile, prepared_sources, structure)
                    return article
                except Exception as e:
                    self.logger.warning(f"OpenAI article generation failed: {e}")
                    if self.anthropic_client:
                        try:
                            self.logger.info("Falling back to Anthropic for article generation")
                            article = self._generate_article_with_anthropic(topic, style_profile, prepared_sources, structure)
                            return article
                        except Exception as e2:
                            self.logger.error(f"Anthropic article generation failed: {e2}")
            elif self.anthropic_client:
                try:
                    self.logger.info("Attempting to generate article with Anthropic")
                    article = self._generate_article_with_anthropic(topic, style_profile, prepared_sources, structure)
                    return article
                except Exception as e:
                    self.logger.error(f"Anthropic article generation failed: {e}")
            
            # If we get here, all API attempts failed
            self.logger.warning("All API attempts failed, using fallback generator")
            fallback = FallbackArticleGenerator(topic, source_material)
            return fallback.generate_article()
            
        except Exception as e:
            self.logger.error(f"Unexpected error during article generation: {e}")
            # Ultimate fallback
            fallback = FallbackArticleGenerator(topic, source_material)
            result = fallback.generate_article()
            result["error"] = str(e)
            return result
    
    def _prepare_source_material(self, source_material: List[Dict]) -> List[Dict]:
        """Process and prepare source material for use in article generation"""
        prepared_sources = []
        for source in source_material:
            # Extract the most useful information from each source
            prepared_source = {
                "title": source.get("title", "Untitled Source"),
                "url": source.get("url", ""),
                "content": source.get("content", "")[:1500],  # Limit length to avoid token limits
                "relevance_score": source.get("relevance_score", 0.5)
            }
            prepared_sources.append(prepared_source)
        
        # Sort by relevance score (highest first)
        prepared_sources.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return prepared_sources[:5]  # Limit to top 5 sources
    
    def _create_article_structure(self, topic: str, sources: List[Dict]) -> Dict:
        """Create the article structure with sections based on the topic and sources"""
        # Extract themes/sections from sources if available
        themes = self._extract_themes(sources, topic)
        
        # Create the final structure
        structure = {
            "title": f"The Complete Guide to {topic}",
            "sections": themes,
            "target_word_count": 4000,
            "words_per_section": 4000 // (len(themes) + 2)  # +2 for intro and conclusion
        }
        
        return structure
    
    def _extract_themes(self, sources: List[Dict], topic: str) -> List[str]:
        """Extract potential themes/section topics from sources"""
        # Try OpenAI first (since we know the key is working)
        if self.openai_client:
            try:
                return self._extract_themes_with_openai(sources, topic)
            except Exception as e:
                self.logger.warning(f"OpenAI theme extraction failed: {e}")
                # Fall back to Anthropic if available
                if self.anthropic_client:
                    try:
                        return self._extract_themes_with_anthropic(sources, topic)
                    except Exception as e2:
                        self.logger.error(f"Anthropic theme extraction failed: {e2}")
        elif self.anthropic_client:
            try:
                return self._extract_themes_with_anthropic(sources, topic)
            except Exception as e:
                self.logger.error(f"Anthropic theme extraction failed: {e}")
        
        # Default themes if API extraction fails
        return [
            f"Understanding {topic}",
            f"Historical Development of {topic}",
            f"Key Concepts in {topic}",
            f"Applications of {topic}",
            f"Challenges and Limitations of {topic}",
            f"Future Directions for {topic}"
        ]
    
    def _extract_themes_with_openai(self, sources: List[Dict], topic: str) -> List[str]:
        """Extract potential themes/section topics from sources using OpenAI's API"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
        
        # Format source content for the prompt
        formatted_sources = "\n\n".join([
            f"SOURCE {i+1}: {source.get('title', 'Untitled Source')}\n{source.get('content', '')[:500]}"
            for i, source in enumerate(sources)
        ])
        
        prompt = f"""
        Based on the following sources about "{topic}", identify 6-8 main themes or sections for a comprehensive article.
        Each theme should be a concise heading (3-7 words) that would work well as a section title.
        
        SOURCES:
        {formatted_sources}
        
        INSTRUCTIONS:
        - Identify 6-8 distinct themes or topics to cover
        - Ensure the sections together provide comprehensive coverage of {topic}
        - Format each theme as a short, engaging section title (e.g., "Evolution of Smart Cities" rather than just "History")
        - Return ONLY the list of section titles, one per line with no numbering or bullets
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a skilled editor helping to structure an article outline based on source materials."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            # Extract themes from response
            themes_text = response.choices[0].message.content.strip()
            themes = [line.strip() for line in themes_text.split("\n") if line.strip()]
            
            # Ensure we have at least 4 themes
            if len(themes) < 4:
                self.logger.warning(f"OpenAI returned fewer than 4 themes, adding default themes")
                default_themes = [
                    f"Understanding {topic}",
                    f"Applications of {topic}",
                    f"Challenges in {topic}",
                    f"Future of {topic}"
                ]
                themes.extend([t for t in default_themes if t not in themes])
                themes = themes[:8]  # Limit to 8 themes
            
            return themes
            
        except Exception as e:
            self.logger.error(f"Error extracting themes with OpenAI: {e}")
            raise
    
    def _extract_themes_with_anthropic(self, sources: List[Dict], topic: str) -> List[str]:
        """Extract potential themes/section topics from sources using Anthropic's Claude API"""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")
        
        # Format source content for the prompt
        formatted_sources = "\n\n".join([
            f"SOURCE {i+1}: {source.get('title', 'Untitled Source')}\n{source.get('content', '')[:500]}"
            for i, source in enumerate(sources)
        ])
        
        prompt = f"""
        Based on the following sources about "{topic}", identify 6-8 main themes or sections for a comprehensive article.
        Each theme should be a concise heading (3-7 words) that would work well as a section title.
        
        SOURCES:
        {formatted_sources}
        
        INSTRUCTIONS:
        - Identify 6-8 distinct themes or topics to cover
        - Ensure the sections together provide comprehensive coverage of {topic}
        - Format each theme as a short, engaging section title (e.g., "Evolution of Smart Cities" rather than just "History")
        - Return ONLY the list of section titles, one per line with no numbering or bullets
        """
        
        try:
            response = self.anthropic_client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                temperature=0.7,
                system="You are a skilled editor helping to structure an article outline based on source materials.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract themes from response
            themes_text = response.content[0].text.strip()
            themes = [line.strip() for line in themes_text.split("\n") if line.strip()]
            
            # Ensure we have at least 4 themes
            if len(themes) < 4:
                self.logger.warning(f"Anthropic returned fewer than 4 themes, adding default themes")
                default_themes = [
                    f"Understanding {topic}",
                    f"Applications of {topic}",
                    f"Challenges in {topic}",
                    f"Future of {topic}"
                ]
                themes.extend([t for t in default_themes if t not in themes])
                themes = themes[:8]  # Limit to 8 themes
            
            return themes
            
        except Exception as e:
            self.logger.error(f"Error extracting themes with Anthropic: {e}")
            raise
    
    def _generate_article_with_openai(self, topic: str, style_profile: Dict, sources: List[Dict], structure: Dict) -> Dict:
        """Generate the complete article using OpenAI's API"""
        if not self.openai_client:
            raise ValueError("OpenAI client not initialized")
            
        self.logger.info(f"Generating article with OpenAI for topic: {topic}")
        
        # Format source material for the prompt
        source_content = "\n\n".join([
            f"SOURCE {i+1}: {source.get('title', 'Untitled')}\n{source.get('content', '')[:1500]}"
            for i, source in enumerate(sources[:5])
        ])
        
        # Extract the sections from the structure
        sections = structure.get("sections", [])
        sections_text = "\n".join([f"- {section}" for section in sections])
        
        # Create the prompt for article generation
        prompt = f"""
        Generate a comprehensive, well-structured article about {topic}.
        
        The article should include the following sections:
        {sections_text}
        
        Use the following source materials for reference and information:
        {source_content}
        
        The article should be approximately 3000-4000 words in total, with a balanced distribution across sections.
        The writing style should be informative, engaging, and accessible to a general audience.
        Include specific examples, data points, and references from the source materials where relevant.
        
        Format the article with clear section headings using Markdown formatting (##).
        Start with a compelling introduction, then proceed through each section, and end with a conclusion.
        """
        
        try:
            # Call OpenAI API to generate the article
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                temperature=0.7,
                messages=[
                    {"role": "system", "content": "You are an expert content writer who creates comprehensive, well-researched articles based on provided sources."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000
            )
            
            # Extract the generated content
            content = response.choices[0].message.content
            
            # Try to extract the title from the content
            title_match = re.search(r'^#\s+(.+?)\s*$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else f"The Complete Guide to {topic}"
            
            # Get the word count
            word_count = len(content.split())
            
            self.logger.info(f"Successfully generated article with OpenAI: {word_count} words")
            
            # Return the article in the expected format
            return {
                "title": title,
                "text": content,
                "word_count": word_count,
                "sources_used": len(sources),
                "fallback_activated": False,
                "provider": "openai"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating article with OpenAI: {e}")
            raise
    
    def _generate_article_with_anthropic(self, topic: str, style_profile: Dict, sources: List[Dict], structure: Dict) -> Dict:
        """Generate the complete article using Anthropic's Claude API"""
        if not self.anthropic_client:
            raise ValueError("Anthropic client not initialized")
            
        self.logger.info(f"Generating article with Anthropic for topic: {topic}")
        
        # Format source material for the prompt
        source_content = "\n\n".join([
            f"SOURCE {i+1}: {source.get('title', 'Untitled')}\n{source.get('content', '')[:1500]}"
            for i, source in enumerate(sources[:5])
        ])
        
        # Extract the sections from the structure
        sections = structure.get("sections", [])
        sections_text = "\n".join([f"- {section}" for section in sections])
        
        # Create the prompt for article generation
        prompt = f"""
        Generate a comprehensive, well-structured article about {topic}.
        
        The article should include the following sections:
        {sections_text}
        
        Use the following source materials for reference and information:
        {source_content}
        
        The article should be approximately 3000-4000 words in total, with a balanced distribution across sections.
        The writing style should be informative, engaging, and accessible to a general audience.
        Include specific examples, data points, and references from the source materials where relevant.
        
        Format the article with clear section headings using Markdown formatting (##).
        Start with a compelling introduction, then proceed through each section, and end with a conclusion.
        """
        
        try:
            # Call Anthropic API to generate the article
            response = self.anthropic_client.messages.create(
                model="claude-3-opus-20240229",  # Use Opus for highest quality
                max_tokens=4000,
                temperature=0.7,
                system="You are an expert content writer who creates comprehensive, well-researched articles based on provided sources.",
                messages=[{"role": "user", "content": prompt}]
            )
            
            # Extract the generated content
            content = response.content[0].text
            
            # Try to extract the title from the content
            title_match = re.search(r'^#\s+(.+?)\s*$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else f"The Complete Guide to {topic}"
            
            # Get the word count
            word_count = len(content.split())
            
            self.logger.info(f"Successfully generated article with Anthropic: {word_count} words")
            
            # Return the article in the expected format
            return {
                "title": title,
                "text": content,
                "word_count": word_count,
                "sources_used": len(sources),
                "fallback_activated": False,
                "provider": "anthropic"
            }
            
        except Exception as e:
            self.logger.error(f"Error generating article with Anthropic: {e}")
            raise

def generate_with_openai(topic: str, sources: Optional[List[Dict]] = None, target_word_count: int = 2000) -> Dict[str, Any]:
    """Generate an article using the OpenAI API with a sectioned approach for longer articles"""
    try:
        logging.info(f"Generating article with OpenAI for topic: {topic}")
        
        # For longer articles (>2000 words), use the sectioned approach
        if target_word_count > 2000:
            return generate_sectioned_article(topic, sources, target_word_count)
        
        # For shorter articles, use the single-prompt approach
        # Prepare the prompt
        prompt = prepare_openai_prompt(topic, sources, target_word_count)
        
        # Initialize the OpenAI client
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Generate the article
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert content writer specializing in creating comprehensive, engaging articles."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=4000  # This may need to be adjusted based on the target word count
        )
        
        # Extract and process the generated article
        article_text = response.choices[0].message.content
        
        # Parse the markdown content to extract title and text
        title_match = re.search(r'^#\s+(.+)$', article_text, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Article on {topic}"
        
        # Count words
        word_count = len(article_text.split())
        
        logging.info(f"Successfully generated article with OpenAI: {word_count} words")
        
        return {
            "title": title,
            "text": article_text,
            "word_count": word_count,
            "provider": "openai"
        }
    except Exception as e:
        logging.error(f"Error generating article with OpenAI: {str(e)}")
        raise


def prepare_openai_prompt(topic: str, sources: Optional[List[Dict]] = None, target_word_count: int = 2000) -> str:
    """Prepare the prompt for OpenAI article generation"""
    # Format sources if provided
    source_content = ""
    if sources:
        source_content = "\n\n".join([
            f"SOURCE {i+1}: {source.get('title', 'Untitled')}\n{source.get('content', '')}"
            for i, source in enumerate(sources[:5])
        ])
    
    # Create the prompt
    prompt = f"""
    Generate a comprehensive article about {topic}.
    
    The article should be approximately {target_word_count} words in length.
    Format the article with Markdown, including a title as an h1 heading (#) and appropriate section headings (##).
    
    The writing style should be informative, engaging, and accessible to a general audience.
    Include specific examples and data points where relevant.
    """
    
    # Add source material if available
    if source_content:
        prompt += f"""
        
        Use the following source materials for reference and information:
        {source_content}
        
        Incorporate relevant information from these sources into your article.
        """
    
    return prompt


def generate_sectioned_article(topic: str, sources: Optional[List[Dict]] = None, target_word_count: int = 4000) -> Dict[str, Any]:
    """Generate a longer article by breaking it into sections and combining them"""
    try:
        logging.info(f"Generating sectioned article for topic: {topic}")
        
        # Initialize the OpenAI client
        from openai import OpenAI
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        
        # Step 1: Generate article outline with sections
        logging.info("Generating article outline with sections...")
        outline_prompt = f"""
        Create a detailed outline for a comprehensive {target_word_count}-word article about {topic}.
        
        The outline should have:
        1. An engaging title
        2. An introduction
        3. 6-8 main sections with descriptive headings
        4. A conclusion
        
        For each section, provide a brief description of what it will cover.
        Format the response as a structured outline with the title at the top.
        """
        
        outline_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert content editor creating article outlines."},
                {"role": "user", "content": outline_prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        outline = outline_response.choices[0].message.content
        logging.info("Article outline generated")
        
        # Step 2: Extract sections from the outline
        import re
        
        # Extract title - look for something that says "Title:" or is presented as a heading
        title_match = re.search(r'(?:Title:\s*|^#*\s*)"?([^"\n]+)"?', outline, re.MULTILINE)
        title = title_match.group(1) if title_match else f"Comprehensive Guide to {topic}"
        title = title.strip()
        
        # Clean up title if it still contains "Title:" 
        if title.startswith("Title:"):
            title = title[6:].strip()
        
        # Extract sections - try different patterns
        sections = []
        
        # Look for patterns like "1. Introduction" or "- Introduction"
        section_patterns = [
            r'(?:^|\n)\d+\.\s+([^\n:]+)(?:\n|:)',  # Numbered sections like "1. Introduction"
            r'(?:^|\n)-\s+([^\n:]+)(?:\n|:)',       # Bulleted sections like "- Introduction"
            r'(?:^|\n)#+\s+([^\n]+)',              # Markdown headings like "## Introduction"
            r'(?:^|\n)(?:I|II|III|IV|V|VI|VII|VIII|IX|X)\.\s+([^\n:]+)'  # Roman numeral sections
        ]
        
        for pattern in section_patterns:
            found_sections = re.findall(pattern, outline, re.MULTILINE)
            if found_sections:
                # Filter out any that aren't actual section headings
                filtered_sections = [s for s in found_sections if 
                                   len(s.split()) < 10 and  # Not too long
                                   not s.lower().startswith("title") and  # Not the title
                                   not s.lower().startswith("for each")]  # Not instructions
                if filtered_sections:
                    sections = filtered_sections
                    break
        
        # If no sections found using patterns, look for capitalized single-line items that might be headings
        if not sections:
            lines = outline.split('\n')
            for line in lines:
                line = line.strip()
                if line and line[0].isupper() and len(line.split()) <= 6 and ':' not in line:
                    sections.append(line)
                    
        # Ensure we have Introduction and Conclusion sections
        has_intro = any('intro' in s.lower() for s in sections)
        has_conclusion = any('conclu' in s.lower() for s in sections)
        
        if not has_intro:
            sections.insert(0, "Introduction")
        if not has_conclusion:
            sections.append("Conclusion")
        
        logging.info(f"Found {len(sections)} sections in outline")
        logging.info(f"Article title: {title}")
        
        # Step 3: Generate content for each section
        complete_article = f"# {title}\n\n"
        section_contents = []
        total_word_count = 0
        
        for i, section in enumerate(sections):
            logging.info(f"Generating content for section {i+1}/{len(sections)}: {section}")
            
            # Select relevant source material for this section
            # Simple relevance matching based on keywords
            section_keywords = set(section.lower().split())
            relevant_sources = []
            
            if sources:
                for source in sources:
                    source_text = source.get('title', '') + ' ' + source.get('content', '')
                    source_text = source_text.lower()
                    if any(keyword in source_text for keyword in section_keywords):
                        relevant_sources.append(source)
                
                # If no relevant sources found, use all sources
                if not relevant_sources:
                    relevant_sources = sources
                    
                # Format source material
                source_content = "\n\n".join([
                    f"SOURCE {i+1}: {source.get('title', 'Untitled')}\n{source.get('content', '')[:800]}"
                    for i, source in enumerate(relevant_sources[:3])
                ])
            else:
                source_content = "No source material provided."
            
            # Calculate target words for this section (slightly more for longer sections)
            section_importance = 1.0
            if 'introduction' in section.lower() or 'conclusion' in section.lower():
                section_importance = 0.75
            target_section_words = int((target_word_count / len(sections)) * section_importance)
            
            # Generate content for this section
            section_prompt = f"""
            Write a detailed section for an article about {topic}. 
            
            The section heading is: "{section}"
            
            This section should be approximately {target_section_words} words.
            
            Use the following source materials for reference:
            {source_content}
            
            Format the content using Markdown with the section heading as a level 2 heading (##).
            Focus on depth, accuracy, and engaging writing.
            Do not conclude the section with a transition to the next section.
            """
            
            section_response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert content writer creating detailed and informative article sections."},
                    {"role": "user", "content": section_prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            section_content = section_response.choices[0].message.content
            section_contents.append(section_content)
            
            # Count words in this section
            section_word_count = len(section_content.split())
            total_word_count += section_word_count
            logging.info(f"Section {i+1} complete: {section_word_count} words")
            
            # Add a short delay to avoid rate limits
            time.sleep(1)
        
        # Step 4: Combine all sections into the complete article
        complete_article = f"# {title}\n\n"
        for section_content in section_contents:
            complete_article += section_content + "\n\n"
        
        logging.info(f"Successfully generated sectioned article with OpenAI: {total_word_count} words")
        
        return {
            "title": title,
            "text": complete_article,
            "word_count": total_word_count,
            "provider": "openai_sectioned"
        }
    except Exception as e:
        logging.error(f"Error generating sectioned article with OpenAI: {str(e)}")
        raise


def generate_advanced_article(
    topic: str,
    tone_analysis: Optional[Dict[str, Any]] = None,
    source_material: Optional[List[Dict]] = None,
    target_word_count: int = 4000
) -> Dict[str, Any]:
    """
    Generate an advanced article using available API providers with fallback options
    
    Args:
        topic (str): The primary topic for the article
        tone_analysis (Dict, optional): Style and tone parameters
        source_material (List[Dict], optional): Source materials for reference
        target_word_count (int): Target word count for the article
    
    Returns:
        Dict: The generated article with metadata
    """
    logger.info(f"Generating advanced article for topic: {topic}")
    
    try:
        # First try using the EnhancedArticleGenerator which supports detailed voice patterns
        try:
            logger.info("Attempting to use EnhancedArticleGenerator with Universal Voice Pattern")
            # Import the enhanced generator - this should be available in our codebase
            try:
                sys.path.append('/root/socialme/social-me-test-2')
                from app.enhanced_article_generator import EnhancedArticleGenerator
                logger.info("Successfully imported EnhancedArticleGenerator")
            except Exception as import_error:
                logger.error(f"Failed to import EnhancedArticleGenerator: {import_error}")
                # If import fails, we'll continue to the other methods
                raise import_error
            
            # Create the generator instance
            enhanced_generator = EnhancedArticleGenerator()
            
            # Prepare the input with proper voice pattern mapping
            article_input = {
                "topic": topic,
                "title": f"Comprehensive Guide to {topic}",
                "use_enhanced_tone": True  # Important flag to use the detailed voice pattern
            }
            
            # If we have tone_analysis data, properly map it to the voice_pattern format
            if tone_analysis and isinstance(tone_analysis, dict):
                logger.info("Mapping tone analysis data to Universal Voice Pattern format")
                
                # Log the actual tone analysis keys we received
                logger.info(f"Tone analysis keys: {tone_analysis.keys()}")
                
                # Create the voice pattern structure expected by EnhancedArticleGenerator
                voice_pattern = {}
                
                # Part 1: Persona & Positioning
                voice_pattern["PART 1: PERSONA & POSITIONING"] = {
                    "Core Identity": tone_analysis.get("writing_persona", tone_analysis.get("core_identity", "Expert knowledge source")),
                    "Key Writing Characteristics": tone_analysis.get("key_characteristics", [])
                }
                
                # Part 2: Voice & Tone Specifications
                voice_pattern["PART 2: VOICE & TONE SPECIFICATIONS"] = {
                    "Core Voice Attributes": tone_analysis.get("voice_attributes", []),
                    "Dominant Tone": tone_analysis.get("neural_tone_analysis", {}).get("tone", "informative")
                }
                
                # Part 3: Linguistic Patterns
                voice_pattern["PART 3: LINGUISTIC PATTERNS"] = {
                    "Sentence Structure": tone_analysis.get("sentence_structure", ""),
                    "Paragraph Construction": tone_analysis.get("paragraph_construction", ""),
                    "Pronoun Usage": tone_analysis.get("pronoun_usage", "")
                }
                
                # Part 5: Content Structure
                voice_pattern["PART 5: CONTENT STRUCTURE"] = {
                    "Overall Framework": tone_analysis.get("overall_framework", ""),
                    "Conclusion Approaches": tone_analysis.get("conclusion_approaches", "")
                }
                
                # Part 10: Vocabulary & Phrasing Guide
                voice_pattern["PART 10: VOCABULARY & PHRASING GUIDE"] = {
                    "Power Words & Phrases": tone_analysis.get("power_words", []),
                    "Terms & Phrases to Avoid": tone_analysis.get("terms_to_avoid", [])
                }
                
                # Add the mapped voice pattern and target word count to the article input
                article_input["voice_pattern"] = voice_pattern
                article_input["target_word_count"] = target_word_count
                logger.info("Successfully mapped tone analysis to voice pattern format")
            else:
                # If we don't have tone analysis, still include the basic tone analysis
                article_input["tone_analysis"] = {"neural_tone_analysis": {"tone": "informative"}}
                article_input["target_word_count"] = target_word_count
                logger.warning("No tone analysis data available, using default tone")
            
            # Add source material to the input if available - critical for enhanced generation
            if source_material:
                article_input["source_material"] = source_material
                logger.info(f"Added {len(source_material)} source materials to article generation input")
            
            # Generate the article with the enhanced generator
            logger.info("Generating article with EnhancedArticleGenerator")
            article_result = enhanced_generator.generate_article(article_input)
            
            # Format the result to match the expected output structure
            result = {
                "title": article_result.get("title", f"Comprehensive Guide to {topic}"),
                "text": article_result.get("text", ""),
                "word_count": article_result.get("metadata", {}).get("word_count", 0),
                "sources_used": len(source_material or []),
                "fallback_activated": False,
                "provider": "enhanced_openai",
                "voice_pattern_applied": article_result.get("metadata", {}).get("voice_pattern_applied", False)
            }
            
            logger.info(f"Successfully generated article with EnhancedArticleGenerator: {result['word_count']} words")
            return result
            
        except Exception as enhanced_error:
            logger.error(f"Error using EnhancedArticleGenerator: {enhanced_error}")
            # Continue to next method if the enhanced generator fails
        
        # Try using OpenAI with our sectioned approach for longer articles as fallback
        if OPENAI_API_KEY and OPENAI_AVAILABLE and OPENAI_KEY_VALID:
            try:
                logger.info("Attempting to generate article with OpenAI")
                from openai import OpenAI  # Import here to avoid issues if package isn't available
                
                # Initialize OpenAI client
                client = OpenAI(api_key=OPENAI_API_KEY)
                logger.info("OpenAI client initialized successfully")
                
                # Call the OpenAI generator
                article = generate_with_openai(topic, source_material, target_word_count)
                
                # Add any additional metadata
                article["sources_used"] = len(source_material or [])
                article["fallback_activated"] = True
                article["fallback_reason"] = "Enhanced generator failed"
                
                return article
            except Exception as e:
                logger.error(f"Error with OpenAI generation: {e}")
                # Continue to next method
        
        # Try using the class-based ArticleGenerator as fallback
        try:
            # Create article generator
            generator = ArticleGenerator()
            
            # Generate article
            logger.info("Falling back to ArticleGenerator class")
            article = generator.generate_article(
                topic=topic,
                style_profile=tone_analysis or {},
                source_material=source_material or []
            )
            
            return article
        except Exception as e:
            logger.error(f"Error with ArticleGenerator class: {e}")
            # Continue to final fallback
        
        # Try using the FallbackArticleGenerator if all else fails
        try:
            logger.info("Attempting to use FallbackArticleGenerator")
            fallback_generator = FallbackArticleGenerator(
                topic=topic,
                source_material=source_material,
                target_word_count=target_word_count,
                tone_profile=tone_analysis
            )
            return fallback_generator.generate_article()
        except Exception as e:
            logger.error(f"Error with FallbackArticleGenerator: {e}")
            # Continue to emergency fallback
            
    except Exception as e:
        logger.error(f"Critical error in generate_advanced_article: {e}")
    
    # Emergency fallback - this should only happen if everything else fails
    fallback_text = f"# The Impact of {topic}\n\n"
    fallback_text += f"## Introduction\n\n{topic} is an important area worth exploring.\n\n"
    fallback_text += f"## Key Aspects\n\n{topic} encompasses various important elements.\n\n"
    fallback_text += f"## Applications\n\n{topic} has numerous practical applications.\n\n"
    fallback_text += f"## Conclusion\n\nFurther research into {topic} is recommended."
    
    logger.warning("Using emergency fallback article generation")
    return {
        "title": f"The Impact of {topic}",
        "text": fallback_text,
        "word_count": len(fallback_text.split()),
        "sources_used": len(source_material or []),
        "fallback_activated": True,
        "error": "All article generation methods failed",
        "provider": "emergency_fallback"
    }
