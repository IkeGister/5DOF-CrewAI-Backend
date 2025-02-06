from crewai import Agent
from typing import Dict, List

class VoiceGenerationAgent(Agent):
    """Agent responsible for converting parsed script into audio segments"""
    
    def __init__(self, voice_tool, parser_tool):
        super().__init__(
            name="Voice Generation Agent",
            goal="Generate high-quality voice segments from podcast scripts",
            backstory="Expert in audio production and voice synthesis",
            tools=[voice_tool, parser_tool]
        )

    async def generate_podcast(self, script_content: str) -> Dict:
        # Parse script
        parsed_segments = self.tools["parser"].run(script_content)
        
        # Generate audio for each segment
        audio_segments = []
        for segment in parsed_segments["segments"]:
            audio = await self.tools["voice"].run(
                text=segment.text,
                voice_role=segment.voice_role,
                segment_type=segment.segment_type
            )
            audio_segments.append(audio)
            
        return {
            "audio_segments": audio_segments,
            "metadata": parsed_segments["metadata"]
        } 