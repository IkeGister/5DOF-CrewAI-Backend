"""
Content Approval Test Suite
==========================

This test suite validates the content approval workflow with four main categories:

1. Task Progression Tests
------------------------
- Verifies tasks execute in correct order: detect_content -> check_content -> approve/reject
- Ensures task dependencies and context passing
- Tests early rejection for invalid content
Expected outcomes:
- Valid content: detect -> check -> approve
- Invalid content: detect -> reject
- Proper context passing between tasks

2. Content Type Tests
--------------------
- Tests handling of different content formats:
  * URLs (valid, invalid, paywalled)
  * PDFs
  * DOCX files
Expected outcomes:
- Correct content type detection
- Appropriate tool selection
- Proper validation based on type

3. Access Tests
--------------
- Tests handling of:
  * Paywalled content
  * Sign-in required content
  * Invalid/non-existent content
Expected outcomes:
- Early rejection with appropriate error codes
- Clear rejection reasons
- Helpful suggestions

4. Tool Usage Tests
------------------
- Validates tool selection based on content type
- Ensures tools receive proper configuration
- Checks tool execution order
Expected outcomes:
- URL content uses web tools
- PDF content uses PDF tools
- DOCX content uses document tools

Test Resources
-------------
- test_urls: Dictionary of test URLs (valid, invalid, paywalled)
- test_files: Dictionary of test files (PDF, DOCX)
- validation helpers: Methods to check response structures

Usage:
    python -m unittest content_approval_tests.py -v
"""

import unittest
from pathlib import Path
import os
from typing import Dict, List
from unittest.mock import patch

from .content_approval_team import ContentApprovalTeam
from .content_approval_tasks import ContentTypeOutput, RejectionOutput, ApprovalOutput

