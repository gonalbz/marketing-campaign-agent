"""
Query Generator Node.

This module is responsible for taking a user prompt and generating 3-5 key questions
for further research.
"""

from config.settings import MAX_QUESTIONS

class QueryGenerator:
    def __init__(self):
        self.max_questions = MAX_QUESTIONS
        
    def generate_questions(self, prompt: str) -> list[str]:
        """
        Generate 3-5 key questions based on the user prompt.
        
        Args:
            prompt (str): The user's input prompt
            
        Returns:
            list[str]: List of generated questions, limited by MAX_QUESTIONS setting
        """
        # TODO: Implement question generation logic
        # The number of questions will be limited by self.max_questions
        pass 