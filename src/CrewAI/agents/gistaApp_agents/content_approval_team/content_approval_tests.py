"""
Content Approval Test Suite
==========================

This test suite validates the content approval workflow:
1. URL Content Rejection
2. URL Content Acceptance
"""

import unittest
import json
from pathlib import Path
from typing import Dict, Any, Tuple, List
from crewai import Crew, Task
from .content_approval_team import ContentApprovalTeam

class TestContentApproval(unittest.TestCase):
    """Test cases for content approval workflow"""
    
    def setUp(self):
        """Set up test environment before each test"""
        self.team = ContentApprovalTeam(verbose=True)
        self.example_url = "https://example.com/article"
        self.valid_url = "https://www.python.org"  # We'll use this later
    
    def test_invalid_url(self):
        """Test rejection flow with example.com placeholder content"""
        print("\n=== Testing Invalid URL Rejection ===")
        
        crew, tasks, _ = self.team.start_podcast_production_flow(
            content_source=self.example_url
        )
        
        # Print task sequence
        print("\nTask Sequence:")
        for i, task in enumerate(tasks):
            print(f"\nTask {i+1}:")
            print(f"Description: {task.description[:200]}...")
            print(f"Expected Output: {task.expected_output}")
        
        # Execute and print results
        result = crew.kickoff()
        print("\nExecution Results:")
        print(json.dumps(result, indent=2))
        
        # Parse the result string into a dictionary
        result_dict = json.loads(result)
        
        # Verify rejection
        self.assertEqual(result_dict.get("status"), "rejected")
        self.assertEqual(result_dict.get("production_state"), "invalid_content")
        self.assertEqual(result_dict.get("code"), "CON001")

    def test_url_content_approval(self):
        """Test approval flow with valid content from python.org"""
        print("\n=== Testing URL Content Approval ===")
        
        crew, tasks, _ = self.team.start_podcast_production_flow(
            content_source=self.valid_url
        )
        
        # Print task sequence
        print("\nTask Sequence:")
        for i, task in enumerate(tasks):
            print(f"\nTask {i+1}:")
            print(f"Description: {task.description[:200]}...")
            print(f"Expected Output: {task.expected_output}")
        
        # Execute and print results
        result = crew.kickoff()
        print("\nExecution Results:")
        print(json.dumps(result, indent=2))
        
        # Parse the result string into a dictionary
        result_dict = json.loads(result)
        
        # Verify approval
        self.assertEqual(result_dict.get("status"), "approved")
        self.assertEqual(result_dict.get("production_state"), "in_production")
        self.assertTrue(result_dict.get("code") in ["ACC200", "ACC201", "ACC202", "ACC203"])
        
        # Verify content quality
        validation_details = result_dict.get("validation_details", {})
        self.assertTrue("access" in validation_details.get("accessibility", "").lower())  # More flexible check
        self.assertTrue(len(validation_details.get("criteria_met", [])) > 0)
        self.assertEqual(len(validation_details.get("issues_found", [])), 0)

def run_tests():
    """Run the test suite"""
    unittest.main(verbosity=2)

if __name__ == "__main__":
    run_tests()
