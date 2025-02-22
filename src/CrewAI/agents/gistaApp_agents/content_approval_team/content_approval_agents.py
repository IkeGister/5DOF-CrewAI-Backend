"""
Content Approval Agents
======================

Specialized agents focused on content validation and approval processes.
These agents work in conjunction with the main Gista system while providing
detailed content validation capabilities.
"""

from crewai import Agent
from typing import List, Optional, Any
from langchain.tools import BaseTool
from .content_approval_tools import create_website_verification_tools

def create_content_validator_agent(url: Optional[str] = None) -> Agent:
    """
    Create content validator agent with website verification tools.
    
    Args:
        url: URL to validate
        
    Returns:
        Agent: Configured content validator agent
    """
    # Get website verification tools for the specific URL
    tools = create_website_verification_tools(url=url)
        
    return Agent(
        role="Content Validator",
        goal="Validate and process content for approval",
        backstory=(
            "Expert content validator with experience in multiple content types. "
            "Skilled at identifying content issues and providing clear feedback. "
            "Uses specialized tools to verify website content and accessibility."
        ),
        tools=tools,
        allow_delegation=True,
        verbose=True,
        llm_config={
            "temperature": 0.7,
            "request_timeout": 600
        }
    )

def create_content_approval_agents(url: Optional[str] = None) -> dict:
    """
    Create and return specialized content approval agents
    
    Args:
        url: URL to validate
        
    Returns:
        dict: Dictionary of configured agents
    """
    content_validator = create_content_validator_agent(url=url)

    agents_dict = {
        "content_validator": content_validator
    }

    return agents_dict
