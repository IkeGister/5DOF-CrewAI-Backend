"""
Content Approval Test Runner
==========================

Dedicated test runner for content approval functionality.
Runs all content approval related tests and provides detailed output.

Test Categories:
1. Task Progression Tests
2. Content Type Tests
3. Access Tests
4. Tool Usage Tests

Usage:
    python run_content_approval_tests.py [--category <test_category>] [--verbose]
"""

import unittest
import sys
import argparse
from pathlib import Path
from typing import Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add project root to Python path to resolve imports
project_root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(project_root))

from CrewAI.agents.gistaApp_agents.content_approval_team.content_approval_tests import TestContentApproval

def run_content_approval_tests(category: Optional[str] = None, verbose: bool = False) -> int:
    """
    Run the content approval test suite
    
    Args:
        category: Optional test category to run ('progression', 'content', 'access', 'tools')
        verbose: Enable detailed test output
    
    Returns:
        int: 0 for success, 1 for failures
    """
    
    # Create test suite
    loader = unittest.TestLoader()
    
    if category:
        # Filter tests by category
        test_pattern = f'test_{category}'
        suite = unittest.TestLoader().loadTestsFromTestCase(TestContentApproval)
        filtered_suite = unittest.TestSuite()
        for test in suite:
            if test_pattern in test._testMethodName:
                filtered_suite.addTest(test)
        suite = filtered_suite
    else:
        suite = loader.loadTestsFromTestCase(TestContentApproval)
    
    # Configure test runner
    runner = unittest.TextTestRunner(
        verbosity=2 if verbose else 1,
        descriptions=True,
        failfast=False
    )
    
    print("\nRunning Content Approval Tests...")
    print("=" * 50)
    
    if category:
        print(f"Running {category.upper()} tests only")
    
    # Run tests and capture results
    result = runner.run(suite)
    
    # Print summary
    print("\nTest Summary:")
    print("-" * 20)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.failures:
        print("\nFailures:")
        for failure in result.failures:
            print(f"- {failure[0]}: {failure[1]}")
    
    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"- {error[0]}: {error[1]}")
    
    # Return appropriate exit code
    return 0 if result.wasSuccessful() else 1

def main():
    """Command line interface for test runner"""
    logger.debug("Starting test execution...")
    
    try:
        parser = argparse.ArgumentParser(description='Run Content Approval Tests')
        parser.add_argument(
            '--category',
            choices=['progression', 'content', 'access', 'tools'],
            help='Specific test category to run'
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Enable verbose output'
        )
        args = parser.parse_args()
        
        logger.debug(f"Running tests with category: {args.category}, verbose: {args.verbose}")
        exit_code = run_content_approval_tests(args.category, args.verbose)
        logger.debug("Tests completed")
        sys.exit(exit_code)
        
    except Exception as e:
        logger.error(f"Error during test execution: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
