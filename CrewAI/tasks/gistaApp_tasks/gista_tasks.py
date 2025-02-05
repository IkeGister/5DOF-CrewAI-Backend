"""
Gista App Tasks Module
=====================

This module defines the tasks for the Gista App workflow, organized by department.
Each task is assigned to specific agents and follows the workflow progression
from content assessment through final delivery.
"""

from crewai import Task

def create_content_assessment_tasks(agents):
    """Create tasks for the Content Assessment Department"""
    
    initial_assessment = Task(
        description=(
            "Perform initial document evaluation:\n"
            "1. Assess document type and format\n"
            "2. Evaluate content length and complexity\n"
            "3. Determine content suitability for podcast conversion\n"
            "4. Identify potential challenges or special requirements\n"
            "5. Estimate processing time and resource needs"
        ),
        expected_output=(
            "A detailed assessment report including:\n"
            "- Document classification\n"
            "- Content complexity score\n"
            "- Suitability rating\n"
            "- Potential challenges\n"
            "- Resource requirements"
        ),
        agent=agents["content_assessment"]["doc_assessor"],
        tools=[],
    )

    terminology_analysis = Task(
        description=(
            "Analyze technical terminology and key concepts:\n"
            "1. Identify all technical terms and industry jargon\n"
            "2. Create a glossary of terms requiring explanation\n"
            "3. Mark sections needing additional context\n"
            "4. Suggest simplification approaches where needed"
        ),
        expected_output=(
            "A comprehensive terminology report including:\n"
            "- Technical terms glossary\n"
            "- Sections needing context\n"
            "- Simplification recommendations"
        ),
        agent=agents["content_assessment"]["keyword_analyst"],
        tools=[],
    )

    background_research = Task(
        description=(
            "Conduct background research:\n"
            "1. Research identified technical terms\n"
            "2. Gather additional context for complex concepts\n"
            "3. Verify facts and statistics\n"
            "4. Compile relevant supporting information"
        ),
        expected_output=(
            "A research compilation including:\n"
            "- Term explanations\n"
            "- Context notes\n"
            "- Fact verification\n"
            "- Supporting documentation"
        ),
        agent=agents["content_assessment"]["research_specialist"],
        tools=[],
    )

    analysis_framework = Task(
        description=(
            "Create Q&A framework and analysis structure:\n"
            "1. Identify key discussion points\n"
            "2. Structure content flow\n"
            "3. Develop Q&A pairs\n"
            "4. Create content breakdown for audio segments"
        ),
        expected_output=(
            "A structured analysis document including:\n"
            "- Key discussion points\n"
            "- Q&A framework\n"
            "- Content flow outline\n"
            "- Segment breakdown"
        ),
        agent=agents["content_assessment"]["analysis_presenter"],
        tools=[],
    )

    return [initial_assessment, terminology_analysis, background_research, analysis_framework]

def create_script_production_tasks(agents):
    """Create tasks for the Script Production Department"""
    
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
    )

    qa_script = Task(
        description=(
            "Develop Q&A segment scripts:\n"
            "1. Convert analysis points into natural dialogue\n"
            "2. Create host questions and expert responses\n"
            "3. Include technical explanations\n"
            "4. Structure discussion flow"
        ),
        expected_output=(
            "Q&A scripts including:\n"
            "- Host questions\n"
            "- Expert responses\n"
            "- Technical explanations\n"
            "- Discussion flow markers"
        ),
        agent=agents["script_production"]["qa_script_writer"],
        tools=[],
    )

    transitions = Task(
        description=(
            "Write segment transitions:\n"
            "1. Create smooth transitions between segments\n"
            "2. Ensure logical flow\n"
            "3. Maintain engagement\n"
            "4. Add audio cues"
        ),
        expected_output=(
            "A set of transitions including:\n"
            "- Segment connectors\n"
            "- Flow markers\n"
            "- Audio cue points"
        ),
        agent=agents["script_production"]["transition_writer"],
        tools=[],
    )

    return [readout_script, qa_script, transitions]

