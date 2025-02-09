"""
Gista App Agent System
=====================

A specialized system for converting text content into podcast episodes.

Department Structure & Task Flow
------------------------------
```
Content Assessment → Script Production → Voice Generation
     [Validate]          [Write]            [Speak]
```

Agent-Task Mapping
-----------------
```
1. Content Assessment Department
┌─────────────────────┬──────────────────────────────┐
│ Agent              │ Tasks                        │
├─────────────────────┼──────────────────────────────┤
│ Content Validator  │ • prepare_content            │
│                   │ • approve_content            │
│                   │ • reject_content             │
│                   │ • start_production_pipeline  │
├─────────────────────┼──────────────────────────────┤
│ Content Analyst    │ • content_analysis          │
│                   │ • content_presentation       │
├─────────────────────┼──────────────────────────────┤
│ Technical Analyst  │ • terminology_analysis      │
├─────────────────────┼──────────────────────────────┤
│ Research Specialist│ • background_research       │
└─────────────────────┴──────────────────────────────┘

2. Script Production Department
┌─────────────────────┬──────────────────────────────┐
│ Agent              │ Tasks                        │
├─────────────────────┼──────────────────────────────┤
│ Transition Writer  │ • opening_transition         │
│                   │ • expert_introduction        │
│                   │ • closing_transition         │
├─────────────────────┼──────────────────────────────┤
│ Readout Writer     │ • readout_script            │
├─────────────────────┼──────────────────────────────┤
│ Script Alpha       │ • segments 1-3              │
│ Script Beta        │ • segments 4-6              │
│ Script Gamma       │ • segments 7-9              │
│ Script Omega       │ • segment 10                │
├─────────────────────┼──────────────────────────────┤
│ Transcript Gen     │ • generate_transcript       │
└─────────────────────┴──────────────────────────────┘

3. Voice Generation Department
┌─────────────────────┬──────────────────────────────┐
│ Agent              │ Tasks                        │
├─────────────────────┼──────────────────────────────┤
│ Voice Alpha        │ • parse_script               │
│                   │ • segments 1-3               │
├─────────────────────┼──────────────────────────────┤
│ Voice Beta         │ • segments 4-6              │
├─────────────────────┼──────────────────────────────┤
│ Voice Gamma        │ • segments 7-9              │
├─────────────────────┼──────────────────────────────┤
│ Voice Omega        │ • segment 10                │
└─────────────────────┴──────────────────────────────┘
```

Tool Integration
---------------
```
Content Assessment ──► Research Tools
                     • Web Scraper
                     • PDF/DOCX/CSV Readers
                     • Enhanced Search
                     • Wikipedia Research
                     • Dictionary

Script Production ──► Analysis Output
                     • Content Maps
                     • Technical Terms
                     • Research Data

Voice Generation ──► Voice Tools
                    • Script Parser
                    • ElevenLabs Voice
                    • Transcription
```

Process Flow
-----------
```
[Content] ──► [Validation] ──► [Research] ──► [Analysis]
                                                │
                                                ▼
[Voice] ◄── [Generation] ◄── [Scripts] ◄── [Presentation]
```

Notes:
- Each department operates sequentially but allows parallel processing within
- Content assessment provides foundation for script production
- Voice generation depends on completed scripts
- Tools are department-specific
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

    # Script Production Department
    transition_writer = Agent(
        role="Transition Writer",
        goal="Create smooth transitions between podcast segments",
        backstory=(
            "Expert in crafting natural transitions and segment connections. "
            "Specializes in opening, closing, and inter-segment transitions "
            "that maintain narrative flow and listener engagement."
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
            "transition_writer": transition_writer,
            "qa_script_writer": segment_script_beta
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
