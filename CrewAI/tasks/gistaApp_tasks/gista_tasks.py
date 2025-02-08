"""
Gista App Tasks Module - Workflow Sequence
========================================

1. Content Validation & Assessment
   - prepare_content (content extraction)
   - approve_content/reject_content (user feedback)

2. Content Research & Analysis
   - start_production_pipeline (research preparation)
   - content_analysis (structure & concepts)
   - terminology_analysis (technical terms)
   - background_research (verification)
   - content_presentation (synthesis)
   Tools used:
   - Enhanced web search (SerperDev)
   - Wikipedia research
   - Dictionary lookups

3. Script Production
   - readout_script
   - qa_script
   - transitions

4. Voice Generation
   - parse_script
   - generate_audio
   - generate_transcript
"""

from crewai import Task
from tools.gista_tools.gista_general_tools import GistaToolbox
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# First, let's define our output models
class ContentAnalysisOutput(BaseModel):
    content_map: Dict
    relationship_map: Dict
    analysis_metrics: Dict

class TerminologyAnalysisOutput(BaseModel):
    technical_glossary: List[Dict]
    concept_groups: List[Dict]
    explanation_strategy: Dict

class ContentValidationOutput(BaseModel):
    status: str
    content_status: str
    metadata: Dict
    content_validation: Dict
    content_complexity: Dict
    extracted_content: Dict
    processing_info: Dict

class TaskOutput(BaseModel):
    status: str
    qa_validation: Optional[Dict]
    content_analysis: Optional[Dict]
    script_generation: Optional[Dict]

# Add new output models
class ScriptOutput(BaseModel):
    """Structured output for podcast script segments"""
    segment_type: str  # 'opening', 'readout', 'expert_intro', 'qa', 'closing'
    script_content: Dict[str, str]  # Keyed by speaker role ('host', 'expert')
    transitions: Dict[str, str]  # Entry/exit transitions for this segment
    technical_terms: List[Dict[str, str]]  # Terms with pronunciations
    segment_metadata: Dict[str, Any] = {
        'duration_estimate': float,
        'voice_roles': List[str],
        'emphasis_points': List[Dict],
        'pause_markers': List[Dict],
        'segment_index': Optional[int]  # For Q&A segments
    }
    references: Optional[List[Dict]] = None  # Citations and sources
    qa_context: Optional[Dict] = None  # For Q&A segments only

class AudioOutput(BaseModel):
    audio_files: List[str]
    segment_info: List[Dict]
    technical_details: Dict
    quality_metrics: Dict

# 1. Content Assessment Tasks
def create_user_content_validation_tasks(agents):
    """Initial content validation and user response tasks"""
    
    gista_tools = GistaToolbox()
    
    prepare_content = Task(
        description=(
            "Extract raw content from the provided source and perform basic content validation:\n"
            "1. Access the provided URL/file\n"
            "2. Extract text content based on source type:\n"
                "- Web pages (using web_scraper)\n"
                "- PDF documents (using pdf_reader)\n"
                "- Word documents (using docx_reader)\n"
                "- CSV files (using csv_reader)\n"
                "- Local directories (using directory_reader)\n"
            "3. Structure the output data\n"
            "4. Set content_status based on validation rules\n"
            "5. Calculate timing estimates"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "- Status and content_status\n"
            "- Complete metadata\n"
            "- Content validation flags\n"
            "- Content complexity metrics\n"
            "- Extracted content sections\n"
            "- Processing information"
        ),
        agent=agents["doc_assessor"],
        tools=[
            gista_tools.web_scraper,   # Content extraction tools
            gista_tools.pdf_reader,
            gista_tools.docx_reader,
            gista_tools.csv_reader,
            gista_tools.directory_reader
        ],
        output_pydantic=ContentValidationOutput,
        callback=task_completed_callback
    )
    
    approve_content = Task(
        description=(
            "Process CLEARED or NEEDS_REVIEW content for quick approval response:\n"
            "1. Verify content_status from prepare_content output\n"
            "2. Generate appropriate approval message\n"
            "3. Prepare user notification with initial timeline estimate\n"
            "4. Set workflow type (standard/special_review)"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "- Status (approved)\n"
            "- Workflow type\n"
            "- Content information\n"
            "- Approval details\n"
            "- UI messages"
        ),
        agent=agents["doc_assessor"],
        tools=[],  # TODO: Implement notification and messaging tools
        context=[prepare_content],
        output_pydantic=ContentValidationOutput,
        callback=task_completed_callback
    )
    
    reject_content = Task(
        description=(
            "Process REJECTED content and prepare rejection response:\n"
            "1. Extract rejection reason from prepare_content output\n"
            "2. Generate appropriate rejection message based on content_validation flags:\n"
                "- Image-only content\n"
                "- Audio/video content\n"
                "- Insufficient text content\n"
            "3. Include alternative suggestions if applicable\n"
            "4. Prepare response for user interface"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "- Status (rejected)\n"
            "- Original content information\n"
            "- Rejection details\n"
            "- UI messages"
        ),
        agent=agents["doc_assessor"],
        tools=[],  # TODO: Implement notification and messaging tools
        context=[prepare_content],
        output_pydantic=ContentValidationOutput,
        callback=task_completed_callback
    )
    
    return [prepare_content, approve_content, reject_content]

