"""
Gista App Agent System
=====================

A multi-department system for converting text content into podcast episodes.

Department Structure and Responsibilities
---------------------------------------

1. Content Assessment Department
   - Initial document evaluation and content analysis
   - Technical term identification and research
   - Key points extraction and structuring
   Agents: Doc Assessor → Keyword Analyst → Research Specialist → Analysis Presenter

2. Script Production Department
   - Verbatim readout script creation
   - Q&A segment script development
   - Transition writing and flow management
   Agents: Readout Writer → Q&A Writer → Transition Writer

3. Audio Production Department
   - Parallel segment production
   - Audio mixing and mastering
   - Sound design and enhancement
   Agents: Readout Producer || (QA Producers α,β,γ) → Audio Mixer + Sound Designer

4. Quality Assurance Department
   - Content accuracy verification
   - Audio quality control
   - Fact-checking and consistency
   Agents: Content QA + Fact Checker || Audio QA

5. Project Management Department
   - Workflow coordination
   - Resource optimization
   - Quality oversight
   Agents: Workflow Coordinator ↔ Resource Manager ↔ Quality Manager

Workflow and Handoff Process
---------------------------

                                    Content Assessment
                                    ┌─────────────────┐
                                    │ Doc Assessment  │
                                    │ Keyword Analysis│
                                    │ Research        │
                                    │ Analysis Points │
                                    └────────┬────────┘
                                            │
                                            ▼
                                   Script Production
                                    ┌─────────────────┐
                                    │ Readout Script  │
                                    │ Q&A Scripts     │
                                    │ Transitions     │
                                    └────────┬────────┘
                                            │
                                            ▼
                                   Audio Production
                                    ┌─────────────────┐
                    ┌───────────────┤ Parallel Process│
                    │               │ Mix & Master    │
                    │               │ Sound Design    │
                    │               └────────┬────────┘
                    │                        │
                    ▼                        ▼
            Quality Assurance        Quality Assurance
            ┌─────────────┐         ┌─────────────┐
            │Content & Fact│         │Audio Quality│
            └──────┬──────┘         └──────┬──────┘
                   │                       │
                   └──────────┬───────────┘
                             │
                             ▼
                    Final QA & Delivery
                    ┌─────────────────┐
                    │Quality Manager  │
                    │Final Approval   │
                    └─────────────────┘

Process Flow
-----------
1. Content Assessment:
   - Doc Assessor evaluates content suitability
   - Keyword Analyst identifies technical terms
   - Research Specialist provides context
   - Analysis Presenter creates Q&A framework

2. Script Production:
   - Readout Script Writer creates verbatim script
   - Q&A Script Writer develops discussion segments
   - Transition Writer ensures smooth flow

3. Audio Production (Parallel Processing):
   - Readout Producer creates main content
   - Q&A Producers (α,β,γ) work on segments 1-3, 4-6, 7-10
   - Audio Mixer combines segments
   - Sound Designer adds enhancements

4. Quality Assurance (Parallel Processing):
   - Content QA and Fact Checker verify accuracy
   - Audio QA ensures sound quality
   - All feed back to Quality Manager

5. Project Management (Continuous):
   - Workflow Coordinator oversees process
   - Resource Manager optimizes parallel processing
   - Quality Manager ensures standards

Legend
------
→  : Sequential flow
||  : Parallel processing
↔  : Bi-directional communication
+   : Collaborative work
"""

from crewai import Agent