def create_audio_production_tasks(agents):
    """Create tasks for the Audio Production Department"""
    
    readout_production = Task(
        description=(
            "Produce readout audio segments:\n"
            "1. Record verbatim content\n"
            "2. Ensure clear pronunciation\n"
            "3. Add emphasis as marked\n"
            "4. Include proper pauses"
        ),
        expected_output="High-quality audio files of readout segments",
        agent=agents["audio_production"]["readout_producer"],
        tools=[],
    )

    qa_production_early = Task(
        description="Produce Q&A segments 1-3 with proper pacing and tone",
        expected_output="Audio files for Q&A segments 1-3",
        agent=agents["audio_production"]["qa_producer_alpha"],
        tools=[],
    )

    qa_production_middle = Task(
        description="Produce Q&A segments 4-6 with proper pacing and tone",
        expected_output="Audio files for Q&A segments 4-6",
        agent=agents["audio_production"]["qa_producer_beta"],
        tools=[],
    )

    qa_production_late = Task(
        description="Produce Q&A segments 7-10 with proper pacing and tone",
        expected_output="Audio files for Q&A segments 7-10",
        agent=agents["audio_production"]["qa_producer_gamma"],
        tools=[],
    )

    audio_mixing = Task(
        description=(
            "Mix and master all audio segments:\n"
            "1. Combine all segments\n"
            "2. Balance audio levels\n"
            "3. Apply consistent EQ\n"
            "4. Ensure smooth transitions"
        ),
        expected_output="Final mixed and mastered audio file",
        agent=agents["audio_production"]["audio_mixer"],
        tools=[],
    )

    sound_design = Task(
        description=(
            "Add sound design elements:\n"
            "1. Insert transition effects\n"
            "2. Add background music\n"
            "3. Include sound effects\n"
            "4. Balance all audio elements"
        ),
        expected_output="Enhanced audio with sound design elements",
        agent=agents["audio_production"]["sound_designer"],
        tools=[],
    )

    return [readout_production, qa_production_early, qa_production_middle, 
            qa_production_late, audio_mixing, sound_design]

def create_quality_assurance_tasks(agents):
    """Create tasks for the Quality Assurance Department"""
    
    content_quality = Task(
        description=(
            "Verify content quality:\n"
            "1. Check content accuracy\n"
            "2. Verify educational value\n"
            "3. Ensure clarity of explanation\n"
            "4. Review technical accuracy"
        ),
        expected_output="Content quality verification report",
        agent=agents["quality_assurance"]["content_qa"],
        tools=[],
    )

    fact_checking = Task(
        description=(
            "Perform fact checking:\n"
            "1. Verify all claims\n"
            "2. Check statistics\n"
            "3. Validate references\n"
            "4. Document sources"
        ),
        expected_output="Fact checking verification report",
        agent=agents["quality_assurance"]["fact_checker"],
        tools=[],
    )

    audio_quality = Task(
        description=(
            "Verify audio quality:\n"
            "1. Check sound quality\n"
            "2. Verify audio consistency\n"
            "3. Review transitions\n"
            "4. Validate sound levels"
        ),
        expected_output="Audio quality verification report",
        agent=agents["quality_assurance"]["audio_qa"],
        tools=[],
    )

    return [content_quality, fact_checking, audio_quality]

def create_project_management_tasks(agents):
    """Create tasks for the Project Management Department"""
    
    workflow_coordination = Task(
        description=(
            "Coordinate overall workflow:\n"
            "1. Monitor task progression\n"
            "2. Manage handoffs\n"
            "3. Address bottlenecks\n"
            "4. Ensure timeline adherence"
        ),
        expected_output="Workflow status and coordination report",
        agent=agents["project_management"]["workflow_coordinator"],
        tools=[],
    )

    resource_optimization = Task(
        description=(
            "Optimize resource allocation:\n"
            "1. Monitor resource usage\n"
            "2. Adjust allocations\n"
            "3. Manage parallel processing\n"
            "4. Resolve resource conflicts"
        ),
        expected_output="Resource optimization report",
        agent=agents["project_management"]["resource_manager"],
        tools=[],
    )

    quality_management = Task(
        description=(
            "Manage overall quality:\n"
            "1. Review all QA reports\n"
            "2. Ensure standard compliance\n"
            "3. Approve final delivery\n"
            "4. Document quality metrics"
        ),
        expected_output="Final quality approval report",
        agent=agents["project_management"]["quality_manager"],
        tools=[],
    )

    return [workflow_coordination, resource_optimization, quality_management]

def create_research_workflow(tasks):
    """
    The research workflow should be:
    1. Initial terminology identification
    2. Dictionary lookup for basic understanding
    3. Technical documentation research for depth
    4. Academic verification for accuracy
    5. Current context for relevance
    6. Background research synthesis
    7. Final analysis framework creation
    """
    return [
        tasks["terminology_analysis"],
        tasks["dictionary_lookup"],
        tasks["technical_documentation"],
        tasks["academic_verification"],
        tasks["current_context"],
        tasks["background_research"],
        tasks["analysis_framework"]
    ]

def create_all_gista_tasks(agents):
    """Create and return all tasks for the Gista App workflow"""
    
    tasks = (
        create_content_assessment_tasks(agents) +
        create_script_production_tasks(agents) +
        create_audio_production_tasks(agents) +
        create_quality_assurance_tasks(agents) +
        create_project_management_tasks(agents)
    )
    
    return tasks
