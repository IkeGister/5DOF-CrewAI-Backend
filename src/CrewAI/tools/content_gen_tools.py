"""
Content Tools Module
===================

This module manages the creation and organization of tools for CrewAI agents.

Tool Assignment Hierarchy:
-------------------------

Tools in CrewAI can be assigned at two levels:

1. Agent Level:
   - Tools assigned directly to an agent are available for all tasks
   - The agent has discretionary use of these tools
   
2. Task Level:
   - Tools assigned to specific tasks override agent-level tools
   - When a task has assigned tools, the agent will ONLY use those tools
   - This provides precise control over tool usage for specific tasks

Visual Representation:
---------------------

                     Assigning Tools
                     
                    ┌──────────────┐
                    │    Tools     │
                    └──────┬───────┘
                           │
                 ┌────────┴────────┐
                 │                  │
        ┌────────┴───────┐    ┌────┴────┐
        │     Agent      │    │  Task   │
        │   (Default)    │    │(Override)│
        └────────────────┘    └─────────┘

Notes:
- Tools assigned to Agent: Available for all tasks (discretionary use)
- Tools assigned to Task: Exclusively used for that specific task
"""
import os  # Import os to access environment variables
from typing import Optional

# Importing necessary tools from crewai_tools
from crewai_tools import (
    SerperDevTool, 
    ScrapeWebsiteTool, 
    WebsiteSearchTool, 
    CSVSearchTool, 
    DOCXSearchTool, 
    YoutubeChannelSearchTool, 
    GithubSearchTool, 
    PDFSearchTool, 
    DirectoryReadTool
)

# Importing tools specific to CrewAI
from CrewAI.tools.travel_guide_tool import TravelGuideTool

# List of tool classes to instantiate
TOOL_CLASSES = [
    SerperDevTool,
    ScrapeWebsiteTool,
    WebsiteSearchTool,
    CSVSearchTool,
    DOCXSearchTool,
    YoutubeChannelSearchTool,
    GithubSearchTool,
    PDFSearchTool,
    DirectoryReadTool,
    TravelGuideTool
]

def create_research_tools():
    """
    Create and return tools for content research.
    """
    # Retrieve the Serper API key from environment variables
    serper_api_key = os.getenv("SERPER_API_KEY")  # Ensure this environment variable is set

    # Instantiate all tools from the TOOL_CLASSES list
    research_tools = [
        tool_class(api_key=serper_api_key) if tool_class == SerperDevTool else tool_class() 
        for tool_class in TOOL_CLASSES
    ]
    
    return research_tools

def create_test_research_tools():
    """
    Create and return a tool that will scrape a page (only 1 URL) of the CrewAI documentation.
    """
    docs_scrape_tool = ScrapeWebsiteTool(
        website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
    )
    
    return [docs_scrape_tool]

def create_directory_tools(directory: str):
    """
    Create and return tools for directory reading.
    """
    return [DirectoryReadTool(directory=directory)]

def file_reader_tools(file_path: str):
    """
    Create and return tools for reading files.
    """
    return [
        CSVSearchTool(file_path=file_path),
        DOCXSearchTool(file_path=file_path),
        PDFSearchTool(file_path=file_path)
    ]

def search_serper_search_tools(search_query: str, url: Optional[str] = None):
    """
    Create and return tools for searching with the SerperDevTool.
    
    Parameters:
    - search_query: The query string to search for.
    - url: An optional URL to search within.
    """
    search_tool = SerperDevTool()
    
    # Run the search tool with the provided query and URL
    results = search_tool._run(search_query=search_query, url=url)
    
    return results

def get_all_content_tools():
    """
    Get all tools needed for content creation.
    """
    # Instantiate all tools from the TOOL_CLASSES list
    return [tool_class() for tool_class in TOOL_CLASSES]