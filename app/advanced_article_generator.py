import json
import random
import requests
import os
import logging
from typing import Dict, List, Any, Optional
import re

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("article_generator")

def _lazy_import(module_name, class_name=None):
    """
    Dynamically import a module or class with robust error handling
    
    Args:
        module_name (str): Full module path
        class_name (str, optional): Name of the class to import
    
    Returns:
        Imported module or class, or None if import fails
    """
    try:
        module = __import__(module_name, fromlist=[class_name] if class_name else [])
        return getattr(module, class_name) if class_name else module
    except (ImportError, AttributeError) as e:
        logger.warning(f"Could not import {module_name}.{class_name}: {e}")
        return None

# Dynamically check dependencies
SPACY_AVAILABLE = _lazy_import('spacy') is not None
ANTHROPIC_AVAILABLE = _lazy_import('anthropic') is not None
TONE_ADAPTATION_AVAILABLE = _lazy_import('app.tone_adaptation') is not None

# Try to load environment variables if dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logger.warning("python-dotenv not available, using environment variables directly.")

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
if not CLAUDE_API_KEY:
    logger.warning("CLAUDE_API_KEY not found in environment variables.")

class FallbackNLPProcessor:
    """
    Fallback NLP Processor when spacy is unavailable
    """
    def __init__(self, text: Optional[str] = None):
        self.text = text or ""
        self.sents = self._split_sentences(self.text)
        self.ents = []  # No named entity recognition
    
    def __call__(self, text: str):
        """
        Process text with fallback method
        
        Args:
            text (str): Input text
        
        Returns:
            Processed text object
        """
        return FallbackNLPProcessor(text)
    
    def _split_sentences(self, text):
        """Split text into sentences"""
        return [sent.strip() for sent in re.split(r'[.!?]', text) if sent.strip()]

def get_nlp_processor():
    """
    Retrieve NLP processor with fallback
    
    Returns:
        NLP processor (spacy or fallback)
    """
    if SPACY_AVAILABLE:
        try:
            import spacy
            return spacy.load('en_core_web_sm')
        except Exception as e:
            logger.warning(f"Failed to load spaCy model: {e}")
    
    return FallbackNLPProcessor()

class FallbackArticleGenerator:
    """
    Fallback Article Generator for scenarios with limited dependencies
    """
    def __init__(self, topic: str = "AI and Technology", tone_analysis: Optional[Dict] = None):
        self.topic = topic
        self.tone_analysis = tone_analysis or {
            'formality': 0.5,
            'complexity': 0.5,
            'sentiment': 0.0
        }
        logger.warning("Using Fallback Article Generator")
    
    def generate_article(self) -> Dict[str, Any]:
        """
        Generate a basic article with fallback mechanisms
        
        Returns:
            Dict with article details
        """
        complexity = self.tone_analysis.get('complexity', 0.5)
        formality = self.tone_analysis.get('formality', 0.5)
        
        # Generate paragraphs based on complexity
        num_paragraphs = max(2, int(complexity * 5))
        
        # Adjust tone based on formality
        tone_descriptors = {
            'low': ['casual', 'conversational', 'friendly'],
            'medium': ['balanced', 'informative', 'neutral'],
            'high': ['professional', 'academic', 'formal']
        }
        
        tone_level = 'medium'
        if formality < 0.3:
            tone_level = 'low'
        elif formality > 0.7:
            tone_level = 'high'
        
        tone = random.choice(tone_descriptors[tone_level])
        
        # Basic article generation
        paragraphs = [
            f"Introduction to {self.topic} with a {tone} tone.",
            *[f"Paragraph {i+1} exploring {self.topic} in a {tone} manner." for i in range(num_paragraphs - 2)],
            f"Concluding thoughts on {self.topic}, maintaining a {tone} perspective."
        ]
        
        return {
            "title": f"Understanding {self.topic}",
            "subtitle": f"A {tone} exploration",
            "introduction": paragraphs[0],
            "body": [{"subheading": f"Section {i+1}", "content": para} for i, para in enumerate(paragraphs[1:-1])],
            "conclusion": paragraphs[-1]
        }

