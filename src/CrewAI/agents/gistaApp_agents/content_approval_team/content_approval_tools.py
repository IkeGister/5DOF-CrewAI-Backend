from typing import List, Optional
from crewai_tools import (
    ScrapeWebsiteTool, 
    DOCXSearchTool, 
    PDFSearchTool, 
    DirectoryReadTool
)

def create_website_verification_tools(url: Optional[str] = None) -> List:
    """
    Create tools for verifying website content.
    
    Parameters:
    - url: Optional specific URL to analyze
    
    Returns:
    - List of tools for website content verification
    """
    website_tool = ScrapeWebsiteTool(
        website_url=url if url else "https://example.com"
    )
    return [website_tool]

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

