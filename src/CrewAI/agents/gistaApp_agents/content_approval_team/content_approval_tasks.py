"""
Content Approval Tasks Module
===========================

This module defines tasks for content approval workflow:
1. check_content - Initial content validation
2. approve_content - Process approved content
3. reject_content - Handle rejected content
"""

from crewai import Task
from typing import Dict, List, Optional, Any  # Keep only needed types
import yaml

def validate_content_tasks(content_validator, guidelines, content_source: str):
    """
    Create tasks for content validation workflow
    
    Args:
        content_validator: The agent that will validate content
        guidelines: The YAML guidelines document to review
        content_source: The content to be validated
    """
    # Format guidelines as a readable string
    guidelines_str = yaml.dump(guidelines, default_flow_style=False)
    
    read_guidelines = Task(
        description=(
            "Review and understand these content approval guidelines:\n\n"
            f"{guidelines_str}\n\n"
            "Analyze and confirm understanding of:\n"
            "1. Content Acceptance Criteria\n"
            "   - Accepted content types\n"
            "   - Length requirements\n"
            "   - Special case handling\n\n"
            "2. Rejection Criteria\n"
            "   - Content-based rejections\n"
            "   - Technical rejections\n\n"
            "3. Metadata Requirements\n"
            "   - Required fields\n"
            "   - Optional fields\n"
            "   - Validation rules\n\n"
            "4. Quality Requirements\n"
            "   - Basic requirements\n"
            "   - Quality markers\n\n"
            "5. Podcast-Specific Requirements\n"
            "   - Content types\n"
            "   - Restrictions\n"
            "   - Accessibility requirements"
        ),
        expected_output="Confirmation of guidelines review completion",
        agent=content_validator
    )

    detect_content_nature = Task(
        description=(
            "Analyze the provided content source and determine its nature:\n"
            f"Content source: {content_source}\n\n"
            "Determine:\n"
            "1. Content Type:\n"
            "   - Is it a URL? (starts with http/https)\n"
            "   - Is it a PDF? (.pdf extension)\n"
            "   - Is it a document? (.docx/.doc extension)\n"
            "   - Is it something else? (specify)\n\n"
            "2. Basic Accessibility:\n"
            "   - Can the content be accessed?\n"
            "   - Are there any immediate access barriers?\n\n"
            "3. Initial Assessment:\n"
            "   - Does it match any accepted content types from guidelines?\n"
            "   - Are there any immediate red flags?\n"
            "   - What validation approach should be used?"
        ),
        expected_output=(
            "A structured analysis containing:\n"
            "- content_type: The detected type\n"
            "- accessibility: Initial access check results\n"
            "- validation_approach: Recommended next steps\n"
            "- concerns: Any immediate issues found"
        ),
        agent=content_validator
    )

    def validate_content_quality(agent, content_source: str, guidelines: dict) -> Task:
        """Create a task for validating content quality."""
        return Task(
            description=f"""
            Using the content approval guidelines you just reviewed, validate the content at {content_source}.
            
            Focus on:
            1. Content accessibility and readability
            2. Content type matches accepted types
            3. Content length meets requirements
            4. Content quality meets basic requirements
            
            If content meets all requirements:
            - Use appropriate success code (ACC200-ACC203)
            - Set status as "approved"
            - Set production_state as "in_production"
            
            If content fails any requirement:
            - Use appropriate error code (ACC001-004, CON001-004, etc.)
            - Set status as "rejected"
            - Set production_state as "invalid_content"
            """,
            
            expected_output="""
            JSON object with:
            {
                "status": "approved" or "rejected",
                "production_state": "in_production" or "invalid_content",
                "code": "<appropriate status code>",
                "message": "<brief explanation>",
                "validation_details": {
                    "accessibility": "status",
                    "quality_check": "result",
                    "criteria_met": ["list of met criteria"],
                    "issues_found": ["list of any issues"]
                }
            }
            """,
            agent=agent
        )

    validate_content_quality_task = validate_content_quality(
        agent=content_validator,
        content_source=content_source,
        guidelines=guidelines
    )

    return [read_guidelines, detect_content_nature, validate_content_quality_task]

