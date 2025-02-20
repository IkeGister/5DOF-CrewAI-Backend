"""
CrewAI Backend Package
"""

from pathlib import Path
import sys

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# This can be empty or contain exports 