"""
Content Approval Team Module
===========================

This module manages the content approval team/crew, which is responsible for:
1. Initial content validation
2. Access verification
3. Content approval/rejection decisions

Task Execution Order
-------------------
The content approval process follows this specific order:

1. detect_content:
   - Determines content type (URL, PDF, DOCX)
   - Validates basic accessibility
   - Returns ContentTypeOutput with appropriate tools

2. check_content:
   - Uses tools specified by detect_content
   - Performs deep content validation
   - Extracts and analyzes content
   - Returns initial validation results

3. approve_content (conditional):
   - Executes if content passes validation
   - Processes approved content
   - Generates approval documentation

4. reject_content (conditional):
   - Executes if content fails validation
   - Generates detailed rejection reason
   - Provides improvement suggestions

Each task's output serves as context for subsequent tasks, ensuring
a progressive validation process.
"""

from crewai import Crew
from typing import Dict, List, Optional, Any, Callable
from pathlib import Path
from dotenv import load_dotenv
import os
import requests

# Original imports - kept for reference
# from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
# from .content_approval_tools import create_directory_verification_tools

# Defer these imports until they're needed to avoid circular imports
def _get_task_creators():
    from CrewAI.agents.gistaApp_agents.content_approval_team.content_approval_tasks import create_content_approval_tasks
    return create_content_approval_tasks

def _get_agent_creators():
    from CrewAI.agents.gistaApp_agents.content_approval_team.content_approval_agents import create_content_validator_agent
    return create_content_validator_agent

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
        self.task_callback: Optional[Callable[[Any], None]] = None
        
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

    # Original tool initialization method - kept for reference
    # def _initialize_tools(self) -> Dict:
    #     """Initialize all tools needed by the team"""
    #     yaml_path = Path(__file__).parent / "content_approval_directories.yaml"
    #     print(f"YAML file path: {yaml_path}")
    #     print(f"YAML file exists: {yaml_path.exists()}")
    #     
    #     content_dir = yaml_path.parent
    #     
    #     return {
    #         "website_search": WebsiteSearchTool(),
    #         "website_scraper": ScrapeWebsiteTool(),
    #         "directory_reader": create_directory_verification_tools(
    #             directory=str(content_dir),
    #             config_path=str(yaml_path)
    #         )
    #     }

    def _setup_team(self):
        """Setup agents and tasks for the team"""
        # Get creators only when needed
        create_content_validator_agent = _get_agent_creators()
        create_content_approval_tasks = _get_task_creators()
        
        # Create agent without tools
        self.agents = {
            "content_validator": create_content_validator_agent(tools=[])
        }
        
        # Original agent creation with tools - kept for reference
        # self.agents = {
        #     "content_validator": create_content_validator_agent(
        #         tools=[
        #             self.tools["website_search"],
        #             self.tools["website_scraper"],
        #             self.tools["directory_reader"]
        #         ]
        #     )
        # }
        
        # Create tasks
        self.tasks = create_content_approval_tasks(self.agents)
        
        # Create crew
        self.crew = Crew(
            agents=[self.agents["content_validator"]],
            tasks=self.tasks,
            verbose=self.verbose
        )

    def _map_crew_output(self, result: Any) -> Dict:
        """Converts the crew output to a dictionary if needed."""
        if hasattr(result, "dict"):
            return result.dict()
        elif isinstance(result, dict):
            return result
        else:
            raise ValueError("Crew output is not a dictionary")
    
    def process_content(self, content_source: str) -> Dict:
        """Process content for approval."""
        try:
            if self.crew is None:
                raise ValueError("Crew has not been initialized")
            print(f"\nProcessing content: {content_source}")
            
            raw_result = self.crew.kickoff(inputs={"content_source": content_source})
            if self.task_callback:
                self.task_callback(raw_result)
            result = self._map_crew_output(raw_result)
            print(f"Crew result: {result}")

            content_status = result.get("content_status", "UNKNOWN")
            error_code = result.get("error_code")

            if error_code:
                return {
                    "status": "rejected",
                    "error_code": error_code,
                    "error_message": result.get("error_message", "Unknown error"),
                    "rejection_reason": result.get("rejection_reason", "Content validation failed"),
                    "suggestions": result.get("suggestions", []),
                    "metadata": result.get("metadata", {})
                }

            if content_status in ["CLEARED", "approved"]:
                return {
                    "status": "completed",
                    "content_status": content_status,
                    "details": result
                }

            return {
                "status": "rejected",
                "error_code": "PROCESSING_ERROR",
                "error_message": "Content validation failed",
                "rejection_reason": "Unable to process content",
                "suggestions": ["Try a different source"],
                "metadata": {}
            }

        except Exception as e:
            print(f"Exception caught: {type(e).__name__}: {str(e)}")
            return {
                "status": "rejected",
                "error_code": "PROCESSING_ERROR",
                "error_message": str(e),
                "rejection_reason": "Content processing failed",
                "suggestions": ["Try again later"],
                "metadata": {}
            }
    
    # Utility methods
    def get_agents(self) -> Dict:
        """Get all agents in the team"""
        return self.agents
    
    def get_tasks(self) -> List:
        """Get all tasks assigned to the team"""
        return self.tasks
    
    def get_crew(self) -> Crew:
        """Get the crew instance"""
        if self.crew is None:
            raise ValueError("Crew has not been initialized")
        return self.crew
    
    def kickoff(self, **kwargs):
        """Start the content approval process"""
        if self.crew is None:
            raise ValueError("Crew has not been initialized")
        return self.crew.kickoff(**kwargs)

    def get_tools(self) -> Dict:
        """Get all tools used by the team"""
        tools = {}
        if (self.agents and "content_validator" in self.agents 
            and hasattr(self.agents["content_validator"], "tools") 
            and self.agents["content_validator"].tools is not None):
            for tool in self.agents["content_validator"].tools:
                tools[tool.name] = tool
        return tools
