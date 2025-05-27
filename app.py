#!/usr/bin/env python3
"""
SocialMe - Main Application

This is the main entry point for the SocialMe application.
It configures the Flask application and registers all routes.
"""

import os
import logging
import secrets
from flask import Flask, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO if os.getenv('DEBUG') != 'true' else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("flask_app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Import from the complete workflow test
from complete_workflow_test import app as workflow_app, workflow as workflow_data

# Store the app reference for use in main
app = workflow_app

# Ensure the SECRET_KEY is set
if 'SECRET_KEY' not in app.config or not app.config['SECRET_KEY']:
    logger.warning("SECRET_KEY not found in config, generating a random one")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or secrets.token_hex(32)

# Root route is already defined in complete_workflow_test.py
# Additional routes can be added here if needed

# Run the application if executed directly
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8004))  # Use PORT env var if set, otherwise default to 8004
    logger.info(f"Starting SocialMe application on port {port}")
    app.run(host='0.0.0.0', port=port, debug=os.getenv('DEBUG') == 'true')
