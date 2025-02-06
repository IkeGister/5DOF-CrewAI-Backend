from crewai import Agent
from typing import Dict

class TranscriptAgent(Agent):
    """Agent responsible for creating clean transcripts from podcast scripts"""
    
    def __init__(self, transcription_tool):
        super().__init__(
            name="Transcript Generator",
            goal="Create accurate and well-formatted transcripts of podcast content",
            backstory=(
                "Expert in converting complex audio content into clear, "
                "readable transcripts while maintaining proper attribution "
                "and speaker identification."
            ),
            tools=[transcription_tool]
        )

    async def execute_task(self, task_context: Dict) -> Dict:
        """Execute transcription task"""
        try:
            # Get parsed segments from previous task
            parsed_segments = task_context.get("parsed_segments")
            if not parsed_segments:
                return {
                    "status": "error",
                    "message": "No parsed segments provided"
                }

            # Generate transcript using the tool
            result = await self.tools["transcription"].run(
                segments=parsed_segments["segments"],
                metadata=parsed_segments["metadata"],
                format_type=task_context.get("format_type", "clean")
            )

            return result

        except Exception as e:
            return {
                "status": "error",
                "message": f"Transcription failed: {str(e)}"
            } 