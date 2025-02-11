"""
Content Approval Test Runner
==========================

Dedicated test runner for content approval functionality.
Runs all content approval related tests and provides detailed output.
"""

import unittest
import sys
from pathlib import Path

# Add project root to Python path to resolve imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from CrewAI.agents.gistaApp_agents.content_approval_team.content_approval_tests import TestContentApproval

def run_content_approval_tests():
    """Run the content approval test suite"""
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestContentApproval)
    
    # Configure test runner with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        descriptions=True,
        failfast=False
    )
    
    print("\nRunning Content Approval Tests...")
    print("=" * 50)
    
    # Run tests and capture results
    result = runner.run(suite)
    
    # Print summary
    print("\nTest Summary:")
    print("-" * 20)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_content_approval_tests())
