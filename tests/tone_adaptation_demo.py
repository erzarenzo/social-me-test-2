#!/usr/bin/env python3
"""
Demonstration Script for Advanced Tone Adaptation System in SocialMe

This script showcases the capabilities of the Enhanced Tone Adaptation System,
highlighting its ability to:
1. Analyze writing styles from multiple sources
2. Generate style-matched content
3. Provide comprehensive tone analysis
"""

import sys
import os
import json

# Ensure the project root is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, project_root)

from complete_workflow_test import EnhancedWorkflowTest

def main():
    print("\n" + "="*80)
    print("🚀 SocialMe: Advanced Tone Adaptation System Demonstration")
    print("="*80 + "\n")

    # Initialize the enhanced workflow
    workflow = EnhancedWorkflowTest(test_mode=False)

    # Demonstrate tone source collection and analysis
    print("\n📝 STEP 1: Tone Source Collection")
    print("-"*40)
    print("For this demo, we'll analyze writing styles from different sources.")
    print("You'll be prompted to enter URLs, text, or file paths.")
    print("Example sources could be:")
    print("- A professional blog post")
    print("- A news article")
    print("- A personal essay")
    print("- A technical documentation page\n")

    # Simulate user interaction for tone source processing
    workflow.tone_sources = [
        "https://www.newyorker.com/magazine/2023/06/05/the-art-of-storytelling",  # Literary style
        "https://techcrunch.com/2023/05/15/ai-innovation-trends/",  # Tech journalism
        "/path/to/personal/essay.txt"  # Personal writing sample
    ]

    # Perform tone analysis
    print("\n🔍 STEP 2: Advanced Tone Analysis")
    print("-"*40)
    tone_analysis = workflow.tone_mapper.analyze_tone(workflow.tone_sources)
    
    # Pretty print tone analysis
    print("\nComprehensive Tone Analysis Results:")
    print(json.dumps(tone_analysis, indent=2))

    # Generate style prompt
    style_prompt = workflow.tone_mapper.generate_style_prompt(tone_analysis)
    print("\n✨ Generated Style Prompt:")
    print(style_prompt)

    # Simulate article generation
    print("\n📄 STEP 3: Style-Guided Article Generation")
    print("-"*40)
    topic = "The Future of AI in Creative Writing"
    
    # Simulate article generation with style matching
    article_generator = workflow.generate_advanced_article()
    
    print("\n🏆 Generated Article Details:")
    print(f"Title: {article_generator.get('title', 'Untitled')}")
    print(f"Word Count: {len(article_generator.get('content', '').split())}")
    
    # Optional: Style validation
    print("\n🧐 Style Validation")
    print("-"*40)
    validation_results = workflow.tone_mapper.validate_style(
        original_sources=workflow.tone_sources,
        generated_article=article_generator
    )
    
    print("\nStyle Validation Metrics:")
    print(json.dumps(validation_results, indent=2))

if __name__ == "__main__":
    main()
