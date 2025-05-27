"""
API Configuration module that securely manages API keys
This provides a robust way to access API keys from multiple sources with fallbacks
"""
import os
import logging
import json
from pathlib import Path

logger = logging.getLogger("api_config")

# Constants
CONFIG_FILE_PATH = os.environ.get(
    "API_CONFIG_FILE_PATH", 
    str(Path(__file__).parent.parent.parent.parent / "config" / "api_keys.json")
)

# Hardcoded keys - ONLY USE FOR DEVELOPMENT or as absolute last resort fallback
# In production, these should be empty strings and the keys should be in environment 
# variables or the config file
DEFAULT_KEYS = {
    "OPENAI_API_KEY": "",
    "ANTHROPIC_API_KEY": ""  # DO NOT put actual key here in production code
}

def _load_keys_from_file():
    """Load API keys from a config file"""
    try:
        if os.path.exists(CONFIG_FILE_PATH):
            with open(CONFIG_FILE_PATH, "r") as f:
                if CONFIG_FILE_PATH.endswith(".json"):
                    return json.load(f)
                else:
                    # Simple key=value format
                    data = {}
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            key, value = line.split("=", 1)
                            data[key.strip()] = value.strip().strip("'").strip('"')
                    return data
    except Exception as e:
        logger.error(f"Error loading API keys from file: {e}")
    return {}

def get_api_key(key_name):
    """
    Get an API key using the following priority:
    1. Environment variable
    2. Configuration file
    3. Default hardcoded value (empty in production)
    """
    # First, check environment variables (highest priority)
    env_value = os.environ.get(key_name)
    if env_value:
        logger.info(f"Using {key_name} from environment variables")
        return env_value
    
    # Next, try to load from config file
    file_keys = _load_keys_from_file()
    if key_name in file_keys and file_keys[key_name]:
        logger.info(f"Using {key_name} from configuration file")
        return file_keys[key_name]
    
    # Finally, fall back to default (should be empty in production)
    if key_name in DEFAULT_KEYS and DEFAULT_KEYS[key_name]:
        logger.warning(f"Using default hardcoded {key_name} - NOT RECOMMENDED FOR PRODUCTION")
        return DEFAULT_KEYS[key_name]
    
    # No key found
    logger.warning(f"{key_name} not found in any configuration source")
    return None

def get_openai_api_key():
    """Get the OpenAI API key"""
    # Try environment variable first, then fall back to hardcoded key
    api_key = os.environ.get('OPENAI_API_KEY')
    if api_key:
        return api_key
    
    # If environment variable not set, use this hardcoded key for development/testing
    # Using the original service account key which worked for tone analysis previously
    return "YOUR_OPENAI_API_KEY_HERE"

def get_anthropic_api_key():
    """Get the Anthropic API key"""
    return get_api_key("ANTHROPIC_API_KEY")

# Initialize and validate on module import
if not get_openai_api_key():
    logger.warning("No OpenAI API key found in any configuration source")

if not get_anthropic_api_key():
    logger.warning("No Anthropic API key found in any configuration source")