def create_user_content_research_tasks(agents, validation_tasks):
    """Research preparation and initial analysis tasks"""
    
    gista_tools = GistaToolbox()
    prepare_content = validation_tasks[0]
    approve_content = validation_tasks[1]
    
    start_production_pipeline = Task(
        description=(
            "Initialize content analysis pipeline for approved content:\n"
            "1. Structure content for analysis:\n"
                "a) Organize raw content for content_analysis\n"
                "b) Flag technical terms for terminology_analysis\n"
                "c) Mark claims for background_research\n"
            "2. For special review content:\n"
                "a) Flag special handling requirements:\n"
                    "- Code block treatment\n"
                    "- Content splitting requirements\n"
                "b) Adjust analysis parameters"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "- Original content with metadata\n"
            "- Analysis preparation data:\n"
                "* Content sections for analysis\n"
                "* Preliminary technical terms\n"
                "* Potential quotes\n"
            "- Terminology flags\n"
            "- Research targets\n"
            "- Special handling requirements"
        ),
        agent=agents["doc_assessor"],
        tools=[
            gista_tools.web_search,   # Enhanced search for initial research
            gista_tools.wikipedia,    # For general knowledge
            gista_tools.dictionary    # For term understanding
        ],
        context=[prepare_content, approve_content],
        output_pydantic=ContentValidationOutput,
        callback=task_completed_callback
    )

    content_analysis = Task(
        description=(
            "Analyze and structure content for technical assessment:\n"
            "1. Analyze content structure\n"
            "2. Map key concepts\n"
            "3. Identify relationships\n"
            "4. Create technical framework"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "- Content map with key concepts\n"
            "- Relationship diagrams\n"
            "- Technical term identification\n"
            "- Complexity metrics"
        ),
        agent=agents["keyword_analyst"],
        tools=[
            gista_tools.web_search,   # Enhanced search for content research
            gista_tools.wikipedia,    # For concept understanding
            gista_tools.dictionary    # For term definitions
        ],
        context=[start_production_pipeline],
        output_pydantic=ContentAnalysisOutput
    )
    
    terminology_analysis = Task(
        description=(
            "Analyze and expand technical elements from content analysis:\n"
            "1. Identify technical terms\n"
            "2. Research definitions\n"
            "3. Create explanation framework\n"
            "4. Map term relationships"
        ),
        expected_output=(
            "Technical analysis document containing:\n"
            "- Comprehensive term glossary\n"
            "- Term relationships\n"
            "- Explanation frameworks\n"
            "- Complexity levels"
        ),
        agent=agents["keyword_analyst"],
        tools=[
            gista_tools.web_search,   # Enhanced search for term research
            gista_tools.dictionary,   # For term definitions
            gista_tools.wikipedia    # For term context
        ],
        context=[content_analysis],
        output_pydantic=TerminologyAnalysisOutput
    )

    background_research = Task(
        description=(
            "Research and validate content from content analysis:\n"
            "1. Conduct deep research on identified topics\n"
            "2. Verify all technical claims and statements\n"
            "3. Provide comprehensive context\n"
            "4. Document all sources and references"
        ),
        expected_output=(
            "Research document containing:\n"
            "- Verified claims with sources\n"
            "- Technical validations\n"
            "- Contextual information\n"
            "- Complete reference list"
        ),
        agent=agents["research_specialist"],
        tools=[
            gista_tools.web_search,   # Enhanced search for deep research
            gista_tools.wikipedia,    # For background information
            gista_tools.dictionary    # For term verification
        ],
        context=[content_analysis],
        output_pydantic=ContentValidationOutput
    )

    content_presentation = Task(
        description=(
            "Synthesize analyzed content into a structured markdown document for script production:\n"
            "1. Integrate data from multiple sources:\n"
                "a) content_analysis output\n"
                "b) terminology_analysis output\n"
                "c) background_research output\n"
            "2. Structure content for podcast format\n"
            "3. Add markdown emphasis markers\n"
            "4. Include technical explanations"
        ),
        expected_output=(
            "A complete markdown document containing:\n"
            "- Structured content sections\n"
            "- Technical term definitions\n"
            "- Research citations\n"
            "- Production notes\n"
            "- Emphasis markers"
        ),
        agent=agents["analysis_presenter"],
        tools=[
            gista_tools.web_search,   # Enhanced search for final verification
            gista_tools.dictionary,   # For final term verification
            gista_tools.wikipedia     # For final fact checking
        ],
        context=[content_analysis, terminology_analysis, background_research],
        output_pydantic=ContentValidationOutput
    )
    
    return [
        start_production_pipeline,
        content_analysis,
        terminology_analysis,
        background_research,
        content_presentation
    ]

