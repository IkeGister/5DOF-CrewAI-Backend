from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import Dict, Optional

class TranscriptionRequest(BaseModel):
    """Schema for transcription requests"""
    segments: list = Field(..., description="List of podcast segments")
    metadata: Dict = Field(..., description="Podcast metadata")
    format_type: str = Field(
        default="clean",
        description="Transcript format type (clean/detailed/timestamped)"
    )

class TranscriptionTool(BaseTool):
    """Tool for generating podcast transcripts in various formats"""
    
    name: str = "Transcription Tool"
    description: str = "Generates clean transcripts from podcast segments"
    args_schema: type[BaseModel] = TranscriptionRequest

    def _run(
        self, 
        segments: list,
        metadata: Dict,
        format_type: str = "clean"
    ) -> Dict:
        """
        Generate transcript from podcast segments
        
        Args:
            segments: List of podcast segments
            metadata: Podcast metadata
            format_type: Type of transcript format to generate
        """
        try:
            if format_type == "clean":
                transcript = self._generate_clean_transcript(segments, metadata)
            elif format_type == "detailed":
                transcript = self._generate_detailed_transcript(segments, metadata)
            elif format_type == "timestamped":
                transcript = self._generate_timestamped_transcript(segments, metadata)
            else:
                transcript = self._generate_clean_transcript(segments, metadata)

            return {
                "status": "success",
                "transcript": transcript,
                "metadata": metadata,
                "format": format_type
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    def _generate_clean_transcript(self, segments: list, metadata: Dict) -> str:
        """Generate a clean, readable transcript"""
        transcript = [f"# {metadata['title']}\n"]
        transcript.append(f"Source: {metadata['source']}\n\n")
        
        for segment in segments:
            speaker = segment.voice_role.upper()
            text = segment.text.replace("//", "")  # Remove pause markers
            transcript.append(f"{speaker}: {text}\n\n")
            
        return "".join(transcript)

    def _generate_detailed_transcript(self, segments: list, metadata: Dict) -> str:
        """Generate a detailed transcript with segment types and markers"""
        transcript = [f"# {metadata['title']}\n"]
        transcript.append(f"Source: {metadata['source']}\n\n")
        
        for segment in segments:
            transcript.append(f"[{segment.segment_type.upper()}]\n")
            transcript.append(f"{segment.voice_role.upper()}: {segment.text}\n\n")
            
        return "".join(transcript)

    def _generate_timestamped_transcript(self, segments: list, metadata: Dict) -> str:
        """Generate a transcript with timestamp markers"""
        transcript = [f"# {metadata['title']}\n"]
        transcript.append(f"Source: {metadata['source']}\n\n")
        
        for i, segment in enumerate(segments):
            timestamp = f"[{i * 30:02d}:00]"  # Simple timestamp estimation
            transcript.append(f"{timestamp} {segment.voice_role.upper()}: {segment.text}\n\n")
            
        return "".join(transcript) 