def create_gista_agents():
    """
    Create and return the Gista App agents organized by department
    """
    
    # Content Assessment Department
    doc_assessor = Agent(
        role="Document Assessor",
        goal="Initial document evaluation and qualification",
        backstory=(
            "Expert in evaluating content suitability for podcast conversion. "
            "You assess document type, length, and content quality."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    keyword_analyst = Agent(
        role="Keyword & Terminology Analyst",
        goal="Identify and explain technical terms and key concepts",
        backstory=(
            "Specialist in identifying technical terminology, industry jargon, "
            "and complex concepts requiring additional explanation."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    research_specialist = Agent(
        role="Research Specialist",
        goal="Provide additional context and background research",
        backstory=(
            "Expert researcher who provides additional context, verifies facts, "
            "and ensures comprehensive understanding of the topic."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    analysis_presenter = Agent(
        role="Analysis Presenter",
        goal="Create structured analysis and Q&A framework",
        backstory=(
            "Content analysis expert who identifies key points and creates "
            "the Q&A discussion framework. Works with research and keyword teams."
        ),
        allow_delegation=True,
        verbose=True
    )

    # Script Production Department
    readout_script_writer = Agent(
        role="Readout Script Writer",
        goal="Create verbatim readout scripts with proper attribution",
        backstory=(
            "Specialized in creating clear, well-structured scripts for the "
            "verbatim readout portion, including proper source attribution."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    qa_script_writer = Agent(
        role="Q&A Script Writer",
        goal="Create engaging Q&A segment scripts",
        backstory=(
            "Expert in converting analysis points into natural, flowing "
            "Q&A exchanges between host and expert."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    transition_writer = Agent(
        role="Transition Writer",
        goal="Create smooth transitions between segments",
        backstory=(
            "Specialist in writing natural transitions between different "
            "segments of the podcast, ensuring smooth flow."
        ),
        allow_delegation=False,
        verbose=True
    )

    # Audio Production Department
    readout_producer = Agent(
        role="Readout Segment Producer",
        goal="Produce high-quality readout audio segments",
        backstory=(
            "Audio specialist focused on producing clear, professional "
            "recordings of the verbatim content."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    qa_producer_alpha = Agent(
        role="Q&A Producer Alpha",
        goal="Produce Q&A segments 1-3",
        backstory=(
            "Audio producer specializing in Q&A segments, handling the "
            "first three segments of each episode."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    qa_producer_beta = Agent(
        role="Q&A Producer Beta",
        goal="Produce Q&A segments 4-6",
        backstory=(
            "Audio producer specializing in Q&A segments, handling the "
            "middle three segments of each episode."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    qa_producer_gamma = Agent(
        role="Q&A Producer Gamma",
        goal="Produce Q&A segments 7-10",
        backstory=(
            "Audio producer specializing in Q&A segments, handling the "
            "final four segments of each episode."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    audio_mixer = Agent(
        role="Audio Mixing Specialist",
        goal="Mix and master all audio segments",
        backstory=(
            "Expert in audio mixing and mastering, ensuring consistent "
            "quality across all segments and smooth transitions."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    sound_designer = Agent(
        role="Sound Designer",
        goal="Create and implement sound effects and transitions",
        backstory=(
            "Specialist in creating audio transitions, background music, "
            "and sound effects to enhance the podcast experience."
        ),
        allow_delegation=False,
        verbose=True
    )

    # Quality Assurance Department
    content_qa = Agent(
        role="Content Quality Specialist",
        goal="Verify content accuracy and quality",
        backstory=(
            "Expert in verifying content accuracy, fact-checking, and "
            "ensuring educational value of the material."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    audio_qa = Agent(
        role="Audio Quality Specialist",
        goal="Verify audio quality and consistency",
        backstory=(
            "Specialist in audio quality control, ensuring consistent "
            "sound quality across all segments."
        ),
        allow_delegation=False,
        verbose=True
    )
    
    fact_checker = Agent(
        role="Fact Checking Specialist",
        goal="Verify factual accuracy of content",
        backstory=(
            "Dedicated fact-checker who verifies all claims, statistics, "
            "and references in both readout and analysis segments."
        ),
        allow_delegation=False,
        verbose=True
    )

    # Project Management Department
    workflow_coordinator = Agent(
        role="Workflow Coordinator",
        goal="Manage overall workflow and task distribution",
        backstory=(
            "Project manager coordinating all departments and ensuring "
            "smooth workflow progression."
        ),
        allow_delegation=True,
        verbose=True
    )
    
    resource_manager = Agent(
        role="Resource Manager",
        goal="Optimize resource allocation and parallel processing",
        backstory=(
            "Specialist in optimizing resource allocation and managing "
            "parallel processing of segments."
        ),
        allow_delegation=True,
        verbose=True
    )
    
    quality_manager = Agent(
        role="Quality Manager",
        goal="Oversee all quality control processes",
        backstory=(
            "Senior manager overseeing all quality control processes "
            "across content and audio production."
        ),
        allow_delegation=True,
        verbose=True
    )

    return {
        "content_assessment": {
            "doc_assessor": doc_assessor,
            "keyword_analyst": keyword_analyst,
            "research_specialist": research_specialist,
            "analysis_presenter": analysis_presenter
        },
        "script_production": {
            "readout_script_writer": readout_script_writer,
            "qa_script_writer": qa_script_writer,
            "transition_writer": transition_writer
        },
        "audio_production": {
            "readout_producer": readout_producer,
            "qa_producer_alpha": qa_producer_alpha,
            "qa_producer_beta": qa_producer_beta,
            "qa_producer_gamma": qa_producer_gamma,
            "audio_mixer": audio_mixer,
            "sound_designer": sound_designer
        },
        "quality_assurance": {
            "content_qa": content_qa,
            "audio_qa": audio_qa,
            "fact_checker": fact_checker
        },
        "project_management": {
            "workflow_coordinator": workflow_coordinator,
            "resource_manager": resource_manager,
            "quality_manager": quality_manager
        }
    }
