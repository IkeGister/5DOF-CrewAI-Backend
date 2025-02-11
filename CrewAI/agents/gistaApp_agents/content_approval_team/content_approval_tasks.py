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
from typing import Dict, List, Optional
import yaml
from pathlib import Path

from .content_approval_tools import create_directory_verification_tools

def load_approval_guidelines():
    """Load content approval guidelines from YAML"""
    yaml_path = Path(__file__).parent / "content_approval_directories.yaml"
    print(f"\nLoading guidelines from: {yaml_path}")
    print(f"File exists: {yaml_path.exists()}\n")
    
    try:
        with open(yaml_path, 'r') as file:
            guidelines = yaml.safe_load(file)['content_approval_guidelines']
            
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
    model_config = ConfigDict(
        extra='allow',
        error_codes = {
            "INVALID_URL": "URL is invalid or inaccessible",
            "MALICIOUS_CONTENT": "Content contains malicious elements",
            "ACCESS_BLOCKED": "Content access is blocked (paywall/login)",
            "CONTENT_TYPE": "Unsupported content type",
            "INSUFFICIENT_LENGTH": "Content length below minimum requirement",
            "EXCESSIVE_LENGTH": "Content length exceeds maximum limit",
            "FORMAT_ERROR": "Content format is invalid or corrupted",
            "BOT_DETECTION": "Site blocks automated access",
            "SECURITY_RISK": "Security concerns detected",
            "NO_TEXT_CONTENT": "No extractable text content found"
        }
    )
    
    status: str = "rejected"
    error_code: str
    error_message: str
    rejection_reason: str
    suggestions: Optional[List[str]] = None
    metadata: Dict = {}

class ApprovalOutput(BaseModel):
    """Output model for content approval tasks"""
    model_config = ConfigDict(
        extra='allow'
    )
    
    status: str
    content_status: str
    metadata: Dict
    content_validation: Dict
    content_complexity: Dict
    extracted_content: Dict
    processing_info: Dict

def create_content_approval_tasks(agents):
    """Create tasks for content approval workflow"""
    
    # Load guidelines
    guidelines = load_approval_guidelines()
    
    # Get current directory for directory tools
    current_dir = Path(__file__).parent
    
    # Base context structure all tasks will need
    base_context = {
        "description": "Content validation guidelines and rules",
        "expected_output": "Validation results based on guidelines",
        "guidelines": guidelines,
        "validation_rules": guidelines["podcast_content_requirements"]["validation_checks"],
        "content_criteria": guidelines["criteria"],
        "error_codes": RejectionOutput.model_config["error_codes"]
    }
    
    check_content = Task(
        description=(
            "Extract raw content from the provided source and perform basic content validation:\n"
            "1. Access the provided URL/file\n"
            "2. Extract text content based on source type:\n"
                "- Web pages (using web_scraper)\n"
                "- PDF documents (using pdf_reader)\n"
                "- Word documents (using docx_reader)\n"
                "- CSV files (using csv_reader)\n"
                "- Local directories (using directory_reader)\n"
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
        tools=agents["content_validator"].tools,
        output_pydantic=RejectionOutput,
        context=[base_context]
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
    
    return [check_content, approve_content, reject_content]

def task_completed_callback(output):
    """Callback function for task completion"""
    print(f"Task completed with status: {output.status}")
