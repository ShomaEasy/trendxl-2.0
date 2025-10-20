"""
Vercel Serverless Function Entry Point
FastAPI ASGI application for Vercel
"""
import sys
import os

# Add the api directory to Python path for module resolution
# In Vercel, __file__ is /var/task/api/index.py
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Also add parent directory (project root)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the FastAPI app from api/main.py
# Vercel will automatically detect and handle the ASGI application
from main import app
