import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from app.main import app

# This is the entry point for Vercel serverless functions
handler = app
