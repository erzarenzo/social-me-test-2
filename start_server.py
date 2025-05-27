#!/usr/bin/env python3
"""
Wrapper script to start the FastAPI server with correct import paths
"""
import os
import sys
import subprocess
from pathlib import Path

# Get the absolute path to the project root
project_root = Path(__file__).parent.absolute()
fastapi_app_dir = project_root / "fastapi_app"

# Add the necessary directories to the Python path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(fastapi_app_dir))

# Change to the fastapi_app directory
os.chdir(str(fastapi_app_dir))

print(f"Starting server from directory: {os.getcwd()}")
print(f"Python path: {sys.path}")

# Start the uvicorn server
cmd = [
    "uvicorn", 
    "app.APP:app", 
    "--host", "0.0.0.0", 
    "--port", "8000",
]

print(f"Running command: {' '.join(cmd)}")
subprocess.run(cmd)
