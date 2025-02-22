import sys
import os
import unittest
import datetime
from pathlib import Path
import warnings
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tasks.gistaApp_tasks.gista_tasks import (
    create_all_gista_tasks,
    create_script_production_tasks,
    create_user_content_validation_tasks,
    create_user_content_research_tasks,
)
from agents.gistaApp_agents.gista_agents import create_gista_agents
from config.settings import validate_settings

def format_markdown(text: str) -> str:
    """Format text as markdown in notebook or plain text in terminal"""
    return text

def display_result(result):
    """Display result in markdown if in notebook, otherwise print"""
    if isinstance(result, dict):
        result = '\n'.join([f"**{k}**: {v}" for k, v in result.items()])
    return format_markdown(result)

def create_test_pipeline(content_source) -> Dict:
    """Create and run a test pipeline for content assessment and script production"""
    validate_settings()
    
    # Create all agents
    gista_agents = create_gista_agents()
    print(f"\nTest pipeline using agents with departments: {list(gista_agents.keys())}")
    
    # Create tasks for content assessment and script production only
    validation_tasks = create_user_content_validation_tasks(gista_agents["content_assessment"])
    research_tasks = create_user_content_research_tasks(gista_agents["content_assessment"], validation_tasks)
    script_tasks = create_script_production_tasks(gista_agents["script_production"])
    
    # Combine only the tasks we need for testing
    content_tasks = validation_tasks + research_tasks
    
    # Execute pipeline
    try:
        from crewai import Crew
        
        # 1. Content Assessment Crew
        content_crew = Crew(
            agents=[
                gista_agents["content_assessment"]["content_validator"],
                gista_agents["content_assessment"]["content_analyst"],
                gista_agents["content_assessment"]["technical_analyst"],
                gista_agents["content_assessment"]["research_specialist"]
            ],
            tasks=content_tasks,
            verbose=True,
            memory=False
        )
        
        # 2. Script Production Crew
        script_crew = Crew(
            agents=[
                gista_agents["script_production"]["transition_writer"],
                gista_agents["script_production"]["readout_script_writer"],
                gista_agents["script_production"]["segment_script_alpha"],
                gista_agents["script_production"]["segment_script_beta"],
                gista_agents["script_production"]["segment_script_gamma"],
                gista_agents["script_production"]["segment_script_omega"],
                gista_agents["script_production"]["transcript_generator"]
            ],
            tasks=script_tasks,
            verbose=True,
            memory=False
        )
        
        # Execute pipeline
        content_result = content_crew.kickoff(inputs={"content_source": content_source})
        
        if isinstance(content_result, dict):
            if content_result.get("content_status") == "CLEARED":
                script_result = script_crew.kickoff(inputs={"content_analysis": content_result})
                return {
                    "status": "completed",
                    "content_analysis": content_result,
                    "script_generation": script_result
                }
            return {
                "status": "content_rejected",
                "details": content_result
            }
        return {"status": "error", "details": "Invalid content result"}
    except Exception as e:
        return {"status": "error", "details": str(e)}

class TestGistaWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test environment once before all tests"""
        print("\n=== Starting Gista Workflow Tests ===\n")

    def setUp(self):
        """Set up test environment before each test"""
        self.test_data_dir = Path("CrewAI/tests/test_data")
        self.test_data_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.output_dir = self.test_data_dir / f"gista_outputs_{timestamp}"
        self.output_dir.mkdir(exist_ok=True)
        
        # Test content paths
        self.pdf_source = "/Users/tonynlemadim/Downloads/Economic Impact of AGI and Superintelligence – An Academic Analysis.pdf"
        self.invalid_article = self.test_data_dir / "invalid_article.md"
        
        self.invalid_article.write_text("Too short to be valid.")
        
        validate_settings()
        print(f"\n--- Running: {self._testMethodName} ---")

    def tearDown(self):
        """Clean up after each test"""
        if self.invalid_article.exists():
            self.invalid_article.unlink()

    def test_content_assessment(self):
        """Test the content assessment phase"""
        print("\nTesting content assessment phase...")
        result = create_test_pipeline(self.pdf_source)
        
        self.assertIn("content_analysis", result)
        content_analysis = result["content_analysis"]
        
        # Verify content analysis structure
        self.assertIn("content_map", content_analysis)
        self.assertIn("relationship_map", content_analysis)
        self.assertIn("analysis_metrics", content_analysis)
        
        print("\n✓ Content assessment test completed successfully")

    def test_script_generation(self):
        """Test the script generation phase"""
        print("\nTesting script generation phase...")
        result = create_test_pipeline(self.pdf_source)
        
        if result["status"] == "completed":
            self.assertIn("script_generation", result)
            script_result = result["script_generation"]
            
            # Verify script components
            self.assertIn("readout_script", script_result)
            self.assertIn("segment_scripts", script_result)
            
            print("\n✓ Script generation test completed successfully")

    def test_content_rejection(self):
        """Test content rejection scenarios"""
        print("\nTesting content rejection...")
        result = create_test_pipeline(str(self.invalid_article))
        
        self.assertEqual(result["status"], "content_rejected")
        self.assertIn("details", result)
        
        print("\n✓ Content rejection test completed successfully")

    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests are done"""
        print("\n=== Completed Gista Workflow Tests ===\n")

if __name__ == '__main__':
    unittest.main(verbosity=2)
