from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import List, Dict, Any

class PodcastSegment(BaseModel):
    voice_role: str
    text: str
    segment_type: str
    pause_markers: List[int] = []
    emphasis_markers: List[Dict[str, int]] = []

class ScriptParserTool(BaseTool):
    name: str = "Script Parser Tool"
    description: str = "Converts markdown podcast scripts into structured segments"

    def _run(self, markdown_content: str) -> Dict[str, Any]:
        segments = []
        current_voice = None
        current_text = []
        
        for line in markdown_content.split('\n'):
            if line.strip().startswith('[') and line.strip().endswith(']'):
                # Process previous segment if exists
                if current_voice and current_text:
                    segments.append(PodcastSegment(
                        voice_role=current_voice.lower().replace(' voice', ''),
                        text=' '.join(current_text),
                        segment_type=self._determine_segment_type(current_voice, current_text)
                    ))
                # Start new segment
                current_voice = line.strip()[1:-1]
                current_text = []
            elif current_voice and line.strip():
                current_text.append(line.strip())

        return {
            "segments": segments,
            "metadata": {
                "title": self._extract_title(markdown_content),
                "source": self._extract_source(markdown_content)
            }
        }

    def _extract_title(self, content: str) -> str:
        return "Untitled"

    def _extract_source(self, content: str) -> str:
        return "Unknown"

    def _determine_segment_type(self, voice: str, text: List[str]) -> str:
        # Logic to determine if segment is readout, qa, intro, etc.
        if "host" in voice.lower():
            return "qa"
        return "readout"  # Default type 