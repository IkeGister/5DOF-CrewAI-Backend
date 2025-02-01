# Type stub file to help VS Code recognize the import
from typing import List, Any

class Crew:
    def __init__(self, agents: List[Any], tasks: List[Any], verbose: int = 0): ...
    def kickoff(self, inputs: dict) -> Any: ... 