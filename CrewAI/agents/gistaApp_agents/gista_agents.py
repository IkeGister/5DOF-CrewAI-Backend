"""
Gista App Agent System
=====================

A specialized system for converting text content into podcast episodes, organized into three main departments.

Department Structure and Agent Responsibilities
--------------------------------------------

1. Content Assessment Department
------------------------------
Primary Tools: Web Scraper, PDF Reader, DOCX Reader, CSV Reader, Directory Reader, 
              Enhanced Web Search, Wikipedia Research, Dictionary Tool

Agents:
- Content Validator
  * Handles initial content preparation and validation
  * Makes approval/rejection decisions
  * Initiates production pipeline
  * Uses content extraction tools for various file types

- Content Analyst
  * Analyzes content structure and relationships
  * Creates content maps and presentation frameworks
  * Prepares content for script production
  * Uses research tools for content analysis

- Technical Analyst
  * Specializes in technical terminology analysis
  * Researches and explains complex concepts
  * Creates technical glossaries
  * Uses dictionary and research tools

- Research Specialist
  * Conducts deep background research
  * Verifies claims and sources
  * Provides contextual information
  * Uses enhanced web search and research tools

2. Script Production Department
-----------------------------
Primary Tools: None currently assigned, uses analysis output

Agents:
- Readout Script Writer
  * Creates main content readout scripts
  * Structures core narrative
  * Sets emphasis points
  * Handles technical term presentation

- Segment Script Writers (Alpha, Beta, Gamma, Omega)
  * Alpha: Segments 1-3 (Opening, Introduction)
  * Beta: Segments 4-6 (Core Content)
  * Gamma: Segments 7-9 (Detailed Discussion)
  * Omega: Segment 10 (Conclusion)
  * Each maintains consistent narrative flow
  * Handles transitions between segments

- Transcript Generator
  * Creates accurate transcripts
  * Handles speaker attribution
  * Maintains proper formatting
  * Works with voice generation output

3. Voice Generation Department
----------------------------
Primary Tools: Script Parser Tool, ElevenLabs Voiceover Tool, Transcription Tool

Agents:
- Voice Generators (Alpha, Beta, Gamma, Omega)
  * Alpha: Segments 1-3
  * Beta: Segments 4-6
  * Gamma: Segments 7-9
  * Omega: Segment 10
  * Each maintains consistent voice quality
  * Handles emphasis and pacing
  * Uses ElevenLabs for voice synthesis

Process Flow and Dependencies
---------------------------
1. Content Assessment Flow:
   Content Validator → Content/Technical Analysis → Research → Presentation

2. Script Production Flow:
   Readout Script → Segment Scripts (parallel) → Transcript

3. Voice Generation Flow:
   Script Parsing → Voice Generation (parallel) → Transcript Generation

Task-Agent Mapping Matrix
------------------------
[C: Content Tasks    S: Script Tasks    V: Voice Tasks]

Agents                Tasks
----------------------------------------
Content Validator     C1 C2 C3 C4
Content Analyst      C5 C6
Technical Analyst    C7 C8
Research Spec.       C9 C10

Readout Writer       S1
Script Alpha         S2(1-3)
Script Beta          S2(4-6)
Script Gamma         S2(7-9)
Script Omega         S2(10)
Transcript Gen.      S3

Voice Alpha          V1(1-3)
Voice Beta          V1(4-6)
Voice Gamma         V1(7-9)
Voice Omega         V1(10)

Parallel Processing Groups
-------------------------
[Segments 1-3]  Script Alpha → Voice Alpha
[Segments 4-6]  Script Beta  → Voice Beta
[Segments 7-9]  Script Gamma → Voice Gamma
[Segment 10]    Script Omega → Voice Omega

Tool Integration
---------------
1. Content Assessment Tools:
   - Web Scraper Tool: Content extraction from web pages
   - PDF/DOCX/CSV Readers: Document content extraction
   - Enhanced Web Search: Research and verification
   - Wikipedia Research: Background information
   - Dictionary Tool: Term definitions and analysis

2. Voice Generation Tools:
   - Script Parser Tool: Converts scripts to voice segments
   - ElevenLabs Voiceover: Voice synthesis
   - Transcription Tool: Creates final transcripts

Notes:
- Each department has specific tool assignments
- Content assessment heavily utilizes research tools
- Voice generation has complete tool coverage
- Script production focuses on content structuring
"""

from crewai import Agent

