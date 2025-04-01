"""
Advanced Style Fingerprinter Demonstration

This script showcases the capabilities of the AdvancedStyleFingerprinter
by analyzing different text styles and generating comprehensive style metrics.
"""

import json
import numpy as np
from app.tone_adaptation.advanced_style_fingerprinter import AdvancedStyleFingerprinter

def print_style_analysis(text: str, title: str = "Text Analysis"):
    """
    Analyze and print style metrics for a given text
    
    Args:
        text (str): Text to analyze
        title (str): Title for the analysis section
    """
    fingerprinter = AdvancedStyleFingerprinter()
    
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    print(f"Original Text: {text}\n")
    
    # Perform style analysis
    style_metrics = fingerprinter.analyze_style(text)
    
    # Pretty print the metrics
    print("Style Metrics:")
    for key, value in style_metrics.items():
        if key == 'style_embedding':
            # Special handling for embedding
            print(f"Style Embedding: {value[:5]}... (truncated, total length: {len(value)})")
        elif isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")
    
    return style_metrics

def compare_style_embeddings(texts):
    """
    Compare style embeddings across multiple texts
    
    Args:
        texts (List[str]): Texts to compare
    """
    print("\n\n" + "="*50)
    print("Style Embedding Comparison")
    print("="*50)
    
    fingerprinter = AdvancedStyleFingerprinter()
    
    # Compute embeddings
    embeddings = [fingerprinter.analyze_style(text)['style_embedding'] for text in texts]
    
    # Compute cosine similarities
    def safe_cosine_similarity(a, b):
        """Compute cosine similarity with robust error handling"""
        a, b = np.array(a), np.array(b)
        
        # Remove any non-finite values
        a = np.nan_to_num(a, nan=0.0, posinf=0.0, neginf=0.0)
        b = np.nan_to_num(b, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Compute norms
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        
        # Prevent division by zero
        if norm_a == 0 or norm_b == 0:
            return 0.0
        
        return np.dot(a, b) / (norm_a * norm_b)
    
    print("\nCosine Similarities:")
    for i in range(len(texts)):
        for j in range(i+1, len(texts)):
            sim = safe_cosine_similarity(embeddings[i], embeddings[j])
            print(f"Text {i+1} vs Text {j+1}: {sim:.4f}")
            
    # Visualize embedding differences
    print("\nEmbedding Visualization:")
    for i, emb in enumerate(embeddings, 1):
        print(f"Text {i} Embedding (first 5 dims): {emb[:5]}")

def main():
    # Diverse text samples
    texts = [
        # 1. Academic/Formal Text
        "The quantum computing paradigm represents a significant breakthrough in computational complexity theory. Researchers have demonstrated remarkable progress in developing quantum algorithms that can solve complex problems exponentially faster than classical computing methods.",
        
        # 2. Casual/Conversational Text
        "Hey, what's up? I was just thinking about how crazy technology is getting. Like, quantum computers are basically magic at this point, right? It's wild how fast things are changing!",
        
        # 3. Technical/Professional Text
        "In the domain of advanced computational methodologies, quantum computing emerges as a transformative technological innovation. The intrinsic quantum mechanical properties enable unprecedented computational capabilities, challenging traditional algorithmic constraints.",
        
        # 4. Journalistic Text
        "Scientists at the forefront of quantum computing research are pushing the boundaries of what was once thought impossible. Their groundbreaking work promises to revolutionize fields ranging from cryptography to drug discovery.",
        
        # 5. Creative/Narrative Text
        "Imagine a world where computers think not in rigid, linear paths, but in fluid, probabilistic waves. Quantum computing isn't just a technology; it's a glimpse into a reality where computation dances with uncertainty."
    ]
    
    # Analyze each text
    style_metrics = []
    for i, text in enumerate(texts, 1):
        print(f"\n\nAnalyzing Text {i}:")
        metrics = print_style_analysis(text, f"Text {i} Style Analysis")
        style_metrics.append(metrics)
    
    # Compare style embeddings
    compare_style_embeddings(texts)
    
    # Optional: Save detailed metrics to a JSON file
    with open('/root/socialme/social-me-test-2/style_metrics_demo.json', 'w') as f:
        json.dump(style_metrics, f, indent=2)
    
    print("\nDetailed style metrics saved to style_metrics_demo.json")

if __name__ == '__main__':
    main()