# 3. Script Production Tasks
def create_script_production_tasks(agents):
    """Convert analyzed content into podcast scripts with proper transitions"""
    
    opening_transition = Task(
        description=(
            "Create show opening transition:\n"
            "1. Write Gista's self-introduction\n"
            "2. Present content overview from research\n"
            "3. Signal upcoming content readout\n"
            "4. Set professional yet approachable tone"
        ),
        expected_output=(
            "Opening script containing:\n"
            "- Host introduction as Gista\n"
            "- Content summary\n"
            "- Readout preparation\n"
            "- Transition markers"
        ),
        agent=agents["script_production"]["transition_writer"],
        tools=[],
        output_pydantic=ScriptOutput
    )

    readout_script = Task(
        description=(
            "Create verbatim readout script:\n"
            "1. Convert document content to spoken format\n"
            "2. Add proper attribution and citations\n"
            "3. Mark emphasis points and pauses\n"
            "4. Include pronunciation guides"
        ),
        expected_output=(
            "A complete readout script including:\n"
            "- Formatted spoken content\n"
            "- Citations and attributions\n"
            "- Emphasis markers\n"
            "- Pronunciation guides"
        ),
        agent=agents["script_production"]["readout_script_writer"],
        tools=[],
        context=[opening_transition],
        output_pydantic=ScriptOutput
    )

    expert_introduction = Task(
        description=(
            "Create expert introduction and analysis setup:\n"
            "1. Write post-readout host transition\n"
            "2. Create expert welcome and introduction\n"
            "3. Write expert's analysis overview\n"
            "4. Set up Q&A format"
        ),
        expected_output=(
            "Expert introduction script containing:\n"
            "- Host's expert introduction\n"
            "- Expert's response and overview\n"
            "- Analysis preview\n"
            "- Q&A format setup"
        ),
        agent=agents["script_production"]["transition_writer"],
        tools=[],
        context=[readout_script],
        output_pydantic=ScriptOutput
    )

    qa_script = Task(
        description=(
            "Develop Q&A segment scripts with transitions:\n"
            "1. Create sequential Q&A pairs (1-10)\n"
            "2. Write transition between each Q&A\n"
            "3. Ensure natural conversation flow\n"
            "4. Maintain technical accuracy\n"
            "Each Q&A should follow pattern:\n"
            "- Transition to question\n"
            "- Host question\n"
            "- Expert response\n"
            "- Bridge to next question"
        ),
        expected_output=(
            "Q&A script package containing:\n"
            "- 10 Q&A segments with transitions\n"
            "- Host questions\n"
            "- Expert responses\n"
            "- Inter-segment transitions"
        ),
        agent=agents["script_production"]["qa_script_writer"],
        tools=[],
        context=[expert_introduction],
        output_pydantic=ScriptOutput
    )

    closing_transition = Task(
        description=(
            "Create show closing:\n"
            "1. Write host's expert acknowledgment\n"
            "2. Summarize key discussion points\n"
            "3. Create Gista's sign-off\n"
            "4. Add final transition markers"
        ),
        expected_output=(
            "Closing script containing:\n"
            "- Expert acknowledgment\n"
            "- Key points summary\n"
            "- Host sign-off\n"
            "- Final transition markers"
        ),
        agent=agents["script_production"]["transition_writer"],
        tools=[],
        context=[qa_script],
        output_pydantic=ScriptOutput
    )

    return [
        opening_transition,
        readout_script,
        expert_introduction,
        qa_script,
        closing_transition
    ]

