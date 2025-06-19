"""
Configuration settings for the application.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Application Settings
MAX_QUESTIONS = 5
MAX_SEARCH_RESULTS_PER_QUESTION = 3
MAX_TRENDS = 3 