"""
Content Analysis Agents
======================

Specialized agents focused on content analysis and assessment tasks.
These agents work in conjunction with the main Gista system while providing
detailed content analysis capabilities.
"""

from crewai import Agent

def create_content_analysis_agents():
    """Create and return specialized content analysis agents"""
    
    content_structure_analyst = Agent(
        role="Content Structure Analyst",
        goal="Analyze and map content structure and flow",
        backstory=(
            "Specialist in breaking down complex content into logical segments "
            "and identifying natural transition points. Expert in content "
            "organization and narrative flow optimization."
        ),
        allow_delegation=False,
        verbose=True
    )

    technical_content_specialist = Agent(
        role="Technical Content Specialist",
        goal="Analyze and simplify technical content",
        backstory=(
            "Expert in translating complex technical concepts into "
            "accessible content. Specializes in maintaining accuracy while "
            "ensuring content remains engaging for general audiences."
        ),
        allow_delegation=False,
        verbose=True
    )

    research_coordinator = Agent(
        role="Research Coordinator",
        goal="Coordinate and conduct in-depth content research",
        backstory=(
            "Experienced research professional skilled in gathering supporting "
            "information, fact-checking, and providing contextual background "
            "for content enhancement."
        ),
        allow_delegation=False,
        verbose=True
    )

    content_optimization_analyst = Agent(
        role="Content Optimization Analyst",
        goal="Optimize content for audio format and engagement",
        backstory=(
            "Specialist in adapting written content for audio presentation. "
            "Expert in identifying areas needing clarification, simplification, "
            "or enhancement for better audience engagement."
        ),
        allow_delegation=False,
        verbose=True
    )

    agents_dict = {
        "content_structure_analyst": content_structure_analyst,
        "technical_content_specialist": technical_content_specialist,
        "research_coordinator": research_coordinator,
        "content_optimization_analyst": content_optimization_analyst
    }

    return agents_dict
