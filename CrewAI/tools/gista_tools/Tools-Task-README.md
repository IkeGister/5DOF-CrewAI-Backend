# Gista Tools and Tasks Overview

## Available Tools (from GistaToolbox)

### Research Tools
1. Enhanced Web Search Tool (SerperDev)
2. Wikipedia Research Tool
3. Dictionary Tool
4. Web Scraper Tool
5. Content Extraction Tools (PDF, DOCX, CSV, Directory readers)

### Podcast Generation Tools
1. Script Parser Tool
2. Transcription Tool
3. ElevenLabs Voiceover Tool

## Tasks by Department with Tool Assignments

### 1. Content Validation & Assessment
1. Prepare Content Task
   - **Assigned Tools**: 
     - Web Scraper Tool
     - PDF Reader Tool
     - DOCX Reader Tool
     - CSV Reader Tool
     - Directory Reader Tool
   - **Purpose**: Extract and validate raw content
   - **Output**: Content validation and extraction results

2. Approve/Reject Content Tasks
   - **Purpose**: User feedback and workflow direction
   - **Tools**: None currently (TODO: notification tools)
   - **Dependencies**: prepare_content

### 2. Content Research & Analysis
1. Start Production Pipeline Task
   - **Assigned Tools**:
     - Enhanced Web Search
     - Wikipedia Research
     - Dictionary Tool
   - **Purpose**: Research preparation and initial analysis

2. Content Analysis Task
   - **Assigned Tools**:
     - Enhanced Web Search
     - Wikipedia Research
     - Dictionary Tool
   - **Purpose**: Structure and concept mapping

3. Terminology Analysis Task
   - **Assigned Tools**:
     - Enhanced Web Search
     - Dictionary Tool
     - Wikipedia Research
   - **Purpose**: Technical term analysis

4. Background Research Task
   - **Assigned Tools**:
     - Enhanced Web Search
     - Wikipedia Research
     - Dictionary Tool
   - **Purpose**: Deep research and verification

5. Content Presentation Task
   - **Assigned Tools**:
     - Enhanced Web Search
     - Dictionary Tool
     - Wikipedia Research
   - **Purpose**: Research synthesis and preparation for script

### 3. Script Production
1. Opening Transition Task
   - **Purpose**: Show introduction and content preview
   - **Dependencies**: Content research tasks

2. Readout Script Task
   - **Purpose**: Content readout preparation
   - **Dependencies**: Opening transition

3. Expert Introduction Task
   - **Purpose**: Expert setup and analysis preview
   - **Dependencies**: Readout script

4. Q&A Script Task
   - **Purpose**: Q&A segment scripting with transitions
   - **Dependencies**: Expert introduction

5. Closing Transition Task
   - **Purpose**: Show wrap-up and sign-off
   - **Dependencies**: Q&A script

### 4. Voice Generation
1. Parse Script Task
   - **Assigned Tool**: Script Parser Tool
   - **Purpose**: Break script into parallel-processable segments
   - **Output**: Segment bundles for parallel processing

2. Audio Production Tasks
   - **Assigned Tool**: ElevenLabs Voiceover Tool
   - Readout Production
   - Q&A Production Early (segments 1-3)
   - Q&A Production Middle (segments 4-6)
   - Q&A Production Late (segments 7-10)
   - **Purpose**: Parallel audio generation

3. Generate Transcript Task
   - **Assigned Tool**: Transcription Tool
   - **Purpose**: Final transcript creation
   - **Dependencies**: All audio segments

### Task Dependencies Flow
```
Content Validation → Content Research → Script Production → Voice Generation
     ├─ prepare_content
     ├─ approve/reject
         └─► Research Tasks (parallel)
             ├─ content_analysis
             ├─ terminology_analysis
             ├─ background_research
             └─ content_presentation
                 └─► Script Tasks (sequential)
                     ├─ opening
                     ├─ readout
                     ├─ expert_intro
                     ├─ qa_script
                     └─ closing
                         └─► Voice Tasks (parallel after parse)
                             ├─ parse_script
                             ├─ readout_production
                             ├─ qa_early
                             ├─ qa_middle
                             ├─ qa_late
                             └─ transcript
```

### Task Output Models

1. ContentValidationOutput
   - status, content_status
   - metadata, validation flags
   - content complexity metrics

2. ContentAnalysisOutput
   - content_map
   - relationship_map
   - analysis_metrics

3. TerminologyAnalysisOutput
   - technical_glossary
   - concept_groups
   - explanation_strategy

4. ScriptOutput
   - segment_type (opening/readout/expert_intro/qa/closing)
   - script_content (by speaker role)
   - transitions (entry/exit)
   - technical_terms
   - segment_metadata
   - references
   - qa_context (optional)

### Notes
1. Research tools are consistently used across research tasks
2. Script production focuses on show flow and transitions
3. Voice generation enables parallel processing
4. Each department has clear tool assignments
5. Dependencies are structured for optimal parallelization

### Script Production Department
1. Readout Script Task
   - **Tools**: None currently assigned
2. Q&A Script Task
   - **Tools**: None currently assigned
3. Transitions Task
   - **Tools**: None currently assigned

### Audio Production Department
1. Readout Production Task
   - **Tools**: None currently assigned
2. Q&A Production Tasks (α,β,γ)
   - **Tools**: None currently assigned
3. Audio Mixing Task
   - **Tools**: None currently assigned
4. Sound Design Task
   - **Tools**: None currently assigned

### Quality Assurance Department
1. Content Quality Task
   - **Tools**: None currently assigned
2. Fact Checking Task
   - **Tools**: None currently assigned
3. Audio Quality Task
   - **Tools**: None currently assigned

### Project Management Department
1. Workflow Coordination Task
   - **Tools**: None currently assigned
2. Resource Optimization Task
   - **Tools**: None currently assigned
3. Quality Management Task
   - **Tools**: None currently assigned

## Potential Tool-to-Task Assignments Needed

### Content Assessment Tasks
- Could use Wikipedia, Dictionary, Academic, and Technical Documentation tools for research tasks
- News Research Tool could assist with current context analysis

### Script Production Tasks
- Could benefit from research tools for fact verification
- Might need specialized writing/editing tools

### Quality Assurance Tasks
- Could use research tools for fact checking
- Might need specialized audio analysis tools

### Project Management Tasks
- Could benefit from project tracking and analytics tools

## Notes
1. Only Voice Generation department has complete tool coverage
2. Research tools are available but not currently assigned to specific tasks
3. Some departments may need additional specialized tools
4. Project Management tasks might need different types of tools

### Task Output Statuses

1. Content Validation (QA & Assessment):
   - content_status: CLEARED/REJECTED/NEEDS_REVIEW
   - Details included in validation/assessment results

2. Script Generation:
   - script_status: COMPLETED/FAILED
   - Includes: readout_script, segment_scripts, transitions

3. Voice Generation:
   - voice_status: COMPLETED/FAILED
   - Includes: audio_segments, transcript

4. Pipeline Status Values:
   - "completed": Full pipeline success
   - "validation_failed": Initial QA check failed
   - "content_rejected": Content assessment failed
   - "error": Exception occurred (with details)
