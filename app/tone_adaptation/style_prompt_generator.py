"""
Style Prompt Generator for Advanced Tone Adaptation

Converts style fingerprints to natural language instructions for LLM article generation.
"""

import logging
import numpy as np
from typing import Dict, Any, List

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("style_prompt_generator")

class StylePromptGenerator:
    """
    Converts style fingerprints to natural language instructions
    for LLM article generation
    """
    
    def __init__(self):
        """Initialize the StylePromptGenerator"""
        self.logger = logging.getLogger("style_prompt_generator")
    
    @staticmethod
    def generate_style_prompt(style_fingerprint: Dict[str, Any]) -> str:
        """
        Generate a detailed style prompt based on the style fingerprint
        
        Args:
            style_fingerprint (Dict[str, Any]): Extracted style metrics
        
        Returns:
            str: Detailed style prompt
        """
        logger.info("Generating style prompt from fingerprint")
        
        # Handle empty or invalid fingerprint
        if not style_fingerprint or all(value == 0 for value in style_fingerprint.values()):
            return "Write in a clear, professional, and objective manner."
        
        # Sentence length guidance
        avg_sentence_length = style_fingerprint.get('avg_sentence_length', 20)
        sentence_length_guidance = (
            f"Use sentences with an average length of around {avg_sentence_length:.1f} words. "
            "Maintain consistent sentence structure and complexity."
        )
        
        # Vocabulary diversity guidance
        vocab_diversity = style_fingerprint.get('vocabulary_diversity', 0.5)
        vocab_guidance = (
            f"Aim for a vocabulary diversity index of {vocab_diversity:.2f}. "
            "Use a rich and varied vocabulary while maintaining clarity."
        )
        
        # Pronoun usage guidance
        first_person_singular_freq = style_fingerprint.get('first_person_singular', 0)
        first_person_plural_freq = style_fingerprint.get('first_person_plural', 0)
        second_person_freq = style_fingerprint.get('second_person', 0)
        
        pronoun_guidance = "Maintain a primarily third-person perspective. "
        if first_person_singular_freq > 0:
            pronoun_guidance += f"Use first-person singular pronouns sparingly (current frequency: {first_person_singular_freq*100:.2f}%). "
        if first_person_plural_freq > 0:
            pronoun_guidance += f"Limit first-person plural pronouns (current frequency: {first_person_plural_freq*100:.2f}%). "
        if second_person_freq > 0:
            pronoun_guidance += f"Minimize second-person pronouns (current frequency: {second_person_freq*100:.2f}%). "
        
        # Tone and style guidance
        question_freq = style_fingerprint.get('question_frequency', 0)
        exclamation_freq = style_fingerprint.get('exclamation_frequency', 0)
        formality_score = style_fingerprint.get('formality_score', 0.5)
        
        if exclamation_freq > 0.15:
            tone_guidance = "Adopt an enthusiastic, exclamatory tone approach. "
        elif question_freq > 0.15:
            tone_guidance = "Adopt an inquisitive tone with frequent questions. "
        else:
            tone_guidance = "Adopt a measured, even tone approach. "
        
        if formality_score > 0.7:
            tone_guidance += "Write in a formal and academic style. "
        elif formality_score < 0.3:
            tone_guidance += "Write in a conversational and informal style. "
        else:
            tone_guidance += "Write in a balanced, semi-formal tone. "
        
        tone_guidance += "Write with an objective and analytical perspective. Ensure the writing flows smoothly and maintains professional credibility."
        
        # Combine all guidance
        style_prompt = (
            f"Write in a style that uses {sentence_length_guidance} {vocab_guidance} {pronoun_guidance} {tone_guidance}"
        )
        
        return style_prompt.strip()
    
    def generate_claude_system_prompt(self, topic: str, style_prompt: str, sample_text: str = None, facts: List[str] = None) -> str:
        """
        Generate a complete system prompt for Claude
        
        Args:
            topic: The article topic
            style_prompt: The style instructions
            sample_text: Optional sample of the target style
            facts: Optional list of facts to include
            
        Returns:
            String containing the complete system prompt
        """
        # Format facts as bulleted list if provided
        facts_text = ""
        if facts:
            facts_text = "FACTUAL CONTENT TO INCLUDE:\n" + "\n".join([f"• {fact}" for fact in facts])
        
        # Build the prompt with style guidance
        if sample_text:
            system_prompt = f"""
You are an expert content writer tasked with writing an article about {topic} that perfectly mimics a specific writing style.

STYLE INSTRUCTIONS:
{style_prompt}

SAMPLE OF TARGET STYLE:
{sample_text[:1000]}

{facts_text}

IMPORTANT GUIDELINES:
1. Your primary goal is to match the writing style EXACTLY while covering the topic.
2. Focus on sentence structure, word choice, perspective, and tone that matches the sample.
3. Incorporate all relevant facts naturally within this style.
4. The final article should be indistinguishable from something the original author would write.
5. Do not mention or refer to these instructions in your output.
"""
        else:
            system_prompt = f"""
You are an expert content writer tasked with writing an article about {topic} according to specific style parameters.

STYLE INSTRUCTIONS:
{style_prompt}

{facts_text}

IMPORTANT GUIDELINES:
1. Your primary goal is to follow the style instructions EXACTLY while covering the topic.
2. Focus on sentence structure, word choice, perspective, and tone as specified.
3. Incorporate all relevant facts naturally within this style.
4. Do not mention or refer to these instructions in your output.
"""
        
        return system_prompt