def task_completed_callback(output):
    """Callback function for task completion"""
    print(f"Task completed with status: {output.status}")

# class RejectionOutput(BaseModel):
#     """Output model for content rejection"""
#     model_config = ConfigDict(extra='allow')
    
#     ERROR_CODES: ClassVar[Dict[str, str]] = {
#         'INVALID_URL': 'URL is invalid or inaccessible',
#         'MALICIOUS_CONTENT': 'Content contains malicious elements',
#         'ACCESS_BLOCKED': 'Content access is blocked (paywall/login)',
#         'CONTENT_TYPE': 'Unsupported content type',
#         'INSUFFICIENT_LENGTH': 'Content length below minimum requirement',
#         'EXCESSIVE_LENGTH': 'Content length exceeds maximum limit',
#         'FORMAT_ERROR': 'Content format is invalid or corrupted',
#         'BOT_DETECTION': 'Site blocks automated access',
#         'SECURITY_RISK': 'Security concerns detected',
#         'NO_TEXT_CONTENT': 'No extractable text content found'
#     }
    
#     status: str = "rejected"
#     error_code: str
#     error_message: str
#     rejection_reason: str
#     suggestions: Optional[List[str]] = None
#     metadata: Dict = {}

# class ApprovalOutput(BaseModel):
#     """Output model for content approval tasks"""
#     model_config = ConfigDict(extra='allow')
    
#     status: str
#     content_status: str
#     metadata: Dict[str, Any]
#     content_validation: Dict[str, Any]
#     content_complexity: Dict[str, Any]
#     extracted_content: Dict[str, Any]
#     processing_info: Dict[str, Any]

# class ContentTypeOutput(BaseModel):
#     """Output model for content type detection"""
#     model_config = ConfigDict(extra='allow')
    
#     content_type: str  # "url", "pdf", "docx", "unknown"
#     content_path: str
#     validation_tools: List[str]
#     error_message: Optional[str] = None

# def detect_content_type(content_path: str) -> str:
#     """Helper function to detect content type from path or URL"""
#     # URL pattern
#     url_pattern = r'^(http|https):\/\/'
    
#     if re.match(url_pattern, content_path):
#         return "url"
    
#     # File extension check
#     file_extension = Path(content_path).suffix.lower()
#     if file_extension in ['.pdf']:
#         return "pdf"
#     elif file_extension in ['.docx', '.doc']:
#         return "docx"
    
#     return "unknown"

# def create_content_approval_tasks(agents):
#     """Create tasks for content approval workflow"""
    
#     # Base context structure all tasks will need
#     base_context = {
#         "description": "Content validation guidelines and rules",
#         "expected_output": "Validation results based on guidelines",
#         "error_codes": RejectionOutput.ERROR_CODES
#     }
    
#     def wrap_task_with_early_exit(task):
#         """
#         Creates a new task that implements early exit functionality
#         """
#         return Task(
#             description=task.description,
#             expected_output=task.expected_output,
#             agent=task.agent,
#             tools=task.tools,
#             context=task.context,
#             output_pydantic=task.output_pydantic,
#             async_execution=task.async_execution,
#             callback=task.callback
#         )

#     # Content type detection task
#     detect_content = Task(
#         description=(
#             "Analyze the provided content path and determine its type:\n"
#             "1. Check if the content is a URL (starts with http/https)\n"
#             "2. Check if the content is a PDF file (.pdf extension)\n"
#             "3. Check if the content is a Word document (.docx/.doc extension)\n"
#             "4. Determine appropriate validation tools based on content type\n"
#             "5. Return error if content type is unsupported"
#         ),
#         expected_output=(
#             "A structured response containing:\n"
#             "- content_type: The detected type (url/pdf/docx/unknown)\n"
#             "- content_path: The original content path\n"
#             "- validation_tools: List of appropriate tools for this content\n"
#             "- error_message: Any error encountered (if applicable)"
#         ),
#         agent=agents["content_validator"],
#         tools=[],  # No tools needed for type detection
#         output_pydantic=ContentTypeOutput
#     )

#     return [detect_content]