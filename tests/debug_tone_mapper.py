#!/usr/bin/env python3
import sys
import os

# Add the current directory to the path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("Importing NeuralToneMapper...")
    from app.neural_tone_mapper import NeuralToneMapper
    
    # Create an instance
    print("Creating NeuralToneMapper instance...")
    mapper = NeuralToneMapper()
    
    # Test with sample text
    sample_text = "This is a sample text for testing the NeuralToneMapper. The SocialMe application needs to analyze user content effectively."
    
    print(f"Analyzing text: {sample_text[:50]}...")
    result = mapper.analyze_text(sample_text)
    
    print("Analysis result keys:", result.keys())
    print("Thought patterns:", result.get("thought_patterns", {}))
    print("Reasoning style:", result.get("reasoning_style", {}))
    
    print("NeuralToneMapper test completed successfully!")
except Exception as e:
    import traceback
    print(f"ERROR: {str(e)}")
    traceback.print_exc()
