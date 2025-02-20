import os
from dotenv import load_dotenv

def get_openai_api_key():
    """
    Get OpenAI API key from environment variables
    """
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return api_key 