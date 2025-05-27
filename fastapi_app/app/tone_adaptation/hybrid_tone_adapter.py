"""
Hybrid Tone Adapter

Provides a unified interface to both the original spaCy-based 
AdvancedToneAdapter and the new OpenAI-based ToneAnalyzer
"""

import logging
import sys
from typing import Dict, Any, Optional, Union, List

# Setup logging
logger = logging.getLogger("app.tone_adaptation.hybrid_tone_adapter")

class HybridToneAdapter:
    """
    Hybrid adapter that tries OpenAI first, then falls back to local analyzer if needed
    """
    def __init__(self, force_openai=True):
        """
        Initialize the hybrid adapter
        
        Args:
            force_openai: If True, only use OpenAI and don't fall back to local analyzer
        """
        self.logger = logger
        self.force_openai = force_openai
        
        # Initialize OpenAI analyzer using direct import to avoid dependency issues
        try:
            # Direct import by loading module from file
            import os
            import importlib.util
            import sys
            
            # Get the current file's directory
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Load the OpenAIToneAnalyzer module directly
            analyzer_path = os.path.join(current_dir, 'openai_tone_analyzer.py')
            spec = importlib.util.spec_from_file_location("openai_tone_analyzer", analyzer_path)
            openai_tone_analyzer = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(openai_tone_analyzer)
            
            # Create an instance of the analyzer
            self.openai_analyzer = openai_tone_analyzer.OpenAIToneAnalyzer()
            self.logger.info("OpenAI tone analyzer initialized")
        except Exception as e:
            self.openai_analyzer = None
            self.logger.error(f"Error initializing OpenAI tone analyzer: {e}")
        
        # Initialize local analyzer (lazy loading to avoid unnecessary imports)
        self.local_analyzer = None
        if not force_openai:
            try:
                from .tone_adapter import AdvancedToneAdapter
                self.local_analyzer = AdvancedToneAdapter()
                self.logger.info("Local tone analyzer initialized as fallback")
            except ImportError as e:
                self.logger.warning(f"Could not initialize local tone analyzer: {e}")
    
    def analyze_tone(self, 
                     sample_text: Optional[str] = None, 
                     url: Optional[str] = None,
                     document_content: Optional[str] = None) -> Dict[str, Any]:
        """
        Analyze tone with OpenAI first, fall back to local analyzer if needed
        """
        # Try OpenAI first
        try:
            if self.openai_analyzer:
                result = self.openai_analyzer.analyze_tone(
                    sample_text=sample_text,
                    url=url,
                    document_content=document_content
                )
                
                if result.get("status") == "success":
                    return result
                
                if self.force_openai:
                    # If OpenAI is forced but failed, return the error
                    return result
            elif self.force_openai:
                return {
                    "status": "error",
                    "message": "OpenAI analyzer not initialized and fallback is disabled"
                }
                
        except Exception as e:
            self.logger.error(f"Error in OpenAI tone analysis: {e}")
            if self.force_openai:
                return {
                    "status": "error",
                    "message": f"OpenAI tone analysis failed: {str(e)}"
                }
        
        # Fall back to local analyzer if available
        if self.local_analyzer:
            try:
                self.logger.info("Falling back to local tone analyzer")
                # Determine which source to use
                if sample_text:
                    # The original tone adapter had different method signatures
                    # We're adapting here for backward compatibility
                    return self.local_analyzer.analyze_text(sample_text)
                elif url:
                    # Local adapter may have different method for URLs
                    # This would need to be adapted based on the local implementation
                    from ..quantum_tone_crawler import QuantumToneCrawler
                    crawler = QuantumToneCrawler()
                    extracted_content = crawler.extract_content_from_url(url)
                    return self.local_analyzer.analyze_text(extracted_content)
                elif document_content:
                    return self.local_analyzer.analyze_text(document_content)
                else:
                    return {
                        "status": "error",
                        "message": "No valid content provided for tone analysis"
                    }
            except Exception as e:
                self.logger.error(f"Error in local tone analysis fallback: {e}")
                return {
                    "status": "error",
                    "message": f"Both OpenAI and local tone analysis failed: {str(e)}"
                }
        
        return {
            "status": "error",
            "message": "No tone analyzers available"
        }
    
    def generate_style_samples(self,
                              sample_text: str,
                              num_samples: int = 3,
                              target_length: int = 250) -> Dict[str, Any]:
        """
        Generate multiple writing style samples based on the provided text
        
        Note: This feature is only available with the OpenAI analyzer
        """
        if not self.openai_analyzer:
            return {
                "status": "error",
                "message": "Style sample generation requires OpenAI analyzer"
            }
        
        try:
            return self.openai_analyzer.generate_style_samples(
                sample_text=sample_text,
                num_samples=num_samples,
                target_length=target_length
            )
        except Exception as e:
            self.logger.error(f"Error generating style samples: {e}")
            return {
                "status": "error",
                "message": f"Error generating style samples: {str(e)}"
            }
    
    def regenerate_style_samples(self,
                                previous_samples: Dict[str, Any],
                                feedback: List[Dict[str, Any]],
                                num_samples: int = 3) -> Dict[str, Any]:
        """
        Regenerate style samples based on previous samples and user feedback
        
        Note: This feature is only available with the OpenAI analyzer
        """
        if not self.openai_analyzer:
            return {
                "status": "error",
                "message": "Style sample regeneration requires OpenAI analyzer"
            }
        
        try:
            return self.openai_analyzer.regenerate_style_samples(
                previous_samples=previous_samples,
                feedback=feedback,
                num_samples=num_samples
            )
        except Exception as e:
            self.logger.error(f"Error regenerating style samples: {e}")
            return {
                "status": "error",
                "message": f"Error regenerating style samples: {str(e)}"
            }
