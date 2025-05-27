#!/usr/bin/env python3
"""
Script to initialize the database for the SocialMe application.
"""
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from app.database import init_db

if __name__ == "__main__":
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialization completed.")
