import os  # Import os to access environment variables
from typing import List, Optional
from langchain.tools import BaseTool  # Add this import

# Importing necessary tools from crewai_tools
from crewai_tools import (
    WebsiteSearchTool, 
    DOCXSearchTool, 
    PDFSearchTool, 
    DirectoryReadTool,
    ScrapeWebsiteTool
)

def create_gista_websearch_tool(website: Optional[str] = None) -> WebsiteSearchTool:
    """
    Creates a configured WebsiteSearchTool for Gista content verification.
    
    Parameters:
    - website: Optional specific website URL to analyze
    
    Returns:
    - Configured WebsiteSearchTool instance
    """
    search_tool = WebsiteSearchTool(website=website) if website else WebsiteSearchTool()
    return search_tool

def create_website_verification_tools(url: Optional[str] = None) -> List:
    """
    Create tools for verifying website content.
    
    Parameters:
    - url: Optional specific URL to analyze
    
    Returns:
    - List of tools for website content verification
    """
    tools = []
    
    # Use the abstracted website search tool
    tools.append(create_gista_websearch_tool())
    
    # Add specific URL scraping tool if URL is provided
    if url:
        tools.append(ScrapeWebsiteTool(website_url=url))
    
    return tools

def create_document_verification_tools(file_path: Optional[str] = None) -> List:
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

def create_directory_verification_tools(directory: str) -> DirectoryReadTool:
    """
    Create tools for verifying content in a directory.
    
    Args:
        directory (str): Path to directory to verify
        
    Returns:
        DirectoryReadTool: Tool for directory content verification
    """
    return DirectoryReadTool(directory=directory)

def create_gista_scrape_tool(website_url: Optional[str] = None) -> ScrapeWebsiteTool:
    """
    Creates a configured ScrapeWebsiteTool for Gista content extraction.
    
    Parameters:
    - website_url: Specific website URL to scrape
    
    Returns:
    - Configured ScrapeWebsiteTool instance
    """
    scrape_tool = ScrapeWebsiteTool(website_url=website_url) if website_url else ScrapeWebsiteTool()
    return scrape_tool

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

