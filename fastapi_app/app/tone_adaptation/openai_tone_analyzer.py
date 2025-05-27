"""
OpenAI-based Tone Analyzer

This module provides tone analysis functionality using OpenAI API,
serving as a lightweight alternative to the spaCy-based implementation.
"""

import logging
import json
import os
from typing import Dict, Any, List, Optional, Union
from pathlib import Path

# Setup logging
logger = logging.getLogger("app.tone_adaptation.openai_tone_analyzer")

# Load API key directly
CONFIG_FILE_PATH = os.environ.get(
    "API_CONFIG_FILE_PATH", 
    str(Path(__file__).parent.parent.parent.parent.parent / "config" / "api_keys.json")
)

def get_openai_api_key():
    """Get OpenAI API key from config file"""
    try:
        # First check if the key is in environment variables
        env_key = os.environ.get("OPENAI_API_KEY")
        if env_key:
            logger.info(f"Found OpenAI API key in environment variables (length: {len(env_key)})")
            logger.info(f"Environment key begins with: {env_key[:10]}...")
            return env_key
            
        # Check config file
        if os.path.exists(CONFIG_FILE_PATH):
            logger.info(f"Loading API key from config file: {CONFIG_FILE_PATH}")
            with open(CONFIG_FILE_PATH, "r") as f:
                if CONFIG_FILE_PATH.endswith(".json"):
                    data = json.load(f)
                    config_key = data.get("OPENAI_API_KEY")
                    if config_key:
                        logger.info(f"Found OpenAI API key in config file (length: {len(config_key)})")
                        logger.info(f"Config key begins with: {config_key[:10]}...")
                        return config_key
                    else:
                        logger.error("Config file does not contain OPENAI_API_KEY")
                else:
                    logger.error(f"Config file {CONFIG_FILE_PATH} is not a JSON file")
        else:
            logger.error(f"Config file not found at: {CONFIG_FILE_PATH}")
    except Exception as e:
        logger.error(f"Error loading API key: {e}")
    
    logger.error("Failed to load OpenAI API key from any source")
    return None