def generate_advanced_article(
    topic: str,
    tone_analysis: Optional[Dict[str, Any]] = None,
    source_material: Optional[List[Dict]] = None
) -> Dict[str, Any]:
    """
    Generate an advanced article with fallback mechanisms
    
    Args:
        topic (str): Article topic
        tone_analysis (Dict, optional): Tone analysis metrics
        source_material (List[Dict], optional): Source materials for article
    
    Returns:
        Dict with generated article
    """
    # Try to use Claude if available
    if ANTHROPIC_AVAILABLE and CLAUDE_API_KEY:
        try:
            from anthropic import Anthropic
            client = Anthropic(api_key=CLAUDE_API_KEY)
            
            # Claude-based generation logic would go here
            # This is a placeholder and would need to be implemented
            logger.info("Using Claude for advanced article generation")
        except Exception as e:
            logger.warning(f"Claude generation failed: {e}")
    
    # Fallback to basic article generation
    article_generator = FallbackArticleGenerator(topic, tone_analysis)
    return article_generator.generate_article()

# Expose key functions
__all__ = [
    'generate_advanced_article',
    'FallbackArticleGenerator'
]

class ArticleGenerator:
    """
    Responsible for generating complete articles based on:
    - User selected topic
    - User style profile
    - Source material from the quantum universal crawler
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the ArticleGenerator with Claude client.
        
        Args:
            api_key: Optional API key for Claude. If not provided, will use environment variable.
        """
        self.client = None
        self.logger = logging.getLogger("article_generator")  # Add logger instance to class
        
        # Use provided API key or read directly from .env file
        if not api_key:
            try:
                # Try to read directly from .env file to ensure we have the latest key
                with open('/root/socialme/social-me-test-2/.env', 'r') as f:
                    env_lines = f.readlines()
                    
                for line in env_lines:
                    if line.startswith('CLAUDE_API_KEY='):
                        api_key = line.strip().split('=', 1)[1]
                        break
                        
                if not api_key:
                    self.logger.warning("No Claude API key found in .env file")
                    api_key = CLAUDE_API_KEY  # Fall back to environment variable
            except Exception as e:
                self.logger.error(f"Error reading .env file: {e}")
                api_key = CLAUDE_API_KEY  # Fall back to environment variable
        
        # Initialize Claude client
        if api_key:
            try:
                self.client = _lazy_import('anthropic').Anthropic(
                    api_key=api_key
                )
                self.logger.info("Claude client initialized successfully")
            except Exception as e:
                self.logger.error(f"Error initializing Claude client: {e}")
        else:
            self.logger.warning("Claude API integration not available. Using fallback methods.")
        
    def generate_article(self, topic: str, style_profile: Dict, source_material: List[Dict]) -> Dict:
        """
        Generate a complete article based on the provided inputs.
        
        Args:
            topic: The main topic for the article
            style_profile: JSON containing the user's writing style profile
            source_material: JSON containing relevant source material
            
        Returns:
            Dict containing the complete structured article
        """
        try:
            if not self.client:
                self.logger.error("Claude client not initialized. Check your API key.")
                return {
                    "title": "Error Generating Article",
                    "subtitle": "API Authentication Error",
                    "body": "There was an error authenticating with the Claude API. Please check your API key and try again.",
                    "error": "API authentication error"
                }
                
            self.logger.info(f"Generating article for topic: {topic}")
            
            # Prepare source material
            self.logger.info("Preparing source material")
            prepared_sources = self._prepare_source_material(source_material)
            
            # Create article structure
            self.logger.info("Creating article structure")
            try:
                themes = self._extract_themes(prepared_sources, topic)
            except Exception as e:
                self.logger.error(f"Error calling Claude for theme extraction: {e}")
                themes = ["Theme 1", "Theme 2", "Theme 3"]  # Fallback themes
            
            # Generate the full article with Claude
            self.logger.info("Generating full article with Claude")
            try:
                article = self._generate_full_article(topic, style_profile, prepared_sources, self._create_article_structure(topic, prepared_sources))
                return article
            except Exception as e:
                self.logger.error(f"Error calling Claude API: {e}")
                
                # Check if it's an authentication error
                if "authentication_error" in str(e) or "invalid x-api-key" in str(e) or "401" in str(e):
                    return {
                        "title": "API Authentication Error",
                        "subtitle": "Unable to Generate Article",
                        "introduction": "There was an error authenticating with the Claude API. The API key appears to be invalid or expired.",
                        "body": [
                            {
                                "subheading": "API Key Error",
                                "content": "The system was unable to authenticate with the Claude API. This is typically caused by an invalid or expired API key."
                            },
                            {
                                "subheading": "How to Fix This",
                                "content": "To fix this issue, you need to obtain a valid API key from Anthropic and update the CLAUDE_API_KEY value in your .env file."
                            }
                        ],
                        "conclusion": "Once you've updated your API key, you'll be able to generate advanced articles using the Claude AI model.",
                        "error": str(e)
                    }
                else:
                    # Generic error
                    return {
                        "title": "Error Generating Article",
                        "subtitle": "An error occurred during article generation",
                        "introduction": "The system encountered an error while trying to generate your article.",
                        "body": [
                            {
                                "subheading": "Error Details",
                                "content": f"Error message: {str(e)}"
                            },
                            {
                                "subheading": "Troubleshooting",
                                "content": "Please check your inputs and try again. If the problem persists, contact support."
                            }
                        ],
                        "conclusion": "We apologize for the inconvenience. Please try again later.",
                        "error": str(e)
                    }
                
        except Exception as e:
            self.logger.error(f"Unexpected error in generate_article: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            return {
                "title": "Error Generating Article",
                "subtitle": "An unexpected error occurred",
                "body": f"Error: {str(e)}",
                "error": str(e)
            }
    
    def _prepare_source_material(self, source_material: List[Dict]) -> List[Dict]:
        """Process and prepare source material for use in article generation."""
        self.logger.info("Preparing source material")
        
        prepared_sources = []
        for source in source_material:
            # Extract only the most relevant parts
            if source.get('relevance_score', 0) > 0.2:  # Only use sources with decent relevance
                prepared_source = {
                    "title": source.get("title", "Untitled Source"),
                    "url": source.get("url", ""),
                    "content": source.get("content", ""),
                    "key_points": self._extract_key_points(source.get("content", "")),
                    "relevance_score": source.get("relevance_score", 0)
                }
                prepared_sources.append(prepared_source)
        
        # Sort sources by relevance score (highest first)
        prepared_sources.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return prepared_sources
    
    def _extract_key_points(self, content: str) -> List[str]:
        """Extract key points from source content."""
        # Split content into paragraphs
        paragraphs = [p.strip() for p in content.split('\n') if p.strip()]
        
        # Select the most substantial paragraphs
        substantial_paragraphs = [p for p in paragraphs if len(p.split()) > 20]
        
        # If we have more than 5 substantial paragraphs, select a subset
        key_paragraphs = substantial_paragraphs[:min(5, len(substantial_paragraphs))]
        
        return key_paragraphs
    
    def _create_article_structure(self, topic: str, sources: List[Dict]) -> Dict:
        """Create the article structure with sections based on the topic and sources."""
        self.logger.info("Creating article structure")
        
        # Get key themes from sources
        themes = self._extract_themes(sources, topic)
        
        # Create structure with 4-7 sections
        num_sections = min(len(themes), 7)
        num_sections = max(num_sections, 4)  # Ensure at least 4 sections
        
        structure = {
            "title": f"Generated title for {topic}",  # Placeholder - will be generated by Claude
            "sections": themes[:num_sections],
            "estimated_word_count": 4000,
            "words_per_section": 4000 // (num_sections + 2)  # +2 for intro and conclusion
        }
        
        return structure
    
    def _extract_themes(self, sources: List[Dict], topic: str) -> List[str]:
        """Extract potential themes/section topics from sources."""
        # If we have Claude available and enough sources with content, use Claude to extract themes
        if self.client and sources and len(sources) >= 3:
            sources_content = "\n\n".join([
                f"SOURCE {i+1}: {source.get('title', 'Untitled')}\n{source.get('content', '')[:1000]}"
                for i, source in enumerate(sources[:5])  # Use up to 5 sources
            ])
            
            # Using Claude to extract themes
            prompt = f"""
            Based on the following source materials about "{topic}", identify 7 distinct themes or subtopics that would make good section headings for a comprehensive article.

            For each theme:
            1. Create a clear, specific section heading (not just generic headings like "Introduction" or "Benefits")
            2. Each heading should represent a distinct aspect of the main topic
            3. The collection of headings should provide comprehensive coverage of the topic

            SOURCE MATERIALS:
            {sources_content}

            Please output your response as a JSON list of strings, each representing a potential section heading. For example:
            ["Heading 1: Specific Aspect", "Heading 2: Another Specific Aspect", ...]
            """
            
            try:
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",  # Fallback to sonnet if opus not available
                    max_tokens=1024,
                    temperature=0.7,
                    system="You are an expert content strategist who identifies key themes in source materials to create article outlines.",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # Extract JSON from response
                response_text = response.content[0].text
                json_match = re.search(r'\[(.*?)\]', response_text, re.DOTALL)
                if json_match:
                    try:
                        themes = json.loads('[' + json_match.group(1) + ']')
                        return themes
                    except json.JSONDecodeError:
                        self.logger.warning("Failed to parse themes JSON from Claude response")
            except Exception as e:
                self.logger.error(f"Error calling Claude for theme extraction: {e}")
        
        # Fallback: Create generic section headings based on the topic
        fallback_themes = [
            f"Understanding {topic}: A Comprehensive Overview",
            f"The Evolution of {topic} Over Time",
            f"Key Challenges and Opportunities in {topic}",
            f"Practical Applications of {topic} Today",
            f"Future Trends and Innovations in {topic}",
            f"Case Studies: {topic} in Action",
            f"Best Practices for Implementing {topic}"
        ]
        
        return fallback_themes
    
    def _generate_full_article(self, topic: str, style_profile: Dict, sources: List[Dict], structure: Dict) -> Dict:
        """Generate the complete article using Claude with a chained approach."""
        self.logger.info("Generating full article with Claude")
        
        if not self.client:
            return self._generate_fallback_article(topic, style_profile, sources)
        
        # Format source material for the prompt
        source_content = ""
        for i, source in enumerate(sources[:10]):  # Limit to top 10 sources
            source_content += f"""
            SOURCE {i+1}: 
            Title: {source.get('title', 'Untitled')}
            URL: {source.get('url', 'No URL')}
            Relevance Score: {source.get('relevance_score', 0)}
            Content: {source.get('content', '')[:1000]}  # Limit content length
            
            """
        
        # Create sections with expected word counts
        sections = structure["sections"]
        words_per_section = structure["words_per_section"]
        
        try:
            # Step 1: Generate the article outline and introduction
            self.logger.info("Step 1: Generating article outline and introduction")
            outline = self._generate_article_outline(topic, style_profile, source_content, sections)
            
            # Step 2: Generate each section separately
            self.logger.info("Step 2: Generating article sections")
            article_sections = []
            
            for i, section_heading in enumerate(sections[:7]):  # Limit to 7 sections max
                self.logger.info(f"Generating section {i+1}: {section_heading}")
                section_content = self._generate_article_section(
                    topic, 
                    section_heading, 
                    style_profile, 
                    source_content, 
                    words_per_section
                )
                article_sections.append({
                    "subheading": section_heading,
                    "content": section_content,
                    "sources": [source.get('title', 'Untitled') for source in sources[:3]]  # Simplified for testing
                })
            
            # Step 3: Generate the conclusion
            self.logger.info("Step 3: Generating article conclusion")
            conclusion = self._generate_article_conclusion(topic, style_profile, source_content, article_sections)
            
            # Combine everything into the final article
            article = {
                "title": outline.get("title", f"The Impact of {topic}"),
                "subtitle": outline.get("subtitle", ""),
                "introduction": outline.get("introduction", ""),
                "body": article_sections,
                "conclusion": conclusion,
                "sources": [{"name": source.get('title', 'Untitled'), "url": source.get('url', '#')} for source in sources[:5]]
            }
            
            return article
            
        except Exception as e:
            self.logger.error(f"Error in article generation: {e}")
            return self._create_error_response(str(e))
    
    def _generate_article_outline(self, topic: str, style_profile: Dict, source_content: str, sections: List[str]) -> Dict:
        """Generate the article outline including title and introduction."""
        system_prompt = """You are an expert content writer who can adapt to any writing style and create engaging article outlines."""
        
        user_prompt = f"""
        Create an outline for an article on "{topic}" with the following sections:
        {json.dumps(sections)}
        
        Based on these source materials:
        {source_content[:2000]}
        
        Please provide:
        1. A compelling title
        2. An optional subtitle
        3. An engaging introduction (150-200 words)
        
        Use this writing style profile: {json.dumps(style_profile)}
        
        Return your response in this JSON format:
        {{
          "title": "Article title",
          "subtitle": "Optional subtitle",
          "introduction": "Full introduction paragraph"
        }}
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            response_text = response.content[0].text
            
            # Extract JSON from response
            json_match = re.search(r'({[\s\S]*})', response_text)
            if json_match:
                outline_json = json.loads(json_match.group(1))
                return outline_json
            else:
                self.logger.error("No JSON found in Claude outline response")
                return {
                    "title": f"The Impact of {topic}",
                    "subtitle": "A Comprehensive Analysis",
                    "introduction": f"This article explores the various aspects of {topic}, examining its impact, challenges, and future directions."
                }
        except Exception as e:
            self.logger.error(f"Error generating article outline: {e}")
            return {
                "title": f"The Impact of {topic}",
                "subtitle": "A Comprehensive Analysis",
                "introduction": f"This article explores the various aspects of {topic}, examining its impact, challenges, and future directions."
            }
    
    def _generate_article_section(self, topic: str, section_heading: str, style_profile: Dict, 
                                 source_content: str, target_words: int) -> str:
        """Generate a single section of the article."""
        system_prompt = """You are an expert content writer who creates detailed, informative article sections."""
        
        user_prompt = f"""
        Write a detailed section for an article on "{topic}" with the heading:
        "{section_heading}"
        
        Use these source materials for reference:
        {source_content[:1500]}
        
        Guidelines:
        1. The section should be approximately {target_words} words
        2. Match this writing style profile: {json.dumps(style_profile)}
        3. Include specific details, examples, and insights relevant to the section topic
        4. Maintain a cohesive flow with the overall article theme
        
        Return only the section content as plain text, without the heading.
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1500,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            section_content = response.content[0].text.strip()
            return section_content
        except Exception as e:
            self.logger.error(f"Error generating article section '{section_heading}': {e}")
            return f"This section discusses important aspects of {section_heading} related to {topic}. [Error: {str(e)}]"
    
    def _generate_article_conclusion(self, topic: str, style_profile: Dict, source_content: str, 
                                    sections: List[Dict]) -> str:
        """Generate the article conclusion."""
        system_prompt = """You are an expert content writer who creates impactful article conclusions."""
        
        # Extract section headings for context
        section_headings = [section.get("subheading", "Untitled Section") for section in sections]
        
        user_prompt = f"""
        Write a conclusion for an article on "{topic}" that has covered these sections:
        {json.dumps(section_headings)}
        
        Guidelines:
        1. The conclusion should be approximately 200-250 words
        2. Match this writing style profile: {json.dumps(style_profile)}
        3. Summarize key insights from the article
        4. Provide final thoughts or future perspectives on the topic
        5. End with an impactful closing statement
        
        Return only the conclusion text.
        """
        
        try:
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=800,
                temperature=0.7,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            conclusion = response.content[0].text.strip()
            return conclusion
        except Exception as e:
            self.logger.error(f"Error generating article conclusion: {e}")
            return f"In conclusion, {topic} represents an important area with significant implications. The various aspects discussed in this article highlight the complexity and relevance of this subject in today's world."
    
    def _generate_fallback_article(self, topic: str, style_profile: Dict, sources: List[Dict]) -> Dict:
        """Generate a simple fallback article when Claude API is not available."""
        self.logger.info("Using fallback article generation")
        
        # Create a basic article structure
        sections = [
            f"Introduction to {topic}",
            "Key Insights and Applications",
            "Challenges and Considerations",
            "Future Perspectives"
        ]
        
        # Extract some content from sources
        source_paragraphs = []
        for source in sources:
            content = source.get("content", "")
            paragraphs = [p for p in content.split("\n") if p.strip()]
            if paragraphs:
                source_paragraphs.extend(paragraphs[:2])  # Take up to 2 paragraphs from each source
        
        # Generate a simple article
        article = {
            "title": f"A Comprehensive Guide to {topic}",
            "introduction": f"This article explores the important aspects of {topic}, examining its key features, practical applications, and future considerations.",
            "body": [],
            "conclusion": f"As we've seen, {topic} represents an important area that continues to evolve. By understanding its fundamentals and keeping track of emerging trends, readers can better navigate this complex subject.",
            "sources": []
        }
        
        # Add sources
        for source in sources:
            article["sources"].append({
                "name": source.get("title", "Untitled Source"),
                "url": source.get("url", ""),
                "description": "Reference source"
            })
        
        # Add body sections
        for i, section in enumerate(sections):
            section_content = "Content not available due to API limitations. Please check your Claude API configuration."
            
            # Try to use some content from sources if available
            if source_paragraphs:
                start_idx = i * 2
                end_idx = start_idx + 2
                if start_idx < len(source_paragraphs):
                    section_content = " ".join(source_paragraphs[start_idx:end_idx])
            
            article["body"].append({
                "subheading": section,
                "content": section_content,
                "sources": [s.get("title", "Source") for s in sources[:2]]
            })
        
        return article
    
    def _create_error_response(self, error_message: str) -> Dict:
        """Create an error response when article generation fails."""
        return {
            "title": "Error Generating Article",
            "introduction": "There was an error generating your article.",
            "body": [
                {
                    "subheading": "Error Details",
                    "content": error_message,
                    "sources": []
                }
            ],
            "conclusion": "Please try again or contact support if the problem persists.",
            "sources": [],
            "error": True
        }

    def validate_article(self, article: Dict) -> Dict:
        """Validate the generated article structure and content."""
        self.logger.info("Validating article structure and content")
        
        validation_results = {"valid": True, "issues": []}
        
        # Check for required fields
        required_fields = ["title", "introduction", "body", "conclusion", "sources"]
        for field in required_fields:
            if field not in article:
                validation_results["valid"] = False
                validation_results["issues"].append(f"Missing required field: {field}")
        
        # Check article length
        if validation_results["valid"]:
            word_count = len(article["introduction"].split()) + len(article["conclusion"].split())
            for section in article["body"]:
                word_count += len(section["content"].split())
            
            if word_count < 3500:
                validation_results["valid"] = False
                validation_results["issues"].append(f"Article too short: {word_count} words (min 3500)")
            elif word_count > 4500:
                validation_results["valid"] = False
                validation_results["issues"].append(f"Article too long: {word_count} words (max 4500)")
            
            # Add word count to the results
            validation_results["word_count"] = word_count
        
        return validation_results


