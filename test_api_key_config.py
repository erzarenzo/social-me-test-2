#!/usr/bin/env python3
"""
Test script to verify the API key configuration system works correctly.
This will check all available methods for accessing API keys.
"""
import os
import sys
import json
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

def test_env_variables():
    """Test API keys from environment variables"""
    print("\n=== Testing Environment Variables ===")
    openai_key = os.environ.get("OPENAI_API_KEY")
    anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
    
    print(f"OpenAI API key in environment: {'Yes' if openai_key else 'No'}")
    if openai_key:
        print(f"OpenAI API key format valid: {'Yes' if openai_key.startswith('sk-') else 'No'}")
    
    print(f"Anthropic API key in environment: {'Yes' if anthropic_key else 'No'}")
    if anthropic_key:
        print(f"Anthropic API key format valid: {'Yes' if anthropic_key.startswith('sk-ant-') else 'No'}")

def test_config_file():
    """Test API keys from config file"""
    print("\n=== Testing Configuration File ===")
    config_file = project_root / "config" / "api_keys.json"
    
    if not config_file.exists():
        print(f"Configuration file not found at {config_file}")
        return
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            
        openai_key = config.get("OPENAI_API_KEY")
        anthropic_key = config.get("ANTHROPIC_API_KEY")
        
        print(f"OpenAI API key in config file: {'Yes' if openai_key else 'No'}")
        if openai_key:
            print(f"OpenAI API key format valid: {'Yes' if openai_key.startswith('sk-') else 'No'}")
        
        print(f"Anthropic API key in config file: {'Yes' if anthropic_key else 'No'}")
        if anthropic_key:
            print(f"Anthropic API key format valid: {'Yes' if anthropic_key.startswith('sk-ant-') else 'No'}")
    
    except Exception as e:
        print(f"Error reading config file: {e}")

def test_api_config_module():
    """Test the API configuration module"""
    print("\n=== Testing API Configuration Module ===")
    try:
        # Import our custom configuration module
        from fastapi_app.app.config.api_config import get_openai_api_key, get_anthropic_api_key
        
        openai_key = get_openai_api_key()
        anthropic_key = get_anthropic_api_key()
        
        print(f"OpenAI API key from module: {'Yes' if openai_key else 'No'}")
        if openai_key:
            print(f"OpenAI API key format valid: {'Yes' if openai_key.startswith('sk-') else 'No'}")
        
        print(f"Anthropic API key from module: {'Yes' if anthropic_key else 'No'}")
        if anthropic_key:
            print(f"Anthropic API key format valid: {'Yes' if anthropic_key.startswith('sk-ant-') else 'No'}")
            
    except ImportError as e:
        print(f"Could not import API configuration module: {e}")
    except Exception as e:
        print(f"Error using API configuration module: {e}")

def test_article_generator():
    """Test the article generator with the new configuration"""
    print("\n=== Testing Article Generator ===")
    try:
        # Import the module directly
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "advanced_article_generator",
            "fastapi_app/app/generators/advanced_article_generator.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Access key variables from the module
        print(f"OpenAI API key in generator: {'Yes' if module.OPENAI_API_KEY else 'No'}")
        if hasattr(module, 'OPENAI_KEY_VALID'):
            print(f"OpenAI API key valid: {'Yes' if module.OPENAI_KEY_VALID else 'No'}")
        
        print(f"Anthropic API key in generator: {'Yes' if module.ANTHROPIC_API_KEY else 'No'}")
        if hasattr(module, 'ANTHROPIC_KEY_VALID'):
            print(f"Anthropic API key valid: {'Yes' if module.ANTHROPIC_KEY_VALID else 'No'}")
    
    except Exception as e:
        print(f"Error testing article generator: {e}")

def main():
    """Run all tests"""
    print("=== API Key Configuration Test ===")
    
    # Test all methods
    test_env_variables()
    test_config_file()
    test_api_config_module()
    test_article_generator()
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    main()
