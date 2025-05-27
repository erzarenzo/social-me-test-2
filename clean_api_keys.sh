#!/bin/bash
# Script to clean API keys from the codebase
# This only affects the current branch without modifying your working files

echo "Cleaning API keys from config files..."

# Clean OpenAI API key from api_config.py
if [ -f "fastapi_app/app/config/api_config.py" ]; then
    sed -i 's/return "sk-svcacct-[^"]*"/return "YOUR_OPENAI_API_KEY_HERE"/' fastapi_app/app/config/api_config.py
    echo "✅ Cleaned OpenAI API key from api_config.py"
fi

# Clean potential API keys from the start_workflow_server.sh
if [ -f "start_workflow_server.sh" ]; then
    sed -i 's/export OPENAI_API_KEY="[^"]*"/export OPENAI_API_KEY="YOUR_OPENAI_API_KEY_HERE"/' start_workflow_server.sh
    echo "✅ Cleaned OpenAI API key from start_workflow_server.sh"
fi

# Clean API keys from api_keys.json if it exists
if [ -f "config/api_keys.json" ]; then
    sed -i 's/"OPENAI_API_KEY": "[^"]*"/"OPENAI_API_KEY": "YOUR_OPENAI_API_KEY_HERE"/' config/api_keys.json
    sed -i 's/"ANTHROPIC_API_KEY": "[^"]*"/"ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE"/' config/api_keys.json
    echo "✅ Cleaned API keys from api_keys.json"
fi

echo "API key cleaning complete!"