# Helper function to format tone analysis results into a style profile
def format_tone_analysis_to_style_profile(tone_analysis):
    """
    Convert a tone analysis result into a style profile for the article generator
    
    Args:
        tone_analysis: Dict containing the tone analysis results
        
    Returns:
        Dict formatted as a style profile
    """
    # Extract tone patterns
    thought_patterns = {}
    reasoning_style = {}
    
    if "thought_patterns" in tone_analysis:
        thought_patterns = tone_analysis["thought_patterns"]
    
    if "reasoning_style" in tone_analysis:
        reasoning_style = tone_analysis["reasoning_style"]
    
    # Determine tone based on dominant thought patterns
    tone = "balanced"
    if thought_patterns:
        sorted_patterns = sorted(thought_patterns.items(), key=lambda x: x[1], reverse=True)
        top_pattern = sorted_patterns[0][0] if sorted_patterns else "analytical"
        
        tone_mapping = {
            "analytical": "professional",
            "logical": "professional",
            "systematic": "professional",
            "creative": "conversational",
            "intuitive": "conversational",
            "emotional": "casual"
        }
        
        tone = tone_mapping.get(top_pattern, "balanced")
    
    # Determine formality based on reasoning style
    formality = "medium"
    if reasoning_style:
        sorted_reasoning = sorted(reasoning_style.items(), key=lambda x: x[1], reverse=True)
        top_reasoning = sorted_reasoning[0][0] if sorted_reasoning else "deductive"
        
        formality_mapping = {
            "deductive": "high",
            "statistical": "high",
            "abductive": "medium",
            "inductive": "medium",
            "analogical": "low",
            "narrative": "low"
        }
        
        formality = formality_mapping.get(top_reasoning, "medium")
    
    # Create the style profile
    style_profile = {
        "tone": tone,
        "formality": formality,
        "vocabulary_level": "advanced" if formality == "high" else "intermediate",
        "sentence_length": "long" if formality == "high" else "medium",
        "paragraph_structure": "complex" if formality == "high" else "balanced",
        "rhetorical_devices": [],
        "voice": "active",
        "perspective": "third_person" if formality == "high" else "mixed"
    }
    
    # Add rhetorical devices based on reasoning style
    if "analogical" in reasoning_style and reasoning_style["analogical"] > 0.3:
        style_profile["rhetorical_devices"].append("metaphor")
        style_profile["rhetorical_devices"].append("analogy")
    
    if "narrative" in reasoning_style and reasoning_style["narrative"] > 0.3:
        style_profile["rhetorical_devices"].append("storytelling")
    
    if "abductive" in reasoning_style and reasoning_style["abductive"] > 0.3:
        style_profile["rhetorical_devices"].append("rhetorical_questions")
    
    return style_profile

