# ElevenLabs Voiceover Tool Specification

## Overview
The ElevenLabs Voiceover Tool is designed to generate high-quality voice narrations for podcast segments. It integrates with the ElevenLabs API to convert text into natural-sounding speech, supporting different voice roles and segment types.

## Key Features
- Text-to-speech conversion using ElevenLabs' advanced AI voices
- Support for multiple voice roles (host, expert, readout)
- Handles different segment types (readout segments, Q&A conversations)
- Voice continuity management across segments
- Error handling and input validation
- Simple testing interface for voice generation

## How It Works

### Basic Usage
1. The tool accepts text input and a voice role
2. Connects to ElevenLabs using API authentication
3. Generates audio using the specified voice
4. Returns the audio data or saves it to a file

### Voice Roles
- **Host Voice**: Main narrator/interviewer voice for questions and introductions
- **Expert Voice**: Subject matter expert voice for detailed explanations
- **Readout Voice**: Neutral voice for document content narration

### Segment Types
1. **Readout Segments**: Continuous narration of content
2. **Q&A Segments**: Interactive dialogue between host and expert voices

## Technical Implementation

### Prerequisites
- ElevenLabs API key
- Voice IDs configuration
- Python environment with required dependencies

### Configuration
Voice IDs are managed through a YAML configuration file:

### API Integration
- Uses ElevenLabs Python client
- Handles streaming audio response
- Supports MP3 output format

### Error Handling
- Validates input text
- Handles API connection issues
- Provides detailed error messages
- Maintains segment information on failure

### Testing
The tool includes a test interface that:
- Validates API connectivity
- Tests voice generation
- Verifies file output
- Handles error cases

## Best Practices
1. Keep text segments under 4000 characters
2. Include proper punctuation
3. Use consistent voice roles
4. Handle API responses properly
5. Maintain secure API key storage

## Limitations
- Requires active internet connection
- API rate limits apply
- Voice ID configuration required
- Text length restrictions

## Example Usage

## Integration Notes
- Tool inherits from CrewAI's BaseTool
- Uses Pydantic models for request validation
- Supports CrewAI's tool execution patterns
- Designed for podcast segment generation workflow

## Best Practices
1. Store API keys in environment variables
2. Use voice config file for ID management
3. Implement proper error handling
4. Clean up test files after generation
5. Validate inputs before API calls

## Limitations
- Requires valid ElevenLabs API key
- Voice IDs must be configured before use
- Test files are temporary by default
- Limited to configured voice roles

## Response Formats

### Success Response
```python
{
    "status": "success",
    "file_path": "path/to/file.mp3",
    "message": "Audio file saved to path/to/file.mp3",
    "voice_id": "voice_id_used"
}
```

### Error Response
```python
{
    "status": "error",
    "message": "Error description"
}
```