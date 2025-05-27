#!/bin/bash
# Script to set up API keys for the application
# This script should be run on the server during deployment

# Set directory paths
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR/config"
API_KEYS_FILE="$CONFIG_DIR/api_keys.json"

# Ensure config directory exists
mkdir -p "$CONFIG_DIR"

# Create the API keys file with proper permissions
if [ ! -f "$API_KEYS_FILE" ]; then
    echo "Creating API keys file..."
    cat > "$API_KEYS_FILE" << EOF
{
    "OPENAI_API_KEY": "$OPENAI_API_KEY",
    "ANTHROPIC_API_KEY": "$ANTHROPIC_API_KEY"
}
EOF
    # Restrict permissions to only the owner (the user running the application)
    chmod 600 "$API_KEYS_FILE"
    echo "API keys file created with restricted permissions."
else
    echo "API keys file already exists. Updating..."
    # Create a temporary file with the new content
    TMP_FILE=$(mktemp)
    cat > "$TMP_FILE" << EOF
{
    "OPENAI_API_KEY": "$OPENAI_API_KEY",
    "ANTHROPIC_API_KEY": "$ANTHROPIC_API_KEY"
}
EOF
    # Replace the existing file with the new one
    mv "$TMP_FILE" "$API_KEYS_FILE"
    chmod 600 "$API_KEYS_FILE"
    echo "API keys file updated with restricted permissions."
fi

# Also set environment variables for the current session
export OPENAI_API_KEY="$OPENAI_API_KEY"
export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"

echo "API keys have been configured. To use them in the current shell session, run:"
echo "source $SCRIPT_DIR/setup_api_keys.sh"
