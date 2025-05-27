import requests
import json
import logging
import os
import openai
from fastapi_app.app.config.api_config import get_openai_api_key

class EnhancedArticleGenerator:
    def __init__(self):
        self.logger = logging.getLogger("article_generator")
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(handler)
        
        # Set up OpenAI API key
        openai.api_key = get_openai_api_key()
        self.logger.info("EnhancedArticleGenerator initialized with OpenAI API key")
    
    def generate_article(self, article_input):
        """Generate an article based on the topic and tone analysis data using a section-based approach."""
        
        topic = article_input.get("topic", "General Topic")
        title = article_input.get("title", f"Article about {topic}")
        target_word_count = article_input.get("target_word_count", 4000)  # Increased default target
        source_material = article_input.get("source_material", [])
        
        # Check if we have the enhanced Universal Voice Pattern Extraction data
        if "voice_pattern" in article_input and article_input.get("use_enhanced_tone", False):
            self.logger.info("Using Universal Voice Pattern Extraction data for article")
            voice_pattern = article_input["voice_pattern"]
            
            # Extract key voice elements for prompt construction
            voice_elements = self._extract_voice_elements(voice_pattern)
            
            # Build a detailed prompt with the voice pattern guidance
            system_prompt = self._build_voice_guided_system_prompt(voice_elements)
            
            self.logger.info(f"Generating article about '{topic}' using detailed voice pattern")
        else:
            # Fallback to basic tone style if no enhanced voice pattern
            tone_analysis = article_input.get("tone_analysis", {})
            tone_style = tone_analysis.get('neural_tone_analysis', {}).get('tone', 'informative')
            self.logger.info(f"Using basic tone style: {tone_style} for article generation")
            
            # Build basic prompts
            system_prompt = f"You are a professional content writer who specializes in writing in a {tone_style} tone."
            voice_elements = {"dominant_tone": tone_style}
        
        try:
            # STEP 1: Generate the detailed outline first
            self.logger.info("STEP 1: Generating detailed article outline")
            outline = self._generate_article_outline(topic, title, system_prompt, voice_elements)
            
            # STEP 2: Generate content for each section based on the outline
            self.logger.info("STEP 2: Generating content for each section based on outline")
            sections = self._extract_sections_from_outline(outline)
            
            # Generate content for each section
            section_contents = {}
            for section_num, section in enumerate(sections):
                section_content = self._generate_section_content(
                    topic=topic,
                    section_title=section,
                    section_num=section_num,
                    total_sections=len(sections),
                    system_prompt=system_prompt,
                    voice_elements=voice_elements
                )
                section_contents[section] = section_content
                self.logger.info(f"Generated content for section: {section} ({len(section_content.split())} words)")
            
            # STEP 3: Assemble the complete article draft
            self.logger.info("STEP 3: Assembling complete article draft")
            article_draft = self._assemble_article(outline, section_contents, title)
            initial_word_count = len(article_draft.split())
            self.logger.info(f"Initial article draft assembled with {initial_word_count} words")
            
            # STEP 4: Enhance the article with additional elements
            self.logger.info("STEP 4: Enhancing article with additional elements")
            enhanced_article = self._enhance_article_with_elements(
                topic=topic,
                initial_article=article_draft,
                target_word_count=target_word_count,
                voice_elements=voice_elements,
                source_material=source_material
            )
            
            final_word_count = len(enhanced_article.split())
            
            # Format the result
            result = {
                "text": enhanced_article,
                "title": title,
                "metadata": {
                    "word_count": final_word_count,
                    "reading_time": f"{final_word_count // 250} min",  # Assuming 250 words per minute
                    "sectioned_generation": True,
                    "enhancement_applied": True,
                    "sections_generated": len(sections)
                }
            }
            
            if "voice_pattern" in article_input:
                result["metadata"]["voice_pattern_applied"] = True
            
            self.logger.info(f"Successfully generated enhanced sectioned article with {final_word_count} words")
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating article: {str(e)}")
            raise Exception(f"Article generation failed: {str(e)}")
    
    def _generate_article_outline(self, topic, title, system_prompt, voice_elements):
        """Generate a detailed outline for the article with sections and subsections."""
        outline_prompt = f"""Create a detailed outline for a comprehensive article about {topic} with the title: '{title}'.
        
Include the following in your outline:
1. An introduction section
2. At least 5-7 main sections with descriptive headings
3. 2-3 subsections under each main section where appropriate
4. A conclusion section

Format your response as a structured outline with Markdown headings (# for title, ## for main sections, ### for subsections).
DO NOT write any actual content - ONLY provide the outline structure with headings."""
        
        # Add tone guidance if available
        if voice_elements.get("dominant_tone"):
            outline_prompt += f"\n\nEnsure the section headings reflect a {voice_elements['dominant_tone']} tone."
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": outline_prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        outline = response.choices[0].message.content
        return outline
    
    def _extract_sections_from_outline(self, outline):
        """Extract main section headings from the outline."""
        sections = []
        for line in outline.split('\n'):
            # Look for level 2 headings (##) which represent main sections
            if line.strip().startswith('## '):
                section_title = line.strip()[3:].strip()  # Remove ## and any trailing/leading spaces
                sections.append(section_title)
        
        # If no sections were found (perhaps formatting was different), return a basic structure
        if not sections:
            sections = ["Introduction", "Overview", "Applications", "Challenges", "Future Perspectives", "Conclusion"]
        
        return sections
    
    def _generate_section_content(self, topic, section_title, section_num, total_sections, system_prompt, voice_elements):
        """Generate content for a specific section of the article."""
        # Determine the type of section based on its position
        section_type = "introduction" if section_num == 0 else "conclusion" if section_num == total_sections - 1 else "body"
        
        section_prompt = f"""Write detailed content for the '{section_title}' section of an article about {topic}.
        
This is section {section_num + 1} of {total_sections} in the article.
"""
        
        # Add specific instructions based on section type
        if section_type == "introduction":
            section_prompt += "\nThis is the introduction section. Provide a compelling opening that establishes the importance of the topic and outlines what the article will cover."
        elif section_type == "conclusion":
            section_prompt += "\nThis is the conclusion section. Summarize the key points discussed in the article and provide forward-looking statements or calls to action."
        else:
            section_prompt += f"\nThis is a main body section on '{section_title}'. Include detailed information, examples, and data points relevant to this specific aspect of the topic."
        
        # Add content structure guidance
        section_prompt += """
        
Include the following elements in your section content:
- Detailed explanations with specific examples
- Statistical data or research findings where relevant
- Bullet points for listing important information
- At least one expert perspective or quote (you may create these based on factual information)

Format the content with proper Markdown, including the section heading.
"""
        
        # Add tone guidance if available
        if voice_elements.get("dominant_tone"):
            section_prompt += f"\n\nMaintain a {voice_elements['dominant_tone']} tone throughout the section."
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": section_prompt}
            ],
            temperature=0.7,
            max_tokens=4000  # Allocate substantial tokens per section
        )
        
        section_content = response.choices[0].message.content
        return section_content
    
    def _assemble_article(self, outline, section_contents, title):
        """Assemble the complete article from the outline and section contents."""
        # Start with the title
        article = f"# {title}\n\n"
        
        # Add an introductory paragraph if we have an Introduction section
        if "Introduction" in section_contents:
            article += section_contents["Introduction"]
        
        # Process each section from the section_contents
        for section, content in section_contents.items():
            if section != "Introduction":  # Skip introduction as we already added it
                # Check if the content already includes the section heading
                if not content.strip().startswith(f"## {section}") and not content.strip().startswith(f"##{section}"):
                    article += f"\n\n## {section}\n\n"
                article += content
        
        return article
    
    def _extract_voice_elements(self, voice_pattern):
        """Extract key elements from the voice pattern for prompt construction."""
        elements = {}
        
        # Extract core voice attributes
        if "PART 1: PERSONA & POSITIONING" in voice_pattern:
            elements["core_identity"] = voice_pattern["PART 1: PERSONA & POSITIONING"].get("Core Identity", "")
            elements["key_characteristics"] = voice_pattern["PART 1: PERSONA & POSITIONING"].get("Key Writing Characteristics", [])
        
        # Extract voice and tone specifications
        if "PART 2: VOICE & TONE SPECIFICATIONS" in voice_pattern:
            elements["voice_attributes"] = voice_pattern["PART 2: VOICE & TONE SPECIFICATIONS"].get("Core Voice Attributes", [])
            elements["dominant_tone"] = voice_pattern["PART 2: VOICE & TONE SPECIFICATIONS"].get("Dominant Tone", "")
        
        # Extract linguistic patterns
        if "PART 3: LINGUISTIC PATTERNS" in voice_pattern:
            elements["sentence_structure"] = voice_pattern["PART 3: LINGUISTIC PATTERNS"].get("Sentence Structure", "")
            elements["paragraph_construction"] = voice_pattern["PART 3: LINGUISTIC PATTERNS"].get("Paragraph Construction", "")
            elements["pronoun_usage"] = voice_pattern["PART 3: LINGUISTIC PATTERNS"].get("Pronoun Usage", "")
        
        # Extract content structure
        if "PART 5: CONTENT STRUCTURE" in voice_pattern:
            elements["overall_framework"] = voice_pattern["PART 5: CONTENT STRUCTURE"].get("Overall Framework", "")
            elements["conclusion_approaches"] = voice_pattern["PART 5: CONTENT STRUCTURE"].get("Conclusion Approaches", "")
        
        # Extract vocabulary guidance
        if "PART 10: VOCABULARY & PHRASING GUIDE" in voice_pattern:
            elements["power_words"] = voice_pattern["PART 10: VOCABULARY & PHRASING GUIDE"].get("Power Words & Phrases", [])
            elements["terms_to_avoid"] = voice_pattern["PART 10: VOCABULARY & PHRASING GUIDE"].get("Terms & Phrases to Avoid", [])
        
        return elements
    
    def _build_voice_guided_system_prompt(self, voice_elements):
        """Build a detailed system prompt using the voice elements."""
        system_prompt = "You are a professional content writer who specializes in writing with very specific voice and style characteristics.\n\n"
        
        # Add core identity and characteristics
        if voice_elements.get("core_identity"):
            system_prompt += f"CORE IDENTITY: {voice_elements['core_identity']}\n\n"
        
        if voice_elements.get("key_characteristics"):
            system_prompt += "KEY WRITING CHARACTERISTICS:\n"
            for char in voice_elements.get("key_characteristics", []):
                system_prompt += f"- {char}\n"
            system_prompt += "\n"
        
        # Add voice attributes
        if voice_elements.get("voice_attributes"):
            system_prompt += "VOICE ATTRIBUTES:\n"
            for attr in voice_elements.get("voice_attributes", []):
                system_prompt += f"- {attr}\n"
            system_prompt += "\n"
        
        # Add linguistic guidance
        system_prompt += "WRITING PATTERNS:\n"
        if voice_elements.get("sentence_structure"):
            system_prompt += f"- Sentence Structure: {voice_elements['sentence_structure']}\n"
        if voice_elements.get("paragraph_construction"):
            system_prompt += f"- Paragraph Construction: {voice_elements['paragraph_construction']}\n"
        if voice_elements.get("pronoun_usage"):
            system_prompt += f"- Pronoun Usage: {voice_elements['pronoun_usage']}\n"
        system_prompt += "\n"
        
        # Add vocabulary guidance
        if voice_elements.get("power_words"):
            system_prompt += "VOCABULARY TO USE:\n"
            for word in voice_elements.get("power_words", []):
                system_prompt += f"- {word}\n"
            system_prompt += "\n"
        
        if voice_elements.get("terms_to_avoid"):
            system_prompt += "TERMS TO AVOID:\n"
            for term in voice_elements.get("terms_to_avoid", []):
                system_prompt += f"- {term}\n"
            system_prompt += "\n"
        
        system_prompt += "Your writing must faithfully represent these voice characteristics in every paragraph and sentence."
        return system_prompt
    
    def _build_enhanced_article_prompt(self, topic, title, voice_elements, target_word_count=2500):
        """Build an enhanced user prompt for article generation with specific structural elements."""
        prompt = f"Write a comprehensive, authoritative article about {topic}. The title should be: {title}.\n\n"
        
        # Add structure guidance
        if voice_elements.get("overall_framework"):
            prompt += f"Structure the article following this pattern: {voice_elements['overall_framework']}\n\n"
        else:
            prompt += "Structure the article with a clear introduction, multiple substantive sections with headings and subheadings, and a conclusion.\n\n"
        
        # Add tone guidance
        if voice_elements.get("dominant_tone"):
            prompt += f"The tone should be: {voice_elements['dominant_tone']}\n\n"
        
        # Add specific content element requirements
        prompt += "IMPORTANT: Include the following elements in your article:\n"
        prompt += "1. At least 3 real-world case studies or examples with specific details\n"
        prompt += "2. Multiple bullet-point lists to break down complex information\n"
        prompt += "3. Direct quotes from experts or authoritative sources (you may create these quotes based on factual information)\n"
        prompt += "4. Statistical data points and research findings to support key points\n"
        prompt += "5. Clear section headings and subheadings for organization\n"
        prompt += "6. A conclusion with specific calls to action\n\n"
        
        # Add conclusion guidance
        if voice_elements.get("conclusion_approaches"):
            prompt += f"End the article using this approach: {voice_elements['conclusion_approaches']}\n\n"
        
        prompt += f"Make sure the article is well-researched, authoritative, and at least {target_word_count} words with proper markdown formatting."
        return prompt
        
    def _enhance_article_with_elements(self, topic, initial_article, target_word_count, voice_elements, source_material=[]):
        """Enhance an article with additional elements like case studies, quotes, statistics, and more."""
        # Check if the article is already detailed enough
        current_word_count = len(initial_article.split())
        if current_word_count >= target_word_count:
            self.logger.info(f"Article already meets target word count ({current_word_count} words). Skipping enhancement.")
            return initial_article
        
        self.logger.info(f"Enhancing article from {current_word_count} words toward target of {target_word_count} words")
        
        # Build the enhancement prompt
        enhancement_prompt = f"""I have an article about {topic} that needs enhancement with additional elements.

Current article:
{initial_article}

Please enhance this article by adding the following elements while maintaining the existing content and structure:

1. CASE STUDIES: Add 2-3 detailed real-world case studies or examples with specific outcomes
2. EXPERT QUOTES: Insert relevant expert quotes to support key points
3. STATISTICS & DATA: Include additional statistics and research findings
4. BULLET POINT LISTS: Convert appropriate paragraphs into bullet point lists for better readability
5. CALLS TO ACTION: Strengthen the conclusion with specific, actionable recommendations

The enhanced article should maintain the same tone and voice but be more comprehensive and detailed.
Ensure the final article is well-structured with proper markdown formatting."""

        try:
            # If we have voice elements, add tone guidance
            tone_instruction = ""
            if voice_elements.get("dominant_tone"):
                tone_instruction = f"\n\nMaintain a {voice_elements['dominant_tone']} tone throughout the enhancements."
            
            if voice_elements.get("power_words") and len(voice_elements.get("power_words", [])) > 0:
                power_words = ", ".join(voice_elements.get("power_words", [])[:5])  # Use up to 5 power words
                tone_instruction += f"\n\nIncorporate powerful words and phrases like: {power_words}"
            
            enhancement_prompt += tone_instruction
            
            # Generate the enhanced article
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert content enhancer who specializes in transforming articles into more comprehensive, engaging, and detailed content while maintaining the original structure and tone."},
                    {"role": "user", "content": enhancement_prompt}
                ],
                temperature=0.7,
                max_tokens=8000
            )
            
            enhanced_article = response.choices[0].message.content
            enhanced_word_count = len(enhanced_article.split())
            
            self.logger.info(f"Successfully enhanced article from {current_word_count} to {enhanced_word_count} words")
            return enhanced_article
            
        except Exception as e:
            self.logger.error(f"Error enhancing article: {str(e)}")
            # If enhancement fails, return the original article
            return initial_article


if __name__ == "__main__":
    generator = EnhancedArticleGenerator()
    result = generator.generate_article({"topic": "The Future of AI"})
    print(result["text"])