# Helper function to format crawler results into source material
def format_crawler_results_to_source_material(crawler_results, topic):
    """
    Convert crawler results into source material for the article generator
    
    Args:
        crawler_results: List of dicts containing crawler results
        topic: The article topic for relevance scoring
        
    Returns:
        List of dicts formatted as source material
    """
    source_material = []
    
    for result in crawler_results:
        # Calculate simple relevance score based on topic presence
        content = result.get("content", "")
        title = result.get("title", "")
        relevance_score = 0.5  # Base score
        
        # Check if topic is in title or content
        if topic.lower() in title.lower():
            relevance_score += 0.3
        
        # Calculate frequency of topic in content
        topic_words = [word.lower() for word in topic.split()]
        content_lower = content.lower()
        
        word_count = 0
        for word in topic_words:
            if len(word) > 3:  # Only count significant words
                word_count += content_lower.count(word)
        
        # Adjust relevance score based on frequency
        if word_count > 10:
            relevance_score += 0.2
        elif word_count > 5:
            relevance_score += 0.1
        
        # Cap relevance at 1.0
        relevance_score = min(relevance_score, 1.0)
        
        source_material.append({
            "title": title,
            "url": result.get("url", ""),
            "content": content,
            "relevance_score": relevance_score
        })
    
    # Sort by relevance
    source_material.sort(key=lambda x: x["relevance_score"], reverse=True)
    
    return source_material


