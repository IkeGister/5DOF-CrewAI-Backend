"""
Gista App Tasks Module
=====================

This module defines the tasks for the Gista App workflow, organized by department.
Each task is assigned to specific agents and follows the workflow progression
from content assessment through final delivery.
"""

from crewai import Task
from tools.gista_tools.gista_general_tools import GistaToolbox

def create_voice_generation_tasks(agents):
    """
    Create tasks for voice generation workflow
    
    Args:
        agents: Dictionary containing voice generation agents
        
    Returns:
        list: List of voice generation tasks with their specific tools
    """
    
    # Initialize toolbox
    gista_tools = GistaToolbox()
    
    parse_script = Task(
        description=(
            "Convert podcast script from markdown format into structured segments.\n"
            "1. Extract metadata (title, source, etc.)\n"
            "2. Identify voice roles and segment types\n"
            "3. Parse pause and emphasis markers\n"
            "4. Maintain proper segment ordering"
        ),
        expected_output=(
            "JSON formatted segment data containing:\n"
            "- Metadata with title and source information\n"
            "- List of segments with voice roles and text\n"
            "- Properly marked pauses and emphasis points"
        ),
        agent=agents["parser"],
        tools=[gista_tools.script_parser]  # Get tool from toolbox
    )
    
    generate_audio = Task(
        description=(
            "Generate audio segments using ElevenLabs voices.\n"
            "1. Use appropriate voice for each role (host/expert/readout)\n"
            "2. Maintain consistent voice across segments\n"
            "3. Apply proper pacing using pause markers\n"
            "4. Handle emphasis points naturally"
        ),
        expected_output=(
            "List of audio segment files with:\n"
            "- Proper voice role assignment\n"
            "- Natural pacing and emphasis\n"
            "- Consistent audio quality"
        ),
        agent=agents["generator"],
        tools=[gista_tools.voiceover]  # Get tool from toolbox
    )
    
    generate_transcript = Task(
        description=(
            "Create clean transcript from podcast script with proper "
            "speaker attribution and formatting.\n"
            "1. Include clear speaker identification\n"
            "2. Maintain proper segmentation\n"
            "3. Preserve metadata and source information"
        ),
        expected_output=(
            "Formatted transcript document with:\n"
            "- Clear speaker identification\n"
            "- Proper segmentation\n"
            "- Complete metadata"
        ),
        agent=agents["transcriber"],
        tools=[gista_tools.transcription],  # Get tool from toolbox
        context={
            "depends_on": parse_script,
            "format_type": "clean"
        }
    )
    
    return [parse_script, generate_audio, generate_transcript]