# 4. Voice Generation Tasks
def create_voice_generation_tasks(agents):
    """Generate voice content from scripts"""
    
    gista_tools = GistaToolbox()
    
    parse_script = Task(
        description=(
            "Convert podcast script into parallel-processable segments:\n"
            "1. Extract metadata (title, source, etc.)\n"
            "2. Break down script into indexed segments:\n"
                "a) readout_segments: Complete readout content\n"
                "b) qa_segments_1_3: First Q&A section\n"
                "c) qa_segments_4_6: Middle Q&A section\n"
                "d) qa_segments_7_10: Final Q&A section\n"
            "3. For each segment:\n"
                "- Identify voice roles\n"
                "- Mark pauses and emphasis\n"
                "- Include technical term guides\n"
            "4. Package segments for parallel processing"
        ),
        expected_output=(
            "JSON formatted segment bundles:\n"
            "- readout_bundle: {segments, metadata, voice_role}\n"
            "- qa_early_bundle: {segments[1:3], metadata, voice_roles}\n"
            "- qa_middle_bundle: {segments[4:6], metadata, voice_roles}\n"
            "- qa_late_bundle: {segments[7:10], metadata, voice_roles}"
        ),
        agent=agents["parser"],
        tools=[gista_tools.script_parser],
        output_pydantic=ContentValidationOutput
    )
    
    readout_production = Task(
        description=(
            "Generate readout audio from readout_bundle:\n"
            "1. Process assigned readout segments\n"
            "2. Apply segment-specific voice settings\n"
            "3. Handle emphasis and pauses\n"
            "4. Output segment-indexed audio files"
        ),
        expected_output="Audio files for readout segments",
        agent=agents["voice_generation"]["readout_producer"],
        tools=[gista_tools.voiceover],
        context=[
            {
                "depends_on": parse_script,
                "segment_bundle": "readout_bundle"
            }
        ],
        output_pydantic=ContentValidationOutput
    )

    qa_production_early = Task(
        description=(
            "Generate Q&A segments 1-3 from qa_early_bundle:\n"
            "1. Process assigned Q&A segments (1-3)\n"
            "2. Apply role-specific voice settings\n"
            "3. Handle technical terminology\n"
            "4. Output indexed audio files"
        ),
        expected_output="Audio files for Q&A segments 1-3",
        agent=agents["voice_generation"]["qa_producer_alpha"],
        tools=[gista_tools.voiceover],
        context=[
            {
                "depends_on": parse_script,
                "segment_bundle": "qa_early_bundle"
            }
        ],
        output_pydantic=ContentValidationOutput
    )

    qa_production_middle = Task(
        description=(
            "Generate Q&A segments 4-6 from qa_middle_bundle:\n"
            "1. Process assigned Q&A segments (4-6)\n"
            "2. Apply role-specific voice settings\n"
            "3. Handle technical terminology\n"
            "4. Output indexed audio files"
        ),
        expected_output="Audio files for Q&A segments 4-6",
        agent=agents["voice_generation"]["qa_producer_beta"],
        tools=[gista_tools.voiceover],
        context=[
            {
                "depends_on": parse_script,
                "segment_bundle": "qa_middle_bundle"
            }
        ],
        output_pydantic=ContentValidationOutput
    )

    qa_production_late = Task(
        description=(
            "Generate Q&A segments 7-10 from qa_late_bundle:\n"
            "1. Process assigned Q&A segments (7-10)\n"
            "2. Apply role-specific voice settings\n"
            "3. Handle technical terminology\n"
            "4. Output indexed audio files"
        ),
        expected_output="Audio files for Q&A segments 7-10",
        agent=agents["voice_generation"]["qa_producer_gamma"],
        tools=[gista_tools.voiceover],
        context=[
            {
                "depends_on": parse_script,
                "segment_bundle": "qa_late_bundle"
            }
        ],
        output_pydantic=ContentValidationOutput
    )
    
    generate_transcript = Task(
        description=(
            "Create transcript from all completed segments:\n"
            "1. Collect all segment audio files\n"
            "2. Process in segment index order\n"
            "3. Maintain speaker attribution\n"
            "4. Combine into final transcript"
        ),
        expected_output="Complete transcript document",
        agent=agents["transcriber"],
        tools=[gista_tools.transcription],
        context=[
            {
                "depends_on": [parse_script, readout_production, 
                             qa_production_early, qa_production_middle, 
                             qa_production_late],
                "segment_order": "index"
            }
        ],
        output_pydantic=ContentValidationOutput
    )
    
    return [
        parse_script,
        readout_production,
        qa_production_early,
        qa_production_middle,
        qa_production_late,
        generate_transcript
    ]

def create_all_gista_tasks(agents):
    """
    Create and return all tasks in workflow order:
    1. Content Assessment → 2. Analysis → 3. Script → 4. Voice
    """
    validation_tasks = create_user_content_validation_tasks(agents)
    research_tasks = create_user_content_research_tasks(agents, validation_tasks)
    script_tasks = create_script_production_tasks(agents["script_production"])
    voice_tasks = create_voice_generation_tasks(agents["voice_generation"])
    
    # Combine in workflow order
    all_tasks = (
        validation_tasks +
        research_tasks +
        script_tasks +
        voice_tasks
    )
    
    return all_tasks

def task_completed_callback(output):
    print(f"Task completed with status: {output.status}")