class TestContentApproval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test resources"""
        cls.team = ContentApprovalTeam(verbose=True)  # Enable verbose for task tracking
        cls.test_objects_path = Path(__file__).parent.parent.parent.parent / "test_objects"
        
        # Test URLs
        cls.test_urls = {
            "dummy": "https://nonexistent-domain-12345.com/article",
            "valid": "https://www.msn.com/en-us/news/world/russia-plays-hardball-on-ukraine-peace-discussions-after-trump-talks-of-putin-contact/ar-AA1yLUjo",
            "video": "https://www.youtube.com/watch?v=KDorKy-13ak",
            "paywall": "https://www.youtube.com/premium",
            "signin": "https://www.spellbook.legal/reviews"
        }
        
        # Test file paths with correct filenames
        cls.test_files = {
            "pdf": cls.test_objects_path / "test_pdf_Article.pdf",
            "image": cls.test_objects_path / "test_image.jpeg",
            "doc": cls.test_objects_path / "test_document.docx",
        }
        
        # Verify test files exist
        for file_type, file_path in cls.test_files.items():
            if not file_path.exists():
                print(f"Warning: Test file {file_type} not found at {file_path}")
    
    def validate_rejection_response(self, result: Dict) -> None:
        """Helper to validate rejection response structure"""
        self.assertEqual(result["status"], "rejected")
        self.assertIn("error_code", result)
        self.assertIn("error_message", result)
        self.assertIn("rejection_reason", result)
        self.assertIn("suggestions", result)
        
    def validate_approval_response(self, result: Dict) -> None:
        """Helper to validate approval response structure"""
        self.assertEqual(result["status"], "completed")
        self.assertIn("content_status", result)
        self.assertIn("details", result)

    def test_dummy_domain(self):
        """Test handling of non-existent domain"""
        result = self.team.process_content(self.test_urls["dummy"])
        self.validate_rejection_response(result)
        self.assertEqual(result["error_code"], "INVALID_URL")

    def test_valid_url(self):
        """Test processing of valid URL"""
        result = self.team.process_content(self.test_urls["valid"])
        self.validate_approval_response(result)
        
        # Additional checks for valid news article
        if result.get("details"):
            content_details = result["details"]
            self.assertIn("metadata", content_details)
            self.assertIn("content_validation", content_details)
            
            # Verify it's a news article
            if content_details.get("metadata"):
                self.assertIn("source", content_details["metadata"])
                self.assertEqual(content_details["metadata"]["source"], "msn.com")

    def test_video_content(self):
        """Test rejection of video content"""
        result = self.team.process_content(self.test_urls["video"])
        self.validate_rejection_response(result)
        self.assertEqual(result["error_code"], "CONTENT_TYPE")
        
        # Additional checks specific to video rejection
        self.assertIn("video", result["rejection_reason"].lower())
        self.assertTrue(
            any("youtube" in suggestion.lower() for suggestion in result["suggestions"]),
            "Suggestions should mention YouTube alternatives"
        )

    def test_pdf_document(self):
        """Test processing of PDF document"""
        if self.test_files["pdf"].exists():
            result = self.team.process_content(str(self.test_files["pdf"]))
            self.validate_approval_response(result)
        else:
            self.skipTest("PDF test file not found")

    def test_image_file(self):
        """Test rejection of image file"""
        if self.test_files["image"].exists():
            result = self.team.process_content(str(self.test_files["image"]))
            self.validate_rejection_response(result)
            self.assertEqual(result["error_code"], "CONTENT_TYPE")
        else:
            self.skipTest("Image test file not found")

    def test_paywall_content(self):
        """Test handling of paywalled content"""
        result = self.team.process_content(self.test_urls["paywall"])
        self.validate_rejection_response(result)
        self.assertEqual(result["error_code"], "ACCESS_BLOCKED")
        
        # Additional checks specific to paywall rejection
        self.assertTrue(
            any(keyword in result["rejection_reason"].lower() 
                for keyword in ["premium", "subscription", "paywall"]),
            "Rejection reason should mention premium/subscription requirement"
        )
        
        # Verify metadata includes paywall information
        if result.get("metadata"):
            self.assertIn("access_type", result["metadata"])
            self.assertEqual(result["metadata"]["access_type"], "premium")

    def test_signin_required(self):
        """Test handling of content requiring sign-in"""
        result = self.team.process_content(self.test_urls["signin"])
        self.validate_rejection_response(result)
        self.assertEqual(result["error_code"], "ACCESS_BLOCKED")
        self.assertIn("sign-in", result["rejection_reason"].lower())  # Verify reason mentions sign-in

    def test_tool_functionality(self):
        """Test if tools are working correctly"""
        tools = self.team.get_tools()
        self.assertIsInstance(tools, dict)
        # Test that tools exist when needed
        self.team.process_content(self.test_urls["valid"])
        tools = self.team.get_tools()
        self.assertGreater(len(tools), 0)

    def test_task_progression(self):
        """
        Test task execution order and progression.
        
        Expected Flows:
        1. Valid content:
           detect_content -> check_content -> approve_content
        
        2. Invalid content:
           detect_content -> reject_content
        
        3. Valid but restricted content:
           detect_content -> check_content -> reject_content
        """
        executed_tasks = []
        
        def track_task_execution(task_output):
            """Callback to track task execution order"""
            task_name = task_output.get("task_name", "unknown")
            executed_tasks.append(task_name)
        
        # Create team with task tracking
        team = ContentApprovalTeam(verbose=True)
        team.task_callback = track_task_execution
        
        # Process a valid URL
        result = team.process_content(self.test_urls["valid"])
        
        # Verify task order
        expected_order = ["detect_content", "check_content", "approve_content"]
        self.assertEqual(executed_tasks, expected_order)

    def test_task_dependencies(self):
        """Test that tasks receive proper context from previous tasks"""
        with patch('crewai.Task.execute') as mock_execute:
            # Process content
            self.team.process_content(self.test_urls["valid"])
            
            # Get all task calls
            calls = mock_execute.call_args_list
            
            # Verify check_content received detect_content output
            check_content_call = calls[1]
            self.assertIn('context', check_content_call.kwargs)
            self.assertIsInstance(
                check_content_call.kwargs['context'].get('content_type_result'),
                ContentTypeOutput
            )

    def test_early_rejection(self):
        """Test that invalid content is rejected early"""
        executed_tasks = []
        
        def track_task_execution(task_output):
            task_name = task_output.get("task_name", "unknown")
            executed_tasks.append(task_name)
        
        team = ContentApprovalTeam(verbose=True)
        team.task_callback = track_task_execution
        
        # Process invalid content
        result = team.process_content(self.test_urls["dummy"])
        
        # Verify only detection and rejection tasks ran
        expected_order = ["detect_content", "reject_content"]
        self.assertEqual(executed_tasks, expected_order)

    def test_tool_selection(self):
        """
        Test dynamic tool selection based on content type.
        
        Expected Tools:
        - URLs: website_search, website_scraper
        - PDFs: pdf_reader
        - DOCX: docx_reader
        
        Tools should be:
        1. Correctly configured with content path
        2. Only relevant tools available to task
        3. Properly initialized with necessary credentials
        """
        # Test URL content
        result = self.team.process_content(self.test_urls["valid"])
        task_tools = self.team.get_tasks()[1].tools  # check_content task
        self.assertTrue(
            any(tool.name == "website_search" for tool in task_tools),
            "URL content should use website search tool"
        )
        
        # Test PDF content
        if self.test_files["pdf"].exists():
            result = self.team.process_content(str(self.test_files["pdf"]))
            task_tools = self.team.get_tasks()[1].tools
            self.assertTrue(
                any(tool.name == "pdf_reader" for tool in task_tools),
                "PDF content should use PDF reader tool"
            )

    def validate_task_output(self, task_output: Dict, expected_type: type) -> None:
        """Helper to validate task output structure"""
        self.assertIsInstance(task_output, expected_type)
        if expected_type == ContentTypeOutput:
            self.assertIn("content_type", task_output)
            self.assertIn("validation_tools", task_output)
        elif expected_type in [ApprovalOutput, RejectionOutput]:
            self.assertIn("status", task_output)
            self.assertIn("metadata", task_output)

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        pass

def run_tests():
    """Run the test suite"""
    unittest.main(verbosity=2)  # Increased verbosity for better test output

if __name__ == "__main__":
    run_tests()
