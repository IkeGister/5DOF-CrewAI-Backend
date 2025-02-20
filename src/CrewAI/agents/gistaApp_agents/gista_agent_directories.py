"""
Gista Agent Directories
======================

Department-specific guidelines and standards for all Gista agents.
Each department has its own set of directories to guide their specific tasks.
"""

# Content Assessment Department Directories
def get_document_assessment_guidelines():
    return {
        "criteria": {
            "accepted": [
                "news article",
                "text-based PDF",
                "blog post",
                "website with primarily text content (e.g., Medium post)"
            ],
            "rejected": [
                "images",
                "videos (e.g., YouTube)",
                "music files",
                "other non-text content"
            ],
            "length_requirements": {
                "minimum_words": 500,
                "maximum_words": 5000,
                "optimal_range": "1000-3000 words"
            }
        },
        "metadata_requirements": [
            "author name",
            "publication date",
            "source/publisher",
            "title",
            "URL (if applicable)"
        ],
        "content_quality_markers": [
            "Clear structure",
            "Professional writing",
            "Factual content",
            "Educational value",
            "Coherent arguments"
        ]
    }

def get_keyword_analysis_guidelines():
    return {
        "identification_criteria": {
            "technical_terms": "Industry-specific vocabulary requiring explanation",
            "jargon": "Specialized terms needing clarification",
            "key_concepts": "Core ideas central to the content",
            "acronyms": "Abbreviated terms requiring expansion"
        },
        "analysis_requirements": {
            "definition_format": {
                "term": "The word or phrase",
                "basic_definition": "Simple, clear explanation",
                "context": "How it's used in the document",
                "additional_notes": "Related concepts or implications"
            },
            "categorization": {
                "essential": "Must be explained in the podcast",
                "contextual": "Explain if time permits",
                "general": "Common knowledge terms"
            }
        }
    }

def get_research_guidelines():
    return {
        "research_areas": {
            "background": "Historical or contextual information",
            "current_developments": "Recent related news or updates",
            "expert_opinions": "Relevant expert perspectives",
            "statistics": "Supporting data and figures"
        },
        "source_requirements": {
            "primary_sources": "Original research, official documents",
            "secondary_sources": "Reputable analysis, expert commentary",
            "verification": "Cross-reference multiple sources"
        },
        "output_format": {
            "context_notes": "Brief background information",
            "key_findings": "Important discoveries or insights",
            "supporting_data": "Relevant statistics or quotes",
            "source_citations": "Reference links and attributions"
        }
    }

def get_analysis_framework_guidelines():
    return {
        "key_points_structure": {
            "quantity": "Exactly 10 key points per document",
            "identification_criteria": [
                "Main arguments or claims",
                "Supporting evidence",
                "Critical insights",
                "Technical concepts",
                "Practical implications"
            ],
            "point_format": {
                "title": "Clear, concise title (max 10 words)",
                "question": "Engaging question that introduces the point",
                "summary": "Comprehensive explanation (200-300 words)",
                "keywords": "List of technical terms and nuanced concepts"
            }
        },
        "qa_framework": {
            "question_types": [
                "Clarification questions",
                "Analysis questions",
                "Implementation questions",
                "Expert insight questions"
            ],
            "answer_requirements": {
                "depth": "Detailed but accessible",
                "length": "2-3 minutes when spoken",
                "structure": "Context → Explanation → Example"
            }
        }
    }

# Script Production Department Directories
def get_readout_script_guidelines():
    return {
        "script_structure": {
            "introduction": {
                "elements": [
                    "Article title",
                    "Author attribution",
                    "Publication information",
                    "Date of original publication"
                ],
                "format": "Clear, professional delivery"
            },
            "main_content": {
                "formatting": "Preserve original paragraphs",
                "pacing": "Add pause markers between sections",
                "emphasis": "Mark key phrases for emphasis"
            },
            "conclusion": {
                "elements": [
                    "Repeat attribution",
                    "Transition to analysis segment"
                ]
            }
        },
        "notation_system": {
            "pause_markers": "// for short pauses",
            "emphasis": "*text* for emphasized words",
            "pronunciation": "[ph: text] for phonetic guides"
        }
    }

def get_qa_script_guidelines():
    return {
        "segment_structure": {
            "introduction": {
                "length": "30-45 seconds",
                "elements": [
                    "Topic introduction",
                    "Context setting",
                    "Expert introduction"
                ]
            },
            "question_format": {
                "style": "Conversational yet focused",
                "length": "15-30 seconds per question",
                "elements": [
                    "Context",
                    "Core question",
                    "Follow-up prompt"
                ]
            },
            "answer_format": {
                "length": "2-3 minutes",
                "structure": [
                    "Direct response",
                    "Explanation",
                    "Example or application"
                ]
            }
        }
    }

# Audio Production Department Directories
def get_audio_production_guidelines():
    return {
        "technical_specifications": {
            "recording": {
                "format": "WAV",
                "sample_rate": "48kHz",
                "bit_depth": "24-bit",
                "channels": "Stereo"
            },
            "processing": {
                "compression": "2:1 ratio, -18dB threshold",
                "eq": "High-pass at 80Hz, presence boost 3-5kHz",
                "normalization": "-14 LUFS for streaming"
            }
        },
        "segment_requirements": {
            "readout": {
                "tone": "Professional, clear delivery",
                "pacing": "150-160 words per minute",
                "dynamics": "Consistent volume levels"
            },
            "qa_segments": {
                "host": "Engaging, conversational tone",
                "expert": "Authoritative yet accessible",
                "interaction": "Natural dialogue flow"
            }
        }
    }

