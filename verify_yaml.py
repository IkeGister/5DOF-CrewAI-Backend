"""
Script to verify YAML configuration
"""
import yaml
from pathlib import Path

try:
    print("Checking YAML configuration...")
    yaml_path = Path(__file__).parent / "src" / "CrewAI" / "agents" / "gistaApp_agents" / "content_approval_team" / "content_approval_directories.yaml"
    
    print(f"Looking for YAML at: {yaml_path}")
    print(f"File exists: {yaml_path.exists()}")
    
    if yaml_path.exists():
        with open(yaml_path, 'r') as file:
            content = yaml.safe_load(file)
            print("\nYAML structure:")
            print("===============")
            print(content)
    else:
        print("\nWARNING: YAML file not found!")

except Exception as e:
    print(f"\nError checking YAML: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    raise 