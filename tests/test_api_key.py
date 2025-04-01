#!/usr/bin/env python3
"""
Test script to verify the Claude API key
"""

import os
import sys
from dotenv import load_dotenv
from anthropic import Anthropic

def test_claude_api_key():
    """Test if the Claude API key is valid"""
    print("Testing Claude API key...")
    
    # Read API key directly from .env file
    try:
        with open('/root/socialme/social-me-test-2/.env', 'r') as f:
            env_lines = f.readlines()
            
        api_key = None
        for line in env_lines:
            if line.startswith('CLAUDE_API_KEY='):
                api_key = line.strip().split('=', 1)[1]
                break
                
        if not api_key:
            print("ERROR: No Claude API key found in .env file")
            return False
            
        # Print the API key for debugging
        print(f"Using API key: {api_key}")
        print(f"API key length: {len(api_key)}")
        print(f"API key found: {api_key[:10]}...{api_key[-4:]}")
    except Exception as e:
        print(f"ERROR reading .env file: {e}")
        return False
    
    # Test the API key
    try:
        client = Anthropic(api_key=api_key)
        
        # Simple test message
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=100,
            messages=[
                {"role": "user", "content": "Hello, this is a test message. Please respond with 'API key is valid' if you receive this."}
            ]
        )
        
        # Check response
        if response and response.content:
            print("SUCCESS: API key is valid")
            print(f"Response from Claude: {response.content[0].text}")
            return True
        else:
            print("ERROR: Received empty response from Claude API")
            return False
            
    except Exception as e:
        print(f"ERROR: Failed to authenticate with Claude API: {e}")
        return False

if __name__ == "__main__":
    success = test_claude_api_key()
    sys.exit(0 if success else 1)