def get_sound_design_guidelines():
    return {
        "elements": {
            "transitions": {
                "duration": "2-3 seconds",
                "style": "Professional, unobtrusive",
                "usage": "Between major segments"
            },
            "background": {
                "type": "Subtle ambient music",
                "level": "-30dB below dialogue",
                "placement": "During introductions and transitions"
            }
        },
        "branding": {
            "intro_sound": "Standard podcast intro theme",
            "outro_sound": "Consistent closing theme",
            "segment_markers": "Unique sound for Q&A transitions"
        }
    }

# Quality Assurance Department Directories
def get_quality_control_guidelines():
    return {
        "content_verification": {
            "accuracy": {
                "fact_checking": "Verify all claims and statistics",
                "source_validation": "Confirm credible sources",
                "consistency": "Check for contradictions"
            },
            "educational_value": {
                "clarity": "Clear explanation of concepts",
                "depth": "Appropriate level of detail",
                "engagement": "Maintains listener interest"
            }
        },
        "audio_quality": {
            "technical_checks": [
                "Volume consistency",
                "Audio clarity",
                "Background noise",
                "Distortion"
            ],
            "performance_checks": [
                "Natural delivery",
                "Proper pacing",
                "Clear pronunciation",
                "Appropriate emphasis"
            ]
        }
    }

# Project Management Department Directories
def get_workflow_management_guidelines():
    return {
        "process_coordination": {
            "handoffs": {
                "content_to_script": "Analysis framework → Script team",
                "script_to_audio": "Approved scripts → Production team",
                "audio_to_qa": "Recorded segments → QA team"
            },
            "parallel_processing": {
                "qa_segments": "Distribute among producers",
                "quality_checks": "Simultaneous content and audio QA"
            }
        },
        "resource_allocation": {
            "producer_assignment": "Round-robin distribution",
            "qa_workflow": "Parallel content and audio review",
            "bottleneck_prevention": "Dynamic resource reallocation"
        },
        "quality_standards": {
            "review_points": [
                "Post-analysis review",
                "Pre-recording script approval",
                "Post-production audio check",
                "Final episode review"
            ],
            "approval_requirements": {
                "content": "Accuracy and educational value",
                "audio": "Technical quality and engagement",
                "overall": "Professional podcast standards"
            }
        }
    }

def get_script_writing_guidelines():
    return {
        "readout_segment": {
            "structure": {
                "introduction": "Source attribution and context",
                "content": "Verbatim reproduction of original text",
                "transitions": "Smooth connections between paragraphs"
            },
            "style": "Professional, clear delivery while maintaining original tone"
        },
        "qa_segments": {
            "per_key_point": {
                "host_intro": "Brief context setting (30-45 seconds)",
                "question_format": "Natural, conversational yet focused",
                "expert_response": "Detailed explanation (2-3 minutes)",
                "follow_up": "Optional clarifying question if needed"
            },
            "transitions": "Smooth connections between key points"
        }
    }

def get_analysis_presentation_guidelines():
    return {
        "content_structure": {
            "introduction": "Briefly introduce the document and its context.",
            "qa_segment": "Develop a Q&A discussion addressing key points and context.",
            "clarity": "Ensure that each question is answered in a clear and educational manner."
        },
        "guidelines": (
            "1. The analysis should complement the readout by expanding on important topics.\n"
            "2. Design questions that provoke thoughtful discussion and context.\n"
            "3. Maintain a balanced tone that educates without bias."
        ),
        "references": "http://example.com/gista_analysis_guidelines"
    }

def get_podcast_assembly_guidelines():
    return {
        "requirements": {
            "transitions": "Ensure smooth transitions between the readout and analysis segments.",
            "length": "The final podcast should adhere to expected episode lengths.",
            "format": "Follow the organizational format for final podcast episodes."
        },
        "guidelines": (
            "1. Merge the two audio segments with seamless transitions.\n"
            "2. Optionally, insert brief transition markers or jingles.\n"
            "3. Conduct a final quality check for overall coherence."
        ),
        "references": "http://example.com/gista_podcast_assembly_guidelines"
    }

def get_analysis_presenter_guidelines():
    return {
        "key_points_analysis": {
            "quantity": "Exactly 10 key points per document",
            "identification_criteria": [
                "Main arguments or claims",
                "Supporting evidence",
                "Critical insights",
                "Technical concepts",
                "Practical implications"
            ],
            "structure_per_point": {
                "title": "Clear, concise title (max 10 words)",
                "question": "Engaging question that introduces the point",
                "summary": "Comprehensive explanation (200-300 words)",
                "keywords": "List of technical terms and nuanced concepts"
            }
        }
    }

def get_workflow_coordinator_guidelines():
    return {
        "responsibilities": (
            "1. Ensure each agent's output is correctly formatted for the next stage.\n"
            "2. Log each step of the workflow and monitor for errors or delays.\n"
            "3. Provide fallback or escalation procedures if any agent encounters issues.\n"
            "4. Serve as the central point for troubleshooting and iterative improvements."
        ),
        "guidelines": (
            "Follow best practices for project coordination and version control. "
            "Ensure that all agents have access to the latest guidelines."
        ),
        "references": "http://example.com/gista_workflow_coordinator_guidelines"
    }
