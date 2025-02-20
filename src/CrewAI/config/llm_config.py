import os
from langchain_community.llms import HuggingFaceHub
from langchain_community.chat_models import ChatCohere
from dotenv import load_dotenv

load_dotenv()

def get_huggingface_llm():
    """
    Initialize and return HuggingFace LLM
    """
    return HuggingFaceHub(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        huggingfacehub_api_token=os.getenv('HUGGINGFACE_API_TOKEN'),
        task="text-generation",
    )

def get_mistral_config():
    """
    Return Mistral configuration
    """
    return {
        "api_key": os.getenv('MISTRAL_API_KEY'),
        "api_base": "https://api.mistral.ai/v1",
        "model_name": "mistral-small"
    }

def get_cohere_llm():
    """
    Initialize and return Cohere LLM
    """
    return ChatCohere(
        cohere_api_key=os.getenv('COHERE_API_KEY')
    )

def get_llm(provider: str = "openai"):
    """
    Factory function to get the specified LLM
    """
    providers = {
        "huggingface": get_huggingface_llm,
        "cohere": get_cohere_llm,
        "mistral": get_mistral_config
    }
    
    return providers.get(provider.lower(), lambda: None)() 