"""
ElevenLabs Voiceover Tool
=========================

Tool for generating voiceovers for Gista podcast segments using ElevenLabs API.
Handles both readout and Q&A segments with different voices.
"""

from crewai_tools import BaseTool
from pydantic.v1 import BaseModel, Field
from typing import List, Optional, Dict, Type, ClassVar
import os
from elevenlabs.client import ElevenLabs

class VoiceoverRequestSchema(BaseModel):
    """Schema for voiceover generation requests"""
    text: str = Field(..., description="Text to convert to speech")
    voice_role: str = Field(..., description="Role of the voice (host/expert)")
    segment_type: str = Field(..., description="Type of segment (readout/qa)")
    previous_segment_ids: Optional[List[str]] = Field(
        default=None, 
        description="IDs of previous segments for prosody continuity"
    )

    class Config:
        orm_mode = True

class ElevenLabsVoiceoverTool(BaseTool):
    """Tool for generating podcast segment voiceovers"""
    
    # Add model config to allow arbitrary types
    model_config = {
        "arbitrary_types_allowed": True
    }
    
    name: str = "ElevenLabs Voiceover Tool"
    description: str = "Generates voiceovers for podcast segments"
    args_schema: Type[VoiceoverRequestSchema] = VoiceoverRequestSchema
    
    # Instance variables need to be declared as class variables with types
    client: ElevenLabs = None
    model_id: str = "eleven_monolingual_v1"

    # Voice IDs with type annotation
    VOICE_IDS: ClassVar[Dict[str, str]] = {
        "host": "Rc9yNQZlJL2KQBPZR6HM",
        "expert": "voice_id_for_expert",
        "readout": "voice_id_for_readout"
    }

    def __init__(self):
        super().__init__()
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable not set")
        self.client = ElevenLabs(api_key=api_key)

    def _run(
        self, 
        text: str,
        voice_role: str,
        segment_type: str,
        previous_segment_ids: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate voiceover for a segment

        Args:
            text: The text to convert to speech
            voice_role: Role of the voice (host/expert)
            segment_type: Type of segment (readout/qa)
            previous_segment_ids: Optional IDs of previous segments
        """
        try:
            voice_id = self.VOICE_IDS.get(voice_role)
            if not voice_id:
                raise ValueError(f"Invalid voice role: {voice_role}")

            # Generate audio using the client with minimal parameters
            response = self.client.generate(
                text=text,
                voice=voice_id
            )

            # Convert generator to bytes
            audio_data = b''.join(response)

            return {
                "audio": audio_data,
                "segment_info": {
                    "type": segment_type,
                    "role": voice_role,
                    "length": len(text)
                }
            }

        except Exception as e:
            return {
                "error": str(e),
                "segment_info": {
                    "type": segment_type,
                    "role": voice_role
                }
            }

    def generate_conversation(
        self,
        qa_pairs: List[Dict[str, str]],
        previous_ids: Optional[List[str]] = None
    ) -> Dict:
        """
        Generate a complete Q&A conversation

        Args:
            qa_pairs: List of Q&A pairs with host questions and expert answers
            previous_ids: Optional IDs from previous segments
        """
        conversation_segments = []
        current_ids = previous_ids or []

        for pair in qa_pairs:
            # Generate host question
            question_audio = self._run(
                text=pair["question"],
                voice_role="host",
                segment_type="qa",
                previous_segment_ids=current_ids
            )
            if "error" not in question_audio:
                current_ids.append(question_audio["segment_info"]["request_id"])
            conversation_segments.append(question_audio)

            # Generate expert answer
            answer_audio = self._run(
                text=pair["answer"],
                voice_role="expert",
                segment_type="qa",
                previous_segment_ids=current_ids
            )
            if "error" not in answer_audio:
                current_ids.append(answer_audio["segment_info"]["request_id"])
            conversation_segments.append(answer_audio)

        return {
            "segments": conversation_segments,
            "segment_ids": current_ids
        }

    def get_voiceover_implementation_guidelines(self) -> Dict:
        """
        Implementation guidelines for ElevenLabs voiceover generation.
        Provides detailed specifications for voice roles, segment types,
        audio settings, and usage patterns.
        """
        return {
            "voice_roles": {
                "host": {
                    "description": "Main presenter/interviewer voice",
                    "characteristics": [
                        "Clear and professional",
                        "Engaging tone",
                        "Natural pacing",
                        "Consistent delivery"
                    ],
                    "usage": "For questions and segment introductions"
                },
                "expert": {
                    "description": "Subject matter expert voice",
                    "characteristics": [
                        "Authoritative tone",
                        "Measured pacing",
                        "Clear articulation",
                        "Professional delivery"
                    ],
                    "usage": "For detailed explanations and answers"
                },
                "readout": {
                    "description": "Document readout voice",
                    "characteristics": [
                        "Neutral tone",
                        "Steady pace",
                        "Clear pronunciation",
                        "Consistent delivery"
                    ],
                    "usage": "For verbatim document content"
                }
            },
            "segment_types": {
                "readout": {
                    "format": "Single continuous narration",
                    "requirements": [
                        "Clear paragraph breaks",
                        "Proper citation markers",
                        "Source attribution",
                        "Section transitions"
                    ]
                },
                "qa": {
                    "format": "Interactive dialogue",
                    "structure": {
                        "question": "Clear, focused inquiry",
                        "answer": "Detailed, informative response",
                        "timing": "Natural conversation flow"
                    }
                }
            },
            "audio_settings": {
                "voice_settings": {
                    "stability": {
                        "value": 0.75,
                        "purpose": "Maintains consistent voice characteristics"
                    },
                    "similarity_boost": {
                        "value": 0.75,
                        "purpose": "Ensures voice remains true to selected profile"
                    }
                },
                "model_settings": {
                    "model_id": "eleven_monolingual_v1",
                    "capabilities": [
                        "High-quality speech synthesis",
                        "Natural prosody",
                        "Consistent delivery"
                    ]
                }
            },
            "usage_patterns": {
                "single_segment": {
                    "method": "_run",
                    "parameters": {
                        "text": "Content to be converted to speech",
                        "voice_role": "Role of the speaker (host/expert/readout)",
                        "segment_type": "Type of segment (readout/qa)",
                        "previous_segment_ids": "Optional IDs for continuity"
                    },
                    "example": """
                        tool._run(
                            text="What are the key findings of this research?",
                            voice_role="host",
                            segment_type="qa"
                        )
                    """
                },
                "conversation": {
                    "method": "generate_conversation",
                    "parameters": {
                        "qa_pairs": "List of question-answer dictionaries",
                        "previous_ids": "Optional IDs from previous segments"
                    },
                    "example": """
                        tool.generate_conversation(
                            qa_pairs=[
                                {
                                    "question": "What is the main concept?",
                                    "answer": "The main concept involves..."
                                }
                            ]
                        )
                    """
                }
            },
            "best_practices": {
                "text_preparation": [
                    "Keep segments under 4000 characters",
                    "Include proper punctuation",
                    "Mark emphasis points clearly",
                    "Use consistent formatting"
                ],
                "voice_continuity": [
                    "Use previous_segment_ids for connected speech",
                    "Maintain consistent voice roles",
                    "Keep conversation flow natural",
                    "Ensure proper transitions"
                ],
                "error_handling": [
                    "Check for API key before use",
                    "Validate voice roles",
                    "Handle response errors gracefully",
                    "Maintain segment information even on failure"
                ]
            }
        }

    def test_simple_voiceover(
        self, 
        text: str, 
        output_path: str = "test_output.mp3",
        voice_id: Optional[str] = None
    ) -> Dict:
        """
        Simple test method to generate and save a voiceover file

        Args:
            text: The text to convert to speech
            output_path: Path where to save the mp3 file (default: test_output.mp3)
            voice_id: Optional voice ID to use (defaults to host voice if not provided)

        Returns:
            Dict containing status and file path if successful
        """
        try:
            # Validate text is not empty
            if not text.strip():
                return {
                    "status": "error",
                    "message": "Text cannot be empty"
                }

            # Use provided voice_id or default to host voice
            voice_id = voice_id or self.VOICE_IDS["host"]
            
            # Generate audio using the client with minimal parameters
            response = self.client.generate(
                text=text,
                voice=voice_id
            )

            # Save the audio to file - handle generator response
            with open(output_path, 'wb') as f:
                for chunk in response:
                    f.write(chunk)

            return {
                "status": "success",
                "file_path": output_path,
                "message": f"Audio file saved to {output_path}",
                "voice_id": voice_id
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
