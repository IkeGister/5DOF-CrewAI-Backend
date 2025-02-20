"""
Content Approval Tasks Module
===========================

This module defines tasks for content approval workflow:
1. check_content - Initial content validation
2. approve_content - Process approved content
3. reject_content - Handle rejected content
"""

from crewai import Task
from pydantic import BaseModel, ConfigDict
from typing import Dict, List, Optional, ClassVar, Any
import yaml
from pathlib import Path
import re

from CrewAI.agents.gistaApp_agents.content_approval_team.content_approval_tools import (
    create_gista_websearch_tool,
    create_gista_scrape_tool,
    create_document_verification_tools,
    create_directory_verification_tools
)

def load_approval_guidelines():
    """Load content approval guidelines from YAML"""
    yaml_path = Path(__file__).parent / "content_approval_directories.yaml"
    print(f"\nLoading guidelines from: {yaml_path}")
    print(f"File exists: {yaml_path.exists()}\n")
    
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

class RejectionOutput(BaseModel):
    """Output model for content rejection"""
    model_config = ConfigDict(extra='allow')
    
    ERROR_CODES: ClassVar[Dict[str, str]] = {
        'INVALID_URL': 'URL is invalid or inaccessible',
        'MALICIOUS_CONTENT': 'Content contains malicious elements',
        'ACCESS_BLOCKED': 'Content access is blocked (paywall/login)',
        'CONTENT_TYPE': 'Unsupported content type',
        'INSUFFICIENT_LENGTH': 'Content length below minimum requirement',
        'EXCESSIVE_LENGTH': 'Content length exceeds maximum limit',
        'FORMAT_ERROR': 'Content format is invalid or corrupted',
        'BOT_DETECTION': 'Site blocks automated access',
        'SECURITY_RISK': 'Security concerns detected',
        'NO_TEXT_CONTENT': 'No extractable text content found'
    }
    
    status: str = "rejected"
    error_code: str
    error_message: str
    rejection_reason: str
    suggestions: Optional[List[str]] = None
    metadata: Dict = {}

class ApprovalOutput(BaseModel):
    """Output model for content approval tasks"""
    model_config = ConfigDict(extra='allow')
    
    status: str
    content_status: str
    metadata: Dict[str, Any]
    content_validation: Dict[str, Any]
    content_complexity: Dict[str, Any]
    extracted_content: Dict[str, Any]
    processing_info: Dict[str, Any]

class ContentTypeOutput(BaseModel):
    """Output model for content type detection"""
    model_config = ConfigDict(extra='allow')
    
    content_type: str  # "url", "pdf", "docx", "unknown"
    content_path: str
    validation_tools: List[str]
    error_message: Optional[str] = None

def detect_content_type(content_path: str) -> str:
    """Helper function to detect content type from path or URL"""
    # URL pattern
    url_pattern = r'^(http|https):\/\/'
    
    if re.match(url_pattern, content_path):
        return "url"
    
    # File extension check
    file_extension = Path(content_path).suffix.lower()
    if file_extension in ['.pdf']:
        return "pdf"
    elif file_extension in ['.docx', '.doc']:
        return "docx"
    
    return "unknown"

