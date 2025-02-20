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
from CrewAI.agents.gistaApp_agents.content_approval_team.content_approval_tools import get_all_content_approval_tools

def create_content_validator_agent(tools: Optional[List[BaseTool]] = None):
    """
    Create content validator agent with specified tools.
    
    Args:
        tools: List of tools for the agent to use
        
    Returns:
        Agent: Configured content validator agent
    """
    if tools is None:
        tools = []
        
    return Agent(
        role="Content Validator",
        goal="Validate and process content for approval",
        backstory=(
            "Expert content validator with experience in multiple content types. "
            "Skilled at identifying content issues and providing clear feedback."
        ),
        tools=tools,
        allow_delegation=True,  # Allow task chaining
        verbose=True,
        llm_config={
            "temperature": 0.7,
            "request_timeout": 600
        }
    )

def create_content_approval_agents(tools: Optional[List[Any]] = None) -> dict:
    """
    Create and return specialized content approval agents
    
    Args:
        tools: Optional list of tools to pass to agents
        
    Returns:
        dict: Dictionary of configured agents
    """
    content_validator = create_content_validator_agent(tools=tools)

    agents_dict = {
        "content_validator": content_validator
    }

    return agents_dict
