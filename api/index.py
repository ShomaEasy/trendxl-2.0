"""
Vercel Serverless Function Entry Point
FastAPI ASGI application for Vercel
"""
import sys
import os

# Get the api directory path
# In Vercel, __file__ is /var/task/api/index.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add api directory to Python path FIRST
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Also add parent directory (project root)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the FastAPI app using standard Python import
# Since current_dir is in sys.path, 'main' will resolve to api/main.py
from main import app
