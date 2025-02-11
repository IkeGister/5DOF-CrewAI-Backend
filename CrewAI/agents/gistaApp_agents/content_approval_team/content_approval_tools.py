import os  # Import os to access environment variables
from typing import List
from langchain.tools import BaseTool  # Add this import

# Importing necessary tools from crewai_tools
from crewai_tools import (
    WebsiteSearchTool, 
    DOCXSearchTool, 
    PDFSearchTool, 
    DirectoryReadTool,
    ScrapeWebsiteTool
)

def create_website_verification_tools(url: str = None) -> List:
    """
    Create tools for verifying website content.
    
    Parameters:
    - url: Optional specific URL to analyze
    
    Returns:
    - List of tools for website content verification
    """
    tools = []
    
    # General website search tool
    tools.append(WebsiteSearchTool())
    
    # Add specific URL scraping tool if URL is provided
    if url:
        tools.append(ScrapeWebsiteTool(website_url=url))
    
    return tools

def create_document_verification_tools(file_path: str = None) -> List:
    """
    Create tools for verifying document content (DOCX, PDF).
    
    Parameters:
    - file_path: Optional specific file path to analyze
    
    Returns:
    - List of tools for document content verification
    """
    tools = []
    
    if file_path:
        # Add specific file tools based on file extension
        if file_path.lower().endswith('.pdf'):
            tools.append(PDFSearchTool(file_path=file_path))
        elif file_path.lower().endswith('.docx'):
            tools.append(DOCXSearchTool(file_path=file_path))
    else:
        # Add general document tools if no specific file
        tools.extend([
            PDFSearchTool(),
            DOCXSearchTool()
        ])
    
    return tools

def create_directory_verification_tools(directory: str) -> BaseTool:
    """
    Create tools for verifying content in a directory.
    
    Args:
        directory (str): Path to directory to verify
        
    Returns:
        BaseTool: Tool for directory content verification
    """
    return DirectoryReadTool(directory=directory)

def get_all_content_approval_tools() -> List:
    """
    Get all available content approval tools.
    
    Returns:
    - List of all content verification tools
    """
    return [
        WebsiteSearchTool(),
        ScrapeWebsiteTool(),
        PDFSearchTool(),
        DOCXSearchTool(),
        DirectoryReadTool()
    ]

