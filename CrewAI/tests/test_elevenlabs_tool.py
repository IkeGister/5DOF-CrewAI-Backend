import os
import unittest
import yaml
from pathlib import Path
from dotenv import load_dotenv
from ..tools.gista_tools.elevenLabs_voiceover_tool import ElevenLabsVoiceoverTool

# Load environment variables from .env file
load_dotenv()

class TestElevenLabsVoiceoverTool(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test method"""
        # Check if API key is set in environment
        if not os.getenv("ELEVENLABS_API_KEY"):
            self.skipTest("ELEVENLABS_API_KEY not set in environment")
        
        # Load voice config
        config_path = Path(__file__).parent.parent / "config" / "voice_config.yaml"
        with open(config_path, 'r') as f:
            self.voice_config = yaml.safe_load(f)
        
        self.tool = ElevenLabsVoiceoverTool()
        self.test_text = "This is a test of the ElevenLabs voice generation system."
        self.test_output_path = "test_output.mp3"

    def tearDown(self):
        """Clean up after each test method"""
        # Remove test output file if it exists
        if os.path.exists(self.test_output_path):
            os.remove(self.test_output_path)

    def test_simple_voiceover_with_host_voice(self):
        """Test voice generation with host voice from config"""
        result = self.tool.test_simple_voiceover(
            text=self.test_text,
            output_path=self.test_output_path,
            voice_id=self.voice_config['voices']['host']
        )
        
        # Print file information
        if result["status"] == "success":
            file_path = os.path.abspath(result["file_path"])
            file_size = os.path.getsize(file_path)
            print(f"\nAudio file generated at: {file_path}")
            print(f"File size: {file_size/1024:.2f} KB")
        
        self.assertEqual(result["status"], "success")
        self.assertTrue(os.path.exists(result["file_path"]))
        self.assertEqual(result["voice_id"], self.voice_config['voices']['host'])

    def test_simple_voiceover_empty_text(self):
        """Test voice generation with empty text"""
        result = self.tool.test_simple_voiceover(
            text="",
            output_path=self.test_output_path,
            voice_id=self.voice_config['voices']['host']
        )
        
        self.assertEqual(result["status"], "error")
        self.assertIn("message", result)

if __name__ == '__main__':
    unittest.main() 