# Function to be called by Flask routes
def generate_advanced_article(
    topic: str, 
    tone_analysis: Dict[str, Any], 
    source_material: List[Dict], 
    target_word_count: int = 4000
) -> Dict[str, Any]:
    """
    Generate an advanced article with specified parameters
    
    Args:
        topic (str): Main topic of the article
        tone_analysis (Dict): Tone and style analysis
        source_material (List[Dict]): Source materials for the article
        target_word_count (int, optional): Target word count for the article. Defaults to 4000.
    
    Returns:
        Dict[str, Any]: Generated article with content and metadata
    """
    # Initialize article generator
    generator = ArticleGenerator()
    
    # Prepare style profile from tone analysis
    style_profile = {
        'avg_sentence_length': tone_analysis.get('style_fingerprint', {}).get('avg_sentence_length', 5.0),
        'vocabulary_diversity': tone_analysis.get('style_fingerprint', {}).get('vocabulary_diversity', 0.8),
        'formality_score': tone_analysis.get('style_fingerprint', {}).get('formality_score', 0.6),
        'style_prompt': tone_analysis.get('style_prompt', '')
    }
    
    # Generate initial article
    article = generator.generate_article(
        topic=topic, 
        style_profile=style_profile, 
        source_material=source_material
    )
    
    # Ensure article content is a string
    if isinstance(article.get('body'), list):
        article_content = "\n\n".join([
            f"{section.get('subheading', '')}\n{section.get('content', '')}" 
            for section in article.get('body', [])
        ])
    else:
        article_content = article.get('body', '')
    
    # Calculate current word count
    current_word_count = len(article_content.split())
    
    # If word count is less than target, generate additional content
    if current_word_count < target_word_count:
        # Prepare prompt for additional content generation
        additional_content_prompt = f"""
        You have already written an article about {topic} that is {current_word_count} words long. 
        Please generate additional content to reach approximately {target_word_count} words. 
        The additional content should:
        1. Expand on existing sections
        2. Add new perspectives or case studies
        3. Maintain the same writing style and tone
        4. Provide deeper insights into {topic}
        5. Ensure coherence with the existing article
        
        Current article content for reference:
        {article_content}
        """
        
        try:
            # Use Claude to generate additional content
            if generator.client:
                additional_content_response = generator.client.messages.create(
                    model="claude-2.1",
                    max_tokens=2000,
                    messages=[
                        {
                            "role": "user",
                            "content": additional_content_prompt
                        }
                    ]
                )
                additional_content = additional_content_response.content[0].text
                
                # Combine original and additional content
                article_content += "\n\n" + additional_content
            else:
                # Fallback method if Claude client is not available
                additional_content = f"""
                ## Further Insights into {topic}
                
                The exploration of {topic} reveals complex and multifaceted dimensions that warrant deeper examination. 
                Ongoing research continues to uncover innovative approaches and emerging trends in this dynamic field.
                
                ### Advanced Perspectives
                
                While the previous sections provided a comprehensive overview, there are additional nuanced considerations 
                that merit thorough investigation. The intersection of technological innovation and human experience 
                presents both challenges and unprecedented opportunities.
                
                ### Future Trajectory
                
                As {topic} continues to evolve, interdisciplinary collaboration and continuous learning will be 
                paramount in navigating the intricate landscape of potential developments and ethical considerations.
                """
                
                article_content += "\n\n" + additional_content
        except Exception as e:
            logger.warning(f"Failed to generate additional content: {e}")
    
    # Prepare final article dictionary
    final_article = {
        'title': article.get('title', topic),
        'content': article_content,
        'word_count': len(article_content.split()),
        'target_word_count': target_word_count
    }
    
    return final_article
