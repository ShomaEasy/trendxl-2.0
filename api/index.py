"""
Vercel Serverless Function Entry Point
FastAPI ASGI application for Vercel
"""
import sys
import os
import importlib.util

# Get the api directory path
# In Vercel, __file__ is /var/task/api/index.py
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add api directory to Python path
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Also add parent directory (project root)
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Load main.py module explicitly using importlib
main_path = os.path.join(current_dir, 'main.py')
if not os.path.exists(main_path):
    raise FileNotFoundError(f"main.py not found at {main_path}")

spec = importlib.util.spec_from_file_location("main", main_path)
if spec is None or spec.loader is None:
    raise ImportError(f"Could not load spec from {main_path}")

main_module = importlib.util.module_from_spec(spec)
sys.modules["main"] = main_module
spec.loader.exec_module(main_module)

# Get the FastAPI app instance
app = main_module.app
