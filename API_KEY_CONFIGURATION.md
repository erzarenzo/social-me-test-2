# API Key Configuration Guide

This document outlines how to configure API keys for the article generation system.

## Overview of the Configuration System

Our API key management system uses a hierarchical approach with multiple fallback mechanisms to ensure API keys are always available to the backend:

1. **Environment variables** (highest priority)
2. **Configuration file** (second priority)
3. **Hardcoded defaults** (lowest priority, empty by default)

## Setting Up the API Keys

### Method 1: Environment Variables (Recommended for Production)

Set the following environment variables on your server:

```bash
export OPENAI_API_KEY=your-openai-key-here
export ANTHROPIC_API_KEY=your-anthropic-key-here
```

For persistent configuration, add these to your server's environment configuration or service definition.

### Method 2: Configuration File

You can store API keys in a JSON configuration file at `/config/api_keys.json`:

```json
{
    "OPENAI_API_KEY": "your-openai-key-here",
    "ANTHROPIC_API_KEY": "your-anthropic-key-here"
}
```

**Important security note:** Restrict access to this file using appropriate permissions:

```bash
chmod 600 /path/to/config/api_keys.json
```

### Method 3: Automated Setup

Use the provided setup script to configure your API keys:

```bash
# Set environment variables first
export OPENAI_API_KEY=your-openai-key-here
export ANTHROPIC_API_KEY=your-anthropic-key-here

# Then run the setup script
./setup_api_keys.sh
```

This will create/update the configuration file with the current environment variables.

## Troubleshooting

If you're experiencing issues with API key access:

1. **Check environment variables** are correctly set:
   ```bash
   echo $OPENAI_API_KEY
   echo $ANTHROPIC_API_KEY
   ```

2. **Verify configuration file** exists and has correct permissions:
   ```bash
   ls -la /path/to/config/api_keys.json
   ```

3. **Check application logs** for API key-related errors:
   ```bash
   grep -i "api key" /path/to/logs/fastapi_errors.log
   ```

4. **Test key validity** using a simple script:
   ```bash
   python3 -c "from fastapi_app.app.config.api_config import get_openai_api_key; print(f'OpenAI API key found: {get_openai_api_key() is not None}')"
   ```

## Deployment Considerations

When deploying to production:

1. **Never commit API keys** to version control
2. **Use environment variables** in orchestration systems like Docker, Kubernetes, etc.
3. **Implement key rotation** policies for enhanced security
4. **Monitor API key usage** to detect unauthorized access

## Fixing 500 Error on API Documentation

If you're seeing a 500 error when accessing `/docs` on your API:

1. Ensure all required environment variables are set
2. Check that the API key configuration is valid
3. Verify the service has proper permissions to read the configuration file
4. Check logs for specific error messages
5. Restart the service after configuring API keys
