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

from crewai import Crew, Task
from typing import Dict, List, Optional, Any, Callable, Tuple
from pathlib import Path
from dotenv import load_dotenv
import os
import requests
import yaml

# Update imports to be relative
from .content_approval_tasks import validate_content_tasks
from .content_approval_agents import create_content_validator_agent as validator_creator

# Original imports - kept for reference
# from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
# from .content_approval_tools import create_directory_verification_tools

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
        
        # Load guidelines
        self.guidelines = self._load_approval_guidelines()
        
        # Remove this line since we don't have content_source yet
        # self._setup_team()
    
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

    def _load_approval_guidelines(self):
        """
        Load content approval guidelines from YAML
        
        Returns:
            dict: The loaded guidelines
            
        Raises:
            FileNotFoundError: If guidelines file is not found
            ValueError: If guidelines are malformed or missing
        """
        yaml_path = Path(__file__).parent / "content_approval_directories.yaml"
        print(f"\nLoading guidelines from: {yaml_path}")
        print(f"Absolute path: {yaml_path.absolute()}")
        print(f"File exists: {yaml_path.exists()}\n")
        
        if not yaml_path.exists():
            raise FileNotFoundError(
                f"YAML file not found at {yaml_path}. "
                f"Current directory: {Path.cwd()}"
            )
        
        try:
            with open(yaml_path, 'r') as file:
                yaml_content = yaml.safe_load(file)
                if yaml_content is None or not isinstance(yaml_content, dict):
                    raise ValueError("YAML file is empty or malformed")
                guidelines = yaml_content.get('content_approval_guidelines')
                if guidelines is None:
                    raise ValueError("Missing content_approval_guidelines in YAML")
                
                # Debug output for structure
                print("Guidelines structure:")
                print("===================")
                print("Top level keys:", list(guidelines.keys()))
                print("\nPodcast requirements keys:", 
                      list(guidelines.get('podcast_content_requirements', {}).keys()))
                print("\nValidation checks structure:", 
                      guidelines.get('podcast_content_requirements', {}).get('validation_checks', {}))
                print("===================\n")
                
                return guidelines
                
        except KeyError as e:
            print(f"KeyError: Missing key {e} in YAML structure")
            raise
        except yaml.YAMLError as e:
            print(f"YAML parsing error: {e}")
            raise
        except Exception as e:
            print(f"Unexpected error loading guidelines: {e}")
            raise

    def _setup_team(self, content_source: str):
        """
        Setup agents and tasks for the team
        
        Args:
            content_source: URL or file path to validate
        """
        # Create agent with content source
        self.agents = {
            "content_validator": validator_creator(url=content_source)
        }
        
        # Initialize empty tasks list
        self.tasks = []
        
        # Create crew
        if self.crew is None:
            self.crew = Crew(
                agents=[self.agents["content_validator"]],
                tasks=self.tasks,
                verbose=self.verbose
            )

    def start_podcast_production_flow(self, content_source: str) -> Tuple[Crew, List[Task], dict]:
        """
        Start the podcast production flow
        
        Args:
            content_source: URL or file path to source content
            
        Returns:
            Tuple[Crew, List[Task], dict]: (crew, tasks, guidelines)
        """
        # Setup team with content source
        self._setup_team(content_source)
        
        # Create tasks
        tasks = validate_content_tasks(
            content_validator=self.agents["content_validator"],
            guidelines=self.guidelines,
            content_source=content_source
        )
        
        # Update crew's tasks
        if self.crew is not None:
            self.crew.tasks = tasks
        else:
            raise ValueError("Crew initialization failed")
        
        return self.crew, tasks, self.guidelines

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