def create_gista_agents():
    """Create and return the Gista App agents organized by department"""
    
    # Content Assessment Department
    content_validator = Agent(
        role="Content Validator",
        goal="Validate and approve content for processing",
        backstory=(
            "Expert in content evaluation and validation. Handles initial content "
            "preparation, approval decisions, and production pipeline initiation."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    content_analyst = Agent(
        role="Content Analyst",
        goal="Analyze and structure content for processing",
        backstory=(
            "Specialist in content analysis and framework development. "
            "Creates content maps and presentation structures."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    technical_analyst = Agent(
        role="Technical Analyst",
        goal="Handle technical analysis and terminology",
        backstory=(
            "Expert in technical terminology and concept analysis. "
            "Manages terminology research and technical explanations."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    research_specialist = Agent(
        role="Research Specialist",
        goal="Conduct background research and verification",
        backstory=(
            "Dedicated researcher handling background research, "
            "fact verification, and context development."
        ),
        allow_delegation=False,
        verbose=True
    )

    # Script & Voice Department
    readout_script_writer = Agent(
        role="Readout Script Writer",
        goal="Create main readout script content",
        backstory=(
            "Expert in creating clear, well-structured scripts for the main "
            "content readout. Ensures proper flow and emphasis in the core narrative."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    segment_script_alpha = Agent(
        role="Script Writer Alpha",
        goal="Create script content for segments 1-3",
        backstory=(
            "Specialized script writer for opening segments. Expert in crafting "
            "engaging introductions and early content development segments."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    segment_script_beta = Agent(
        role="Script Writer Beta",
        goal="Create script content for segments 4-6",
        backstory=(
            "Specialized script writer for middle segments. Expert in developing "
            "core discussion points and maintaining narrative momentum."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    segment_script_gamma = Agent(
        role="Script Writer Gamma",
        goal="Create script content for segments 7-9",
        backstory=(
            "Specialized script writer for later segments. Expert in crafting "
            "detailed discussion segments and complex topic exploration."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    segment_script_omega = Agent(
        role="Script Writer Omega",
        goal="Create script content for segment 10",
        backstory=(
            "Specialized script writer for the final segment. Expert in creating "
            "strong conclusions and summary content that ties everything together."
        ),
        allow_delegation=False,
        verbose=True
    )

    # Voice Generation Department
    segment_voice_alpha = Agent(
        role="Voice Generator Alpha",
        goal="Generate voice content for segments 1-3",
        backstory=(
            "Specialized voice synthesis agent handling the first three segments. "
            "Expert in maintaining consistent voice quality and pacing for "
            "opening segments of content."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    segment_voice_beta = Agent(
        role="Voice Generator Beta",
        goal="Generate voice content for segments 4-6",
        backstory=(
            "Specialized voice synthesis agent handling the middle three segments. "
            "Expert in maintaining narrative flow and voice consistency across "
            "core content segments."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    segment_voice_gamma = Agent(
        role="Voice Generator Gamma",
        goal="Generate voice content for segments 7-9",
        backstory=(
            "Specialized voice synthesis agent handling segments seven through nine. "
            "Expert in maintaining engagement and voice quality for "
            "detailed discussion segments."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    segment_voice_omega = Agent(
        role="Voice Generator Omega",
        goal="Generate voice content for segment 10",
        backstory=(
            "Specialized voice synthesis agent handling the final segment. "
            "Expert in conclusion and summary voice generation, ensuring "
            "strong closing delivery."
        ),
        allow_delegation=False,
        verbose=True
    )

    # Add this with the Script & Voice Department agents
    transcript_generator = Agent(
        role="Transcript Generator",
        goal="Generate accurate transcripts",
        backstory=(
            "Expert in transcript generation and formatting. Creates accurate "
            "transcripts with proper speaker attribution and formatting."
        ),
        allow_delegation=False,
        verbose=True
    )

    agents_dict = {
        "content_assessment": {
            "doc_assessor": content_validator,
            "content_validator": content_validator,
            "content_analyst": content_analyst,
            "technical_analyst": technical_analyst,
            "research_specialist": research_specialist,
            "keyword_analyst": content_analyst,
            "analysis_presenter": content_analyst
        },
        "script_production": {
            "readout_script_writer": readout_script_writer,
            "segment_script_alpha": segment_script_alpha,
            "segment_script_beta": segment_script_beta,
            "segment_script_gamma": segment_script_gamma,
            "segment_script_omega": segment_script_omega,
            "transcript_generator": transcript_generator,
            "qa_script_writer": segment_script_beta,
            "transition_writer": segment_script_gamma
        },
        "voice_generation": {
            "segment_voice_alpha": segment_voice_alpha,
            "segment_voice_beta": segment_voice_beta,
            "segment_voice_gamma": segment_voice_gamma,
            "segment_voice_omega": segment_voice_omega,
            "parser": segment_voice_alpha,
            "generator": segment_voice_beta,
            "transcriber": segment_voice_omega
        }
    }
    print("DEBUG: gista_agents keys:", list(agents_dict.keys()))
    return agents_dict
