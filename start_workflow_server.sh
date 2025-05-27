#!/bin/bash
# Standard workflow server startup script
# Created: May 7, 2025
# Purpose: Ensures consistent server startup with the correct configuration

# Show execution steps
set -e

echo "====================================================="
echo "Starting SocialMe Workflow API Server"
echo "====================================================="

# Move to project root
cd /root/socialme/social-me-test-2
echo "✅ Changed to project root: $(pwd)"

# Activate virtual environment
source fastapi_app/venv/bin/activate
echo "✅ Activated virtual environment: $(which python)"

# Check Python version and packages
python -V
echo "✅ Python environment ready"

# Check if OPENAI_API_KEY is set in environment
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Error: OPENAI_API_KEY environment variable is not set. Please set it before running."
    exit 1
fi

# Kill any existing server on port 8001
echo "🔄 Checking for existing servers on port 8001..."
if fuser -k 8001/tcp 2>/dev/null; then
    echo "✅ Stopped existing server on port 8001"
else
    echo "✅ No existing server found on port 8001"
fi

# Wait briefly to ensure port is released
sleep 1

# Ensure static directory exists and has correct files
echo "🔄 Verifying static files..."
mkdir -p fastapi_app/static

# Check if files need to be copied or are already properly linked
if [ "$(readlink -f static)" != "$(readlink -f fastapi_app/static)" ]; then
    echo "Creating copies of HTML files (ignoring errors for already linked files)"
    cp -f static/*.html fastapi_app/static/ 2>/dev/null || true
fi
echo "✅ Static files verified: $(ls -1 fastapi_app/static/*.html | wc -l) HTML files available"

# Start the correct server implementation in module mode for better import handling
echo "🔄 Starting workflow API server..."
nohup python -m uvicorn fastapi_app.workflow_api:app --host 0.0.0.0 --port 8001 > /tmp/workflow_server.log 2>&1 &
SERVER_PID=$!
echo "✅ Server started with PID: $SERVER_PID"

# Wait briefly to verify server is running
sleep 2
if ps -p $SERVER_PID > /dev/null; then
    echo "✅ Server is running correctly"
else
    echo "❌ Server failed to start properly"
    echo "Check logs at /tmp/workflow_server.log"
    exit 1
fi

echo ""
echo "====================================================="
echo "Server is running at http://localhost:8001"
echo "Direct Workflow UI: http://localhost:8001/workflow-ui (RECOMMENDED)"
echo "Redirect URL: http://localhost:8001/static/workflow.html"
echo "Logs available at: /tmp/workflow_server.log"
echo "====================================================="
