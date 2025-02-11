"""
Content Approval Tests
=====================

Test suite for content approval functionality.
Tests the ContentApprovalTeam's ability to validate different content types.
"""

import unittest
from pathlib import Path
import os
from typing import Dict

from .content_approval_team import ContentApprovalTeam
from .content_approval_tasks import RejectionOutput, ApprovalOutput

class TestContentApproval(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test resources"""
        cls.team = ContentApprovalTeam(verbose=False)
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
        # Test website search tool
        self.assertIn("website_search", self.team.get_tools())
        
        # Test website scraper
        self.assertIn("website_scraper", self.team.get_tools())
        
        # Test directory reader
        self.assertIn("directory_reader", self.team.get_tools())

    @classmethod
    def tearDownClass(cls):
        """Clean up after tests"""
        pass

def run_tests():
    """Run the test suite"""
    unittest.main()

if __name__ == "__main__":
    run_tests()
