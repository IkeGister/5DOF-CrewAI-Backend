import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SERPER_API_KEY = os.getenv('SERPER_API_KEY')

# Model Settings
DEFAULT_MODEL = "gpt-4-turbo"
TEMPERATURE = 0.7
MAX_TOKENS = 1500

# Application Settings
DEBUG_MODE = True
VERBOSE_OUTPUT = bool(2)  # or simply True if you want verbose output

# Validate required settings
def validate_settings():
    """Validate that all required settings are present"""
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in environment variables")
    if not SERPER_API_KEY:
        raise ValueError("SERPER_API_KEY is not set in environment variables")

# Initialize settings validation
validate_settings() 