class OpenAIToneAnalyzer:
    """
    Tone analysis implementation using OpenAI API
    Provides compatible interface with the original tone analysis system
    """
    def __init__(self):
        self.logger = logger
        self.api_key = get_openai_api_key()
        
        # Validate API key format - be lenient with all known OpenAI key formats
        if not self.api_key or len(self.api_key) < 20:
            self.logger.error("Missing or too short OpenAI API key")
            return
            
        # Check for all known key formats
        if self.api_key.startswith('sk-'):
            key_type = "standard"
        elif 'sk-proj-' in self.api_key:
            key_type = "project"
        elif 'sk-svcacct-' in self.api_key:
            key_type = "service_account"
        else:
            # Be even more lenient for unknown formats but with sufficient length
            key_type = "unknown"
            
        self.logger.info(f"OpenAI API key detected (type: {key_type}, length: {len(self.api_key)})")
        
        # Initialize OpenAI client with correct configuration
        try:
            from openai import OpenAI
            
            # Use the same consistent configuration for all key types for better compatibility
            # This helps address authentication issues with different key formats
            self.client = OpenAI(
                api_key=self.api_key,
                base_url="https://api.openai.com/v1",  # Explicit API endpoint
                max_retries=3,                        # Add retries for resilience
                timeout=60.0                          # Longer timeout for OpenAI API
            )
                
            self.logger.info("OpenAI client initialized successfully")
        except Exception as e:
            self.client = None
            self.logger.error(f"Error initializing OpenAI client: {e}")
    
    def analyze_tone(self, 
                     sample_text: Optional[str] = None, 
                     url: Optional[str] = None,
                     document_content: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze the tone of provided content (text, URL, or document)
        
        Args:
            sample_text: Direct text input for analysis
            url: URL to extract content from for analysis
            document_content: Document content for analysis
        
        Returns:
            Dict containing comprehensive tone analysis results
        """
        # Determine which source to analyze
        content_to_analyze = None
        source_type = None
        
        if sample_text:
            content_to_analyze = sample_text
            source_type = "text"
        elif url:
            # For URLs, use a simplified direct approach or fetch with requests
            try:
                # Simplified URL content extraction without dependencies
                import requests
                from bs4 import BeautifulSoup
                
                # Prepare headers to mimic browser
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                }
                
                # Make request with timeout
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove script, style, and navigation elements
                for element in soup(["script", "style", "nav", "header", "footer"]):
                    element.decompose()
                
                # Extract text content
                text = soup.get_text(separator=' ', strip=True)
                
                # Clean text (remove excessive whitespace)
                import re
                text = re.sub(r'\s+', ' ', text).strip()
                
                content_to_analyze = text[:10000]  # Limit to 10,000 chars
                source_type = "url"
                
                self.logger.info(f"Successfully extracted {len(content_to_analyze)} chars from URL")
                
            except Exception as e:
                self.logger.error(f"Error extracting content from URL: {e}")
                return {
                    "status": "error",
                    "message": f"Error extracting content from URL: {str(e)}"
                }
        elif document_content:
            content_to_analyze = document_content
            source_type = "document"
        
        if not content_to_analyze:
            return {
                "status": "error",
                "message": "No valid content provided for tone analysis"
            }
            
        # Perform analysis with OpenAI
        try:
            if not self.client:
                raise ValueError("OpenAI client not initialized")
                
            # Create prompt for tone analysis
            prompt = self._create_tone_analysis_prompt(content_to_analyze)
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o",  # Using the latest model for best analysis
                messages=[
                    {"role": "system", "content": "You are an advanced tone analyzer specializing in detailed writing style analysis. Provide comprehensive, structured analysis formatted as valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3  # Lower temperature for more consistent results
            )
            
            # Parse the response
            analysis_result = json.loads(response.choices[0].message.content)
            
            # Add metadata
            analysis_result["source_type"] = source_type
            analysis_result["status"] = "success"
            analysis_result["provider"] = "openai"
            
            return analysis_result
            
        except Exception as e:
            self.logger.error(f"Error analyzing tone with OpenAI: {e}")
            return {
                "status": "error",
                "message": f"Error analyzing tone: {str(e)}",
                "source_type": source_type
            }
    
    def generate_style_samples(self, 
                               sample_text: str,
                               num_samples: int = 3,
                               target_length: int = 250) -> Dict[str, Any]:
        """
        Generate multiple writing style samples based on analysis of provided text
        
        Args:
            sample_text: Reference text to analyze and mimic style
            num_samples: Number of different samples to generate
            target_length: Approximate length of each sample in words
            
        Returns:
            Dict containing tone analysis and multiple style samples
        """
        # First, analyze the tone
        tone_analysis = self.analyze_tone(sample_text=sample_text)
        
        # Then generate style samples based on that analysis
        try:
            if not self.client:
                raise ValueError("OpenAI client not initialized")
                
            # Create prompt for style sample generation
            prompt = self._create_style_samples_prompt(
                sample_text=sample_text,
                tone_analysis=tone_analysis,
                num_samples=num_samples,
                target_length=target_length
            )
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert writing style analyst and content creator who can perfectly mimic writing styles."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7  # Higher temperature for more creative variety
            )
            
            # Parse the response
            result = json.loads(response.choices[0].message.content)
            
            # Add the tone analysis to the result
            result["tone_analysis"] = tone_analysis
            result["status"] = "success"
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating style samples with OpenAI: {e}")
            return {
                "status": "error",
                "message": f"Error generating style samples: {str(e)}",
                "tone_analysis": tone_analysis
            }
    
    def regenerate_style_samples(self,
                                previous_samples: Dict[str, Any],
                                feedback: List[Dict[str, Any]],
                                num_samples: int = 3) -> Dict[str, Any]:
        """
        Regenerate style samples based on previous samples and user feedback
        
        Args:
            previous_samples: Previous style samples and analysis
            feedback: User feedback on previous samples
            num_samples: Number of new samples to generate
            
        Returns:
            Dict containing updated style samples
        """
        try:
            if not self.client:
                raise ValueError("OpenAI client not initialized")
                
            # Extract original sample text from previous analysis
            original_text = previous_samples.get("original_text", "")
            if not original_text and "tone_analysis" in previous_samples:
                # Try to extract from tone analysis
                tone_analysis = previous_samples.get("tone_analysis", {})
                if "original_sample" in tone_analysis:
                    original_text = tone_analysis["original_sample"]
            
            # If we still don't have text, return error
            if not original_text:
                return {
                    "status": "error",
                    "message": "Could not find original text to regenerate samples"
                }
            
            # Create prompt for regeneration
            prompt = self._create_regeneration_prompt(
                original_text=original_text,
                previous_samples=previous_samples,
                feedback=feedback,
                num_samples=num_samples
            )
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert writing style analyst who can adapt content based on feedback."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.7
            )
            
            # Parse the response
            result = json.loads(response.choices[0].message.content)
            
            # Add metadata
            result["status"] = "success"
            result["original_text"] = original_text
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error regenerating style samples with OpenAI: {e}")
            return {
                "status": "error",
                "message": f"Error regenerating style samples: {str(e)}"
            }
    
    def _create_tone_analysis_prompt(self, content: str) -> str:
        """
        Create a detailed prompt for OpenAI tone analysis
        """
        # Create the full prompt text - note we avoid using an f-string with a comment inside
        prompt_text = """Analyze the following text for tone, style, and writing characteristics. 
        Provide a comprehensive analysis that includes:
        
        1. FORMALITY_ANALYSIS:
           - overall_formality_score (0-100)
           - formal_indicators (list of phrases/words that indicate formality)
           - informal_indicators (list of phrases/words that indicate informality)
           
        2. LINGUISTIC_COMPLEXITY:
           - vocabulary_sophistication (0-100)
           - sentence_complexity (0-100)
           - technical_terminology_density (0-100)
           
        3. REASONING_PATTERNS:
           - primary_reasoning_style (deductive, inductive, abductive, etc.)
           - evidence_usage_pattern (anecdotal, statistical, authoritative, etc.)
           - logical_structure_rating (0-100)
           
        4. STYLISTIC_ELEMENTS:
           - tone_markers (analytical, creative, conversational, etc.)
           - distinctive_phrases (unique or characteristic expressions)
           - sentence_structure_preferences (simple, compound, complex)
           
        5. DOMAIN_CLASSIFICATION:
           - primary_domain (technical, academic, business, casual, etc.)
           - confidence_score (0-100)
           
        6. REPRESENTATIVE_SAMPLES:
           - characteristic_sentences (2-3 sentences that exemplify the writing style)
           
        7. PSYCHOLOGICAL_PROFILE:
           - thought_patterns (analytical, creative, systematic, intuitive, etc.)
           - communication_style (direct, elaborative, metaphorical, etc.)
           - audience_relationship (formal, conversational, persuasive, etc.)
        
        TEXT TO ANALYZE:
        {0}
        
        Include an "original_sample" field with the first 500 characters of the analyzed text.
        Format the response as a valid JSON object with each section properly nested.
        """
        
        # Limit content to 8000 chars to avoid token limits
        limited_content = content[:8000]
        
        return prompt_text.format(limited_content)
    
    def _create_style_samples_prompt(self, 
                                   sample_text: str,
                                   tone_analysis: Dict[str, Any],
                                   num_samples: int,
                                   target_length: int) -> str:
        """
        Create a prompt for generating style samples
        """
        # Prepare the safe sample text for JSON embedding
        limited_sample = sample_text[:4000]  # Limit to 4000 chars
        short_sample = sample_text[:500]  # First 500 chars for original_text
        # Replace quotes safely
        safe_short_sample = short_sample.replace('"', '\"')  
        
        prompt_template = """Analyze the writing style in the following text, then generate {0} distinct paragraph samples that emulate this exact writing style.
        
        Each sample should be about {1} words long and should represent content the original author might write about a general topic like technology, business, or society.
        
        The samples should precisely match the original author's:
        1. Sentence structure and complexity
        2. Vocabulary level and word choice patterns
        3. Tone and voice (formal/informal, passionate/detached, etc.)
        4. Characteristic expressions and phrases
        5. Reasoning patterns and argument structure
        
        REFERENCE TEXT TO ANALYZE:
        {2}
        
        Return your response as a JSON object with this structure:
        {{
            "original_text": "{3}...",
            "style_analysis": {{
                "key_characteristics": [list of 5-7 key style characteristics],
                "distinctive_patterns": [list of 3-5 distinctive patterns]
            }},
            "samples": [
                {{
                    "id": 1,
                    "sample_text": "First sample text here...",
                    "topic": "Brief topic description"
                }},
                ...repeat for all samples...
            ]
        }}
        """
        
        return prompt_template.format(num_samples, target_length, limited_sample, safe_short_sample)
    
    def _create_regeneration_prompt(self,
                                   original_text: str,
                                   previous_samples: Dict[str, Any],
                                   feedback: List[Dict[str, Any]],
                                   num_samples: int) -> str:
        """
        Create a prompt for regenerating samples based on feedback
        """
        # Extract positive and negative feedback
        positive_ids = []
        negative_ids = []
        comments = []
        
        for fb in feedback:
            sample_id = fb.get("sample_id")
            rating = fb.get("rating")
            
            if rating == "upvote" and sample_id:
                positive_ids.append(sample_id)
            elif rating == "downvote" and sample_id:
                negative_ids.append(sample_id)
                
            if fb.get("comments"):
                comments.append(fb.get("comments"))
        
        # Extract previous samples
        previous_samples_list = previous_samples.get("samples", [])
        positive_samples = [s for s in previous_samples_list if s.get("id") in positive_ids]
        negative_samples = [s for s in previous_samples_list if s.get("id") in negative_ids]
        
        # Create the feedback summary
        feedback_text = ""
        if positive_samples:
            feedback_text += "POSITIVELY RATED EXAMPLES (These were good):\n"
            for i, sample in enumerate(positive_samples):
                feedback_text += f"{i+1}. {sample.get('sample_text', '')}\n\n"
        
        if negative_samples:
            feedback_text += "NEGATIVELY RATED EXAMPLES (These should be avoided):\n"
            for i, sample in enumerate(negative_samples):
                feedback_text += f"{i+1}. {sample.get('sample_text', '')}\n\n"
        
        if comments:
            feedback_text += "USER COMMENTS:\n"
            for i, comment in enumerate(comments):
                feedback_text += f"{i+1}. {comment}\n"
                
        # Create the final prompt
        return f"""Based on the original writing sample and user feedback, generate {num_samples} NEW paragraph samples that better match the user's preferred writing style.
        
        ORIGINAL TEXT:
        {original_text[:4000]}
        
        PREVIOUS FEEDBACK:
        {feedback_text}
        
        Create samples that follow the style of positively rated examples, while avoiding characteristics of negatively rated ones.
        Each sample should be about 250 words and should represent content the user might write.
        
        Return your response as a JSON object with this structure:
        {{
            "style_analysis": {{
                "adjusted_characteristics": [list of characteristics after feedback],
                "avoided_patterns": [patterns avoided based on negative feedback]
            }},
            "samples": [
                {{
                    "id": {max([s.get("id", 0) for s in previous_samples_list], default=0) + 1},
                    "sample_text": "First sample text here...",
                    "topic": "Brief topic description"
                }},
                ...repeat for all samples...
            ]
        }}
        """
    def process_sample_feedback(self, sample_id: int, rating: str, comments: str = "", regenerate: bool = False, num_samples: int = 1):
        """Process feedback on style samples and optionally regenerate new samples
        
        Args:
            sample_id: ID of the sample that received feedback
            rating: Feedback rating ('upvote' or 'downvote')
            comments: Optional comments explaining the feedback
            regenerate: Whether to generate new samples based on feedback
            num_samples: Number of new samples to generate if regenerating
            
        Returns:
            Dictionary with feedback status and optionally new samples
        """
        try:
            import time
            # Record the feedback
            feedback = {
                "sample_id": sample_id,
                "rating": rating,
                "comments": comments,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            self.logger.info(f"Received {rating} feedback for sample {sample_id}: {comments}")
            
            # If regeneration is not requested, just acknowledge the feedback
            if not regenerate:
                return {
                    "status": "success",
                    "message": "Feedback recorded successfully"
                }
            
            # If regeneration is requested, generate new samples based on feedback
            regenerate_prompt = f"""
            Generate {num_samples} new writing style samples based on the following feedback:
            
            Rating: {rating}
            Comments: {comments}
            
            If this was an upvote, emphasize the positive aspects mentioned.
            If this was a downvote, adjust to avoid the negative aspects mentioned.
            
            Generate a style analysis first, then the samples. Return your response in JSON format with the structure:
            {{
                "adjusted_characteristics": ["list", "of", "style", "characteristics"],
                "avoided_patterns": ["list", "of", "patterns", "to", "avoid"],
                "samples": [
                    {{"id": {sample_id + 1}, "topic": "Topic Name", "sample_text": "Sample text here..."}},
                    {{"id": {sample_id + 2}, "topic": "Another Topic", "sample_text": "Another sample..."}}
                ]
            }}
            """
            
            regen_response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a skilled writer who can adapt writing styles based on feedback. Generate new samples that incorporate the feedback given." },
                    {"role": "user", "content": regenerate_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )
            
            # Parse the regenerated samples
            regeneration_result = json.loads(regen_response.choices[0].message.content)
            
            # Return the regenerated samples with feedback acknowledgment
            return {
                "status": "success",
                "message": "Feedback processed and new samples generated",
                "style_analysis": {
                    "adjusted_characteristics": regeneration_result.get("adjusted_characteristics", []),
                    "avoided_patterns": regeneration_result.get("avoided_patterns", [])
                },
                "samples": regeneration_result.get("samples", [])
            }
            
        except Exception as e:
            self.logger.error(f"Error processing sample feedback: {e}")
            return {
                "status": "error",
                "message": f"Error processing feedback: {str(e)}"
            }