def create_content_assessment_tasks(agents):
    """Create tasks for the Content Assessment Department"""
    
    # Initialize toolbox
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
            "3. Structure the output data:\n"
                "a) Top-level Information:\n"
                    "- status: success/failure\n"
                    "- content_status: REJECTED/NEEDS_REVIEW/CLEARED\n"
                "b) Metadata:\n"
                    "- title, author, publication_date, source, url\n"
                    "- content_metrics:\n"
                        "* estimated_read_time\n"
                        "* estimated_word_count\n"
                        "* estimated_listening_times (slow/normal/fast/recommended)\n"
                        "* estimated_final_duration\n"
                "c) Content Validation Flags:\n"
                    "- is_image_only: true/false\n"
                    "- has_text_content: true/false\n"
                    "- estimated_word_count: number\n"
                    "- contains_code_blocks: true/false\n"
                    "- is_audio_file: true/false\n"
                    "- is_video_content: true/false\n"
                "d) Content Complexity:\n"
                    "- technical_terms_count\n"
                    "- average_sentence_length\n"
                    "- recommended_speaking_pace\n"
                    "- content_type\n"
                "e) Extracted Content:\n"
                    "- raw_text\n"
                    "- sections with position and duration\n"
                    "- removed_elements log\n"
                "f) Processing Info:\n"
                    "- tool_used, timestamp, content_hash\n"
            "4. Set content_status based on validation rules:\n"
                "- REJECTED if:\n"
                    "* is_image_only is true\n"
                    "* has_text_content is false\n"
                    "* estimated_word_count < 100\n"
                    "* is_audio_file is true\n"
                    "* is_video_content is true\n"
                "- NEEDS_REVIEW if:\n"
                    "* contains_code_blocks is true\n"
                    "* estimated_word_count > 5000\n"
                "- CLEARED otherwise\n"
            "5. Calculate timing estimates:\n"
                "- Use standard speaking rates (100-120/130-150/160-180 wpm)\n"
                "- Account for content complexity\n"
                "- Include podcast element durations\n"
                "- Provide section-level timing"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "{\n"
            "    'status': 'success/failure',\n"
            "    'content_status': 'REJECTED/NEEDS_REVIEW/CLEARED',\n"
            "    'metadata': {\n"
            "        'title': string,\n"
            "        'author': string,\n"
            "        'publication_date': date,\n"
            "        'source': string,\n"
            "        'url': string,\n"
            "        'content_metrics': {\n"
            "            'estimated_read_time': string,\n"
            "            'estimated_word_count': number,\n"
            "            'estimated_listening_times': {\n"
            "                'slow_pace': string,\n"
            "                'normal_pace': string,\n"
            "                'fast_pace': string,\n"
            "                'recommended_pace': string\n"
            "            },\n"
            "            'estimated_final_duration': string\n"
            "        }\n"
            "    },\n"
            "    'content_validation': {...},\n"
            "    'content_complexity': {...},\n"
            "    'extracted_content': {\n"
            "        'raw_text': string,\n"
            "        'sections': [{\n"
            "            'type': string,\n"
            "            'content': string,\n"
            "            'position': number,\n"
            "            'estimated_duration': string\n"
            "        }],\n"
            "        'removed_elements': [...]\n"
            "    },\n"
            "    'processing_info': {...}\n"
            "}"
        ),
        agent=agents["content_assessment"]["doc_assessor"],
        tools=[
            gista_tools.web_scraper,   # For web pages
            gista_tools.pdf_reader,    # For PDFs
            gista_tools.docx_reader,   # For Word docs
            gista_tools.csv_reader,    # For CSV files
            gista_tools.directory_reader  # For local files
        ]
    )
    
    approve_content = Task(
        description=(
            "Process CLEARED or NEEDS_REVIEW content for quick approval response:\n"
            "1. Verify content_status from prepare_content output\n"
            "2. Generate appropriate approval message\n"
            "3. Prepare user notification with initial timeline estimate"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "{\n"
            "    'status': 'approved',\n"
            "    'workflow_type': 'standard|special_review',\n"
            "    'content_info': {\n"
            "        'title': string,\n"
            "        'source': string,\n"
            "        'content_hash': string\n"
            "    },\n"
            "    'approval_details': {\n"
            "        'approval_timestamp': datetime,\n"
            "        'initial_assessment': string,\n"
            "        'estimated_completion': string\n"
            "    },\n"
            "    'ui_message': {\n"
            "        'short_message': string,  # e.g., 'Content approved for podcast production'\n"
            "        'detailed_message': string,  # e.g., 'Your content is now being processed...'\n"
            "        'next_steps': string  # e.g., 'You will be notified when...'\n"
            "    }\n"
            "}"
        ),
        agent=agents["content_assessment"]["doc_assessor"],
        tools=[],  # No tools needed for quick approval
        context={
            "depends_on": "prepare_content"
        }
    )

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
            "{\n"
            "    'original_content': {\n"
            "        'raw_text': string,\n"
            "        'metadata': {\n"
            "            'title': string,\n"
            "            'author': string,\n"
            "            'publication_date': string,\n"
            "            'source': string,\n"
            "            'url': string,\n"
            "            'content_hash': string\n"
            "        }\n"
            "    },\n"
            "    'analysis_preparation': {\n"
            "        'content_analysis_input': {\n"
            "            'sections': [{\n"
            "                'id': string,\n"
            "                'text': string,\n"
            "                'type': string,\n"
            "                'position': number\n"
            "            }],\n"
            "            'preliminary_terms': [{\n"
            "                'term': string,\n"
            "                'location': {\n"
            "                    'section_id': string,\n"
            "                    'position': number\n"
            "                }\n"
            "            }],\n"
            "            'potential_quotes': [{\n"
            "                'text': string,\n"
            "                'speaker': string,\n"
            "                'section_id': string\n"
            "            }]\n"
            "        },\n"
            "        'terminology_flags': [{\n"
            "            'term': string,\n"
            "            'context': string,\n"
            "            'requires_research': boolean\n"
            "        }],\n"
            "        'research_targets': [{\n"
            "            'claim': string,\n"
            "            'type': 'factual|statistical|technical',\n"
            "            'verification_priority': number  # 1-10\n"
            "        }]\n"
            "    },\n"
            "    'special_requirements': [{\n"
            "        'type': string,\n"
            "        'description': string,\n"
            "        'handling_instructions': string\n"
            "    }]\n"
            "}"
        ),
        agent=agents["content_assessment"]["doc_assessor"],
        tools=[gista_tools.technical],  # For initial technical assessment
        context={
            "depends_on": ["prepare_content", "approve_content"]
        }
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
            "{\n"
            "    'status': 'rejected',\n"
            "    'original_content': {\n"
            "        'url': string,\n"
            "        'title': string,\n"
            "        'content_hash': string\n"
            "    },\n"
            "    'rejection_details': {\n"
            "        'primary_reason': string,\n"
            "        'validation_flags': {\n"
            "            'is_image_only': boolean,\n"
            "            'is_audio_file': boolean,\n"
            "            'is_video_content': boolean,\n"
            "            'has_text_content': boolean,\n"
            "            'word_count': number\n"
            "        },\n"
            "        'explanation': string,\n"
            "        'suggestions': [{\n"
            "            'type': string,\n"
            "            'description': string\n"
            "        }]\n"
            "    },\n"
            "    'ui_message': {\n"
            "        'short_message': string,\n"
            "        'detailed_message': string,\n"
            "        'action_required': string\n"
            "    }\n"
            "}"
        ),
        agent=agents["content_assessment"]["doc_assessor"],
        tools=[],  # No additional tools needed for rejection processing
        context={
            "depends_on": "prepare_content"
        }
    )

    terminology_analysis = Task(
        description=(
            "Analyze and expand technical elements from content analysis:\n"
            "1. Process technical_elements from content_map:\n"
                "a) Research each term's definition and usage\n"
                "b) Identify prerequisite concepts\n"
                "c) Determine explanation complexity\n"
                "d) Find common analogies or examples\n"
            "2. Review concept relationships:\n"
                "a) Map technical dependencies\n"
                "b) Identify concept prerequisites\n"
                "c) Group related technical terms\n"
            "3. Analyze quotations containing technical terms:\n"
                "a) Extract technical context\n"
                "b) Link expert explanations\n"
            "4. Generate explanation strategies:\n"
                "a) Basic to advanced progression\n"
                "b) Analogy mappings\n"
                "c) Prerequisite ordering"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "{\n"
            "    'technical_glossary': [{\n"
            "        'term_id': string,  # from content_analysis\n"
            "        'term': string,\n"
            "        'formal_definition': string,\n"
            "        'simplified_explanation': string,\n"
            "        'prerequisites': [string],  # term_ids\n"
            "        'analogies': [{\n"
            "            'comparison': string,\n"
            "            'explanation': string\n"
            "        }],\n"
            "        'usage_examples': [string],\n"
            "        'expert_quotes': [string]  # quote_ids from content_analysis\n"
            "    }],\n"
            "    'concept_groups': [{\n"
            "        'group_id': string,\n"
            "        'theme': string,\n"
            "        'terms': [string],  # term_ids\n"
            "        'explanation_order': [string]  # term_ids in optimal order\n"
            "    }],\n"
            "    'explanation_strategy': {\n"
            "        'complexity_progression': [{\n"
            "            'level': string,\n"
            "            'terms': [string],  # term_ids\n"
            "            'approach': string\n"
            "        }],\n"
            "        'key_analogies': [{\n"
            "            'complex_concept': string,  # term_id\n"
            "            'analogy_chain': [{\n"
            "                'step': number,\n"
            "                'explanation': string\n"
            "            }]\n"
            "        }]\n"
            "    }\n"
            "}"
        ),
        agent=agents["content_assessment"]["keyword_analyst"],
        tools=[
            gista_tools.dictionary,     # For definitions
            gista_tools.technical,      # For technical context
            gista_tools.academic,       # For academic explanations
            gista_tools.wikipedia       # For broader context and common explanations
        ],
        context={
            "depends_on": "content_analysis"
        }
    )

    background_research = Task(
        description=(
            "Research and validate content from content analysis:\n"
            "1. Process key_concepts from content_map:\n"
                "a) Verify factual claims\n"
                "b) Find supporting research\n"
                "c) Identify current developments\n"
            "2. Analyze quoted statistics and claims:\n"
                "a) Verify accuracy\n"
                "b) Find original sources\n"
                "c) Check for updates or corrections\n"
            "3. Research topic clusters:\n"
                "a) Gather contextual information\n"
                "b) Identify key developments\n"
                "c) Find expert consensus\n"
            "4. Compile supporting evidence:\n"
                "a) Academic sources\n"
                "b) Expert opinions\n"
                "c) Recent developments"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "{\n"
            "    'concept_validation': [{\n"
            "        'concept_id': string,  # from content_analysis\n"
            "        'verification_status': 'verified|updated|disputed',\n"
            "        'supporting_evidence': [{\n"
            "            'source_type': 'academic|expert|news',\n"
            "            'source': string,\n"
            "            'relevance_score': number,  # 1-10\n"
            "            'key_points': [string]\n"
            "        }],\n"
            "        'current_context': {\n"
            "            'recent_developments': [string],\n"
            "            'expert_consensus': string,\n"
            "            'industry_impact': string\n"
            "        }\n"
            "    }],\n"
            "    'quote_verification': [{\n"
            "        'quote_id': string,  # from content_analysis\n"
            "        'verification_status': 'verified|updated|disputed',\n"
            "        'original_source': string,\n"
            "        'context_notes': string,\n"
            "        'updates_or_corrections': [string]\n"
            "    }],\n"
            "    'topic_research': [{\n"
            "        'cluster_id': string,  # from content_analysis\n"
            "        'context_summary': string,\n"
            "        'key_developments': [{\n"
            "            'date': string,\n"
            "            'development': string,\n"
            "            'significance': string\n"
            "        }],\n"
            "        'expert_insights': [{\n"
            "            'expert': string,\n"
            "            'insight': string,\n"
            "            'relevance': string\n"
            "        }]\n"
            "    }]\n"
            "}"
        ),
        agent=agents["content_assessment"]["research_specialist"],
        tools=[
            gista_tools.academic,    # For academic research
            gista_tools.technical,   # For technical verification
            gista_tools.news         # For current developments
        ],
        context={
            "depends_on": "content_analysis"
        }
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

    content_analysis = Task(
        description=(
            "Analyze and structure content for technical assessment:\n"
            "1. Parse the approved content JSON:\n"
                "a) Access raw_text from extracted_content\n"
                "b) Review section breakdowns\n"
                "c) Consider content complexity metrics\n"
            "2. Identify and categorize content elements:\n"
                "a) Key Concepts:\n"
                    "- Main ideas and theories\n"
                    "- Core arguments\n"
                    "- Critical findings\n"
                "b) Technical Elements:\n"
                    "- Technical terms and jargon\n"
                    "- Scientific concepts\n"
                    "- Methodologies or processes\n"
                "c) Quotations:\n"
                    "- Direct quotes with attribution\n"
                    "- Statistical citations\n"
                    "- Expert statements\n"
            "3. Map content relationships:\n"
                "- Concept hierarchies\n"
                "- Dependency chains\n"
                "- Topic clusters"
        ),
        expected_output=(
            "A structured JSON document containing:\n"
            "{\n"
            "    'content_map': {\n"
            "        'key_concepts': [{\n"
            "            'id': string,\n"
            "            'type': 'main_idea|theory|argument|finding',\n"
            "            'text': string,\n"
            "            'location': {\n"
            "                'section': number,\n"
            "                'paragraph': number\n"
            "            },\n"
            "            'importance_score': number,  # 1-10\n"
            "            'related_concepts': [string]  # IDs of related concepts\n"
            "        }],\n"
            "        'technical_elements': [{\n"
            "            'id': string,\n"
            "            'type': 'term|concept|methodology',\n"
            "            'text': string,\n"
            "            'context': string,\n"
            "            'complexity_score': number,  # 1-10\n"
            "            'requires_explanation': boolean,\n"
            "            'related_terms': [string]  # IDs of related terms\n"
            "        }],\n"
            "        'quotations': [{\n"
            "            'id': string,\n"
            "            'type': 'expert_quote|statistic|citation',\n"
            "            'text': string,\n"
            "            'speaker': string,\n"
            "            'context': string,\n"
            "            'supports_concept': string  # ID of supported concept\n"
            "        }]\n"
            "    },\n"
            "    'relationship_map': {\n"
            "        'concept_hierarchies': [{\n"
            "            'parent_id': string,\n"
            "            'child_ids': [string],\n"
            "            'relationship_type': string\n"
            "        }],\n"
            "        'topic_clusters': [{\n"
            "            'cluster_id': string,\n"
            "            'theme': string,\n"
            "            'elements': [string]  # IDs of related elements\n"
            "        }]\n"
            "    },\n"
            "    'analysis_metrics': {\n"
            "        'total_concepts': number,\n"
            "        'technical_density': number,  # percentage\n"
            "        'complexity_distribution': {\n"
            "            'basic': number,\n"
            "            'intermediate': number,\n"
            "            'advanced': number\n"
            "        },\n"
            "        'key_themes': [string]\n"
            "    }\n"
            "}"
        ),
        agent=agents["content_assessment"]["keyword_analyst"],
        tools=[
            gista_tools.technical,    # For technical term identification
            gista_tools.dictionary    # For term classification
        ],
        context={
            "depends_on": "start_production_pipeline",
            "required_data": ["analysis_preparation.content_analysis_input"]
        }
    )

    content_presentation = Task(
        description=(
            "Synthesize analyzed content into a structured markdown document for script production:\n"
            "1. Integrate data from multiple sources:\n"
                "a) content_analysis output:\n"
                    "- Key concepts and their relationships\n"
                    "- Technical elements and complexity\n"
                    "- Important quotations\n"
                "b) terminology_analysis output:\n"
                    "- Technical glossary\n"
                    "- Explanation strategies\n"
                    "- Concept progressions\n"
                "c) background_research output:\n"
                    "- Verified claims and sources\n"
                    "- Current context\n"
                    "- Expert insights\n"
            "2. Structure content for podcast format:\n"
                "a) Opening Overview:\n"
                    "- Main topic introduction\n"
                    "- Key themes preview\n"
                    "- Complexity level indication\n"
                "b) Content Progression:\n"
                    "- Logical concept ordering\n"
                    "- Technical term introduction points\n"
                    "- Natural knowledge building\n"
                "c) Discussion Points:\n"
                    "- Expert quote placements\n"
                    "- Statistical evidence positions\n"
                    "- Explanation opportunities\n"
            "3. Add markdown emphasis markers:\n"
                "- **bold** for key terms\n"
                "- *italic* for emphasis\n"
                "- `code` for technical terms\n"
                "- > for quotations\n"
                "- --- for segment breaks\n"
                "- // for pause indicators"
        ),
        expected_output=(
            "A markdown document structured as:\n"
            "```markdown\n"
            "# [Article Title]\n"
            "Source: [Original Source]\n"
            "\n"
            "## Content Overview\n"
            "- Complexity Level: [basic|intermediate|advanced]\n"
            "- Estimated Duration: [time]\n"
            "- Key Themes: [list]\n"
            "\n"
            "## Original Content\n"
            "```json\n"
            "// Original content and metadata from prepare_content\n"
            "{\n"
            "    \"raw_text\": \"full original text\",\n"
            "    \"metadata\": {...},\n"
            "    \"sections\": [...]\n"
            "}\n"
            "```\n"
            "\n"
            "## Analysis Results\n"
            "```json\n"
            "// Results from content_analysis, terminology_analysis, and background_research\n"
            "{\n"
            "    \"content_map\": {...},\n"
            "    \"technical_glossary\": {...},\n"
            "    \"verified_claims\": [...]\n"
            "}\n"
            "```\n"
            "\n"
            "## Technical Glossary\n"
            "- `term`: definition // simplified explanation\n"
            "- `term`: definition // simplified explanation\n"
            "\n"
            "## Content Sections\n"
            "\n"
            "### 1. Introduction\n"
            "[Introductory content with *emphasis* and **key terms**]\n"
            "\n"
            "### 2. Main Content\n"
            "[Section content]\n"
            "> Expert quote with attribution\n"
            "\n"
            "#### Technical Explanation Breakout\n"
            "- Concept: [explanation]\n"
            "- Analogy: [comparison]\n"
            "\n"
            "### 3. Analysis Points\n"
            "1. [Point with supporting evidence]\n"
            "2. [Point with expert insight]\n"
            "\n"
            "---\n"
            "\n"
            "## Production Notes\n"
            "- Pause Points: [locations]\n"
            "- Emphasis Guide: [key moments]\n"
            "- Technical Term Order: [progression]\n"
            "- Expert Quote Placements: [positions]\n"
            "\n"
            "## Reference Data\n"
            "- Verified Sources: [list]\n"
            "- Expert Citations: [list]\n"
            "- Current Context: [updates]\n"
            "\n"
            "## Raw Analysis Data\n"
            "```json\n"
            "// Complete analysis data for reference\n"
            "{\n"
            "    \"content_analysis\": {...},\n"
            "    \"terminology_analysis\": {...},\n"
            "    \"background_research\": {...}\n"
            "}\n"
            "```\n"
            "```"
        ),
        agent=agents["content_assessment"]["analysis_presenter"],
        tools=[],  # No additional tools needed - this is a synthesis task
        context={
            "depends_on": [
                "content_analysis",
                "terminology_analysis",
                "background_research"
            ]
        }
    )

    return [
        prepare_content,
        approve_content,
        reject_content,
        start_production_pipeline,
        content_analysis,
        terminology_analysis,
        background_research,
        analysis_framework,
        content_presentation
    ]

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
    """
    Create and return all tasks for the Gista workflow
    
    Args:
        agents: Dictionary containing all Gista agents by department
        
    Returns:
        list: Complete list of ordered tasks for the workflow
    """
    
    tasks = (
        create_content_assessment_tasks(agents["content_assessment"]) +
        create_script_production_tasks(agents["script_production"]) +
        create_voice_generation_tasks(agents["voice_generation"]) +
        create_audio_production_tasks(agents["audio_production"]) +
        create_quality_assurance_tasks(agents["quality_assurance"]) +
        create_project_management_tasks(agents["project_management"])
    )
    
    return tasks
