"""
Content Approval Team Module
===========================

This module manages the content approval team/crew, which is responsible for:
1. Initial content validation
2. Access verification
3. Content approval/rejection decisions
"""

from crewai import Crew
from typing import Dict, List, Optional
from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
import os
from dotenv import load_dotenv
from pathlib import Path
import requests

from .content_approval_tasks import create_content_approval_tasks
from .content_approval_agents import create_content_validator_agent
from .content_approval_tools import create_directory_verification_tools

class ContentApprovalTeam:
    """
    Wrapper class for content approval crew and its operations.
    Handles initial content validation and approval process.
    """
    
    def __init__(self, verbose: bool = False):
        """
        Initialize the content approval team.
        
        Args:
            verbose (bool): Enable verbose output
        """
        # Load environment variables
        self._load_environment()
        
        self.verbose = verbose
        self.agents = {}
        self.tasks = []
        self.crew = None
        self.tools = self._initialize_tools()
        
        # Initialize team
        self._setup_team()
    
    def _load_environment(self):
        """Load environment variables from .env file"""
        # Try to find .env file in CrewAI root
        project_root = Path(__file__).parent.parent.parent.parent
        env_path = project_root / '.env'
        
        print(f"Looking for .env at: {env_path}")  # Debug print
        print(f"File exists: {env_path.exists()}")  # Debug print
        
        if env_path.exists():
            load_dotenv(env_path)
            print(f"Loaded environment from: {env_path}")  # Debug print
        else:
            raise EnvironmentError(
                f"No .env file found at {env_path}. Please create one with OPENAI_API_KEY="
                "your-api-key in the CrewAI directory"
            )
        
        # Verify OpenAI API key is set
        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError(
                "OPENAI_API_KEY not found in environment variables. "
                "Please set it in your .env file"
            )
    
    def _initialize_tools(self) -> Dict:
        """Initialize all tools needed by the team"""
        # Get directory containing content_approval_directories.yaml
        content_dir = Path(__file__).parent  # Current directory containing YAML file
        
        return {
            "website_search": WebsiteSearchTool(),
            "website_scraper": ScrapeWebsiteTool(),
            "directory_reader": create_directory_verification_tools(directory=str(content_dir))
        }
    
    def _setup_team(self):
        """Setup agents and tasks for the team"""
        # Create agents with all tools
        self.agents = {
            "content_validator": create_content_validator_agent(
                tools=[
                    self.tools["website_search"],
                    self.tools["website_scraper"],
                    self.tools["directory_reader"]
                ]
            )
        }
        
        # Create tasks (directory tool already assigned in tasks)
        self.tasks = create_content_approval_tasks(self.agents)
        
        # Create crew
        self.crew = Crew(
            agents=[self.agents["content_validator"]],
            tasks=self.tasks,
            verbose=self.verbose,
            process_type="sequential"
        )
    
    def process_content(self, content_source: str) -> Dict:
        """Process content for approval."""
        try:
            # Add debug logging
            print(f"\nProcessing content: {content_source}")
            
            result = self.crew.kickoff(
                inputs={"content_source": content_source}
            )
            
            # Add debug logging for result
            print(f"Crew result: {result}")
            
            content_status = result.get("content_status", "UNKNOWN")
            error_code = result.get("error_code")
            
            # If we have an error_code in the result, use it
            if error_code:
                return {
                    "status": "rejected",
                    "error_code": error_code,
                    "error_message": result.get("error_message", "Unknown error"),
                    "rejection_reason": result.get("rejection_reason", "Content validation failed"),
                    "suggestions": result.get("suggestions", []),
                    "metadata": result.get("metadata", {})
                }
            
            # If content is cleared, return completed
            if content_status == "CLEARED":
                return {
                    "status": "completed",
                    "content_status": content_status,
                    "details": result
                }
            
            # Default rejection with processing error
            return {
                "status": "rejected",
                "error_code": "PROCESSING_ERROR",
                "error_message": "Content validation failed",
                "rejection_reason": "Unable to process content",
                "suggestions": ["Try a different source"],
                "metadata": {}
            }
            
        except Exception as e:
            print(f"Exception caught: {type(e).__name__}: {str(e)}")  # Debug logging
            return {
                "status": "rejected",
                "error_code": "PROCESSING_ERROR",
                "error_message": str(e),
                "rejection_reason": "Content processing failed",
                "suggestions": ["Try again later"],
                "metadata": {}
            }
    
    def get_agents(self) -> Dict:
        """Get all agents in the team"""
        return self.agents
    
    def get_tasks(self) -> List:
        """Get all tasks assigned to the team"""
        return self.tasks
    
    def get_crew(self) -> Crew:
        """Get the crew instance"""
        return self.crew
    
    def get_tools(self) -> Dict:
        """Get all tools available to the team"""
        return self.tools
