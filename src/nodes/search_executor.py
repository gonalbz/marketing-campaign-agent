"""
Search Executor Node.

This module is responsible for using Tavily to search and fetch top 3 results
for each provided question.
"""

from config.settings import TAVILY_API_KEY, MAX_SEARCH_RESULTS_PER_QUESTION

class SearchExecutor:
    def __init__(self, tavily_api_key: str = None):
        # Use provided API key or fall back to the one in settings
        self.api_key = tavily_api_key or TAVILY_API_KEY
        self.max_results = MAX_SEARCH_RESULTS_PER_QUESTION
        
    def search(self, questions: list[str]) -> dict:
        """
        Execute searches for each question using Tavily API.
        
        Args:
            questions (list[str]): List of questions to search for
            
        Returns:
            dict: Dictionary mapping questions to their top 3 search results
        """
        if not self.api_key:
            raise ValueError("Tavily API key not found. Please set it in .env file or pass it to the constructor.")
            
        # TODO: Implement Tavily search logic
        pass 