def create_content_approval_tasks(agents):
    """Create tasks for content approval workflow"""
    
    # Load guidelines
    guidelines = load_approval_guidelines()
    
    # Base context structure all tasks will need
    base_context = {
        "description": "Content validation guidelines and rules",
        "expected_output": "Validation results based on guidelines",
        "guidelines": guidelines,
        "validation_rules": guidelines["podcast_content_requirements"]["validation_checks"],
        "content_criteria": guidelines["criteria"],
        "error_codes": RejectionOutput.ERROR_CODES
    }
    
    def wrap_task_with_early_exit(task):
        """
        Creates a new task that implements early exit functionality
        """
        return Task(
            description=task.description,
            expected_output=task.expected_output,
            agent=task.agent,
            tools=task.tools,
            context=task.context,
            output_pydantic=task.output_pydantic,
            async_execution=task.async_execution,
            callback=task.callback
        )

    # Content type detection task
    detect_content = Task(
        description=(
            "Analyze the provided content path and determine its type:\n"
            "1. Check if the content is a URL (starts with http/https)\n"
            "2. Check if the content is a PDF file (.pdf extension)\n"
            "3. Check if the content is a Word document (.docx/.doc extension)\n"
            "4. Determine appropriate validation tools based on content type\n"
            "5. Return error if content type is unsupported"
        ),
        expected_output=(
            "A structured response containing:\n"
            "- content_type: The detected type (url/pdf/docx/unknown)\n"
            "- content_path: The original content path\n"
            "- validation_tools: List of appropriate tools for this content\n"
            "- error_message: Any error encountered (if applicable)"
        ),
        agent=agents["content_validator"],
        tools=[],  # No tools needed for type detection
        output_pydantic=ContentTypeOutput
    )

    def get_tools_for_content_type(content_type: str, content_path: Optional[str] = None) -> List:
        """Helper function to get appropriate tools based on content type"""
        if content_path is None:
            return []  # Return empty list if no path provided
            
        if content_type == "url":
            return [
                create_gista_websearch_tool(website=content_path),
                create_gista_scrape_tool(website_url=content_path)
            ]
        elif content_type in ["pdf", "docx"]:
            return create_document_verification_tools(file_path=content_path)
        else:
            return []  # Return empty list for unknown types

    # Check content task with dynamic tool selection
    check_content = Task(
        description=(
            "Extract and validate content based on its detected type:\n"
            "1. Use the content type from previous task\n"
            "2. Apply appropriate tools based on content type:\n"
                "- URLs: Use web_scraper and website_search\n"
                "- PDFs: Use pdf_reader\n"
                "- Word docs: Use docx_reader\n"
            "3. Structure the output data\n"
            "4. Set content_status based on validation rules\n"
            "5. Calculate timing estimates"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "- Status and content_status\n"
            "- Complete metadata\n"
            "- Content validation flags\n"
            "- Content complexity metrics\n"
            "- Extracted content sections\n"
            "- Processing information\n"
            "If rejected, include:\n"
            "- Error code from RejectionOutput.error_codes\n"
            "- Detailed error message\n"
            "- Rejection reason\n"
            "- Suggested alternatives if applicable"
        ),
        agent=agents["content_validator"],
        tools=lambda task_output: get_tools_for_content_type(
            content_type=task_output.content_type,
            content_path=task_output.content_path
        ) if task_output else [],
        output_pydantic=RejectionOutput,
        context=[base_context, detect_content]
    )
    
    approve_content = Task(
        description=(
            "Process CLEARED or NEEDS_REVIEW content for quick approval response:\n"
            "1. Verify content_status from check_content output\n"
            "2. Generate appropriate approval message\n"
            "3. Prepare user notification with initial timeline estimate\n"
            "4. Set workflow type (standard/special_review)"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "- Status (approved)\n"
            "- Workflow type\n"
            "- Content information\n"
            "- Approval details\n"
            "- UI messages"
        ),
        agent=agents["content_validator"],
        tools=[],
        context=[
            {
                "description": "Approval process guidelines",
                "expected_output": "Approval validation results",
                **base_context,
                "previous_check": check_content.output
            }
        ],
        output_pydantic=ApprovalOutput
    )
    
    reject_content = Task(
        description=(
            "Process REJECTED content and prepare rejection response:\n"
            "1. Extract rejection reason from check_content output\n"
            "2. Select appropriate error code from RejectionOutput.error_codes\n"
            "3. Generate detailed error message and rejection reason\n"
            "4. Provide helpful suggestions when possible\n"
            "5. Include relevant metadata about the rejection"
        ),
        expected_output=(
            "A structured rejection document containing:\n"
            "- status: 'rejected'\n"
            "- error_code: Standardized error code from provided list\n"
            "- error_message: Clear explanation of the error\n"
            "- rejection_reason: Detailed reason for rejection\n"
            "- suggestions: List of alternative actions or fixes\n"
            "- metadata: Additional context about the rejection"
        ),
        agent=agents["content_validator"],
        tools=[],
        context=[
            {
                "description": "Rejection process guidelines",
                "expected_output": "Rejection validation results",
                **base_context,
                "previous_check": check_content.output
            }
        ],
        output_pydantic=RejectionOutput
    )
    
    # Return tasks with detect_content as first task
    tasks = [
        detect_content,
        check_content,
        wrap_task_with_early_exit(approve_content),
        wrap_task_with_early_exit(reject_content)
    ]
    
    return tasks

def task_completed_callback(output):
    """Callback function for task completion"""
    print(f"Task completed with status: {output.status}")
