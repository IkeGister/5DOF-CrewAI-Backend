import warnings
import os
import sys
from crewai import Crew
from CrewAI.agents.agents import create_content_agents, create_support_agents, create_travel_agents
from CrewAI.tasks.crewAI_tasks import create_content_tasks, customer_support_task, create_travel_tasks, test_travel_agent_task
from CrewAI.config.topics import get_topic, get_all_topics
from CrewAI.config.settings import VERBOSE_OUTPUT, validate_settings
from CrewAI.agents.gistaApp_agents.gista_agents import create_gista_agents
from CrewAI.tasks.gistaApp_tasks.gista_tasks import (
    create_all_gista_tasks,
    create_script_production_tasks,
    create_voice_generation_tasks,
)
from CrewAI.agents.gistaApp_agents.content_approval_team.content_approval_team import ContentApprovalTeam
from CrewAI.agents.gistaApp_agents.content_approval_team.run_content_approval_tests import run_content_approval_tests

# Suppress warnings
warnings.filterwarnings('ignore')

def check_environment():
    print(f"OpenAI API Key present: {'OPENAI_API_KEY' in os.environ}")
    if 'OPENAI_API_KEY' not in os.environ:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

def create_content_crew(topic):
    """
    Create and run a crew for content creation
    
    Args:
        topic (str): The topic to create content about
    """
    # Validate settings before proceeding
    validate_settings()
    
    # 1. Create agents
    planner, writer, editor = create_content_agents()
    
    # 2. Create tasks with the agents
    tasks = create_content_tasks(planner, writer, editor)
    
    # 3. Create and run crew
    content_crew = Crew(
        agents=[planner, writer, editor],
        tasks=tasks,
        verbose=VERBOSE_OUTPUT
    )
    
    # 4. Execute with topic input
    return content_crew.kickoff(inputs={"topic": topic})

def create_support_crew(inquiry, person, customer="Gister App"):
    """
    Create and run a crew for customer support
    
    Args:
        inquiry (str): The customer inquiry
        person (str): The person making the inquiry
        customer (str): The customer company name
    """
    # Validate settings before proceeding
    validate_settings()
    
    print("Starting support crew creation...")  # Debug print
    
    # 1. Create agents
    support_agent, qa_agent = create_support_agents(customer=customer)
    print("Agents created successfully")  # Debug print
    
    # 2. Create tasks with agents and tools
    tasks = customer_support_task(
        support_agent=support_agent,
        qa_agent=qa_agent
    )  # Returns list of [support_inquiry, quality_review]
    print("Tasks created successfully")  # Debug print
    
    # 3. Create and run crew
    support_crew = Crew(
        agents=[support_agent, qa_agent],
        tasks=tasks,  # Pass the list of tasks directly
        verbose=VERBOSE_OUTPUT,
        memory=True  # Support crew needs memory for context
    )
    
    # 4. Execute with inquiry inputs
    return support_crew.kickoff(inputs={
        "inquiry": inquiry,
        "person": person,
        "customer": customer
    })

def create_travel_crew(inputs):
    """
    Create and run a crew for travel planning
    """
    # Validate settings before proceeding
    validate_settings()
    
    # 1. Create agents
    travel_planner_consultant, travel_info_coordinator = create_travel_agents()
    
    # 2. Create tasks with the agents and inputs
    tasks = create_travel_tasks(travel_planner_consultant, travel_info_coordinator, inputs)
    
    # 3. Create and run crew
    travel_crew = Crew(
        agents=[travel_planner_consultant, travel_info_coordinator],
        tasks=tasks,
        verbose=VERBOSE_OUTPUT
    )
    
    # 4. Execute with travel inputs
    return travel_crew.kickoff(inputs=inputs)  # Pass the inputs to the kickoff

def create_test_travel_crew():
    """
    Create and run a test crew for travel planning
    """
    # Validate settings before proceeding
    validate_settings()
    
    # Create agents for testing
    travel_planner_consultant, travel_info_coordinator = create_travel_agents()
    
    # Create the test travel task
    tasks = test_travel_agent_task(travel_planner_consultant, travel_info_coordinator)
    
    # Create and run crew
    test_travel_crew = Crew(
        agents=[travel_planner_consultant, travel_info_coordinator],
        tasks=tasks,
        verbose=VERBOSE_OUTPUT
    )
    
    # Execute the test crew
    return test_travel_crew.kickoff(inputs={})  # No specific inputs needed for the test

def create_gista_crew(content_source):
    """
    Create and run a crew for podcast generation
    
    Args:
        content_source (str): URL or file path to source content
        
    Returns:
        dict: Results from the podcast generation process
    """
    # Validate settings
    validate_settings()
    
    # Create all agents
    gista_agents = create_gista_agents()
    
    # Create all tasks with agents
    tasks = create_all_gista_tasks(gista_agents)
    
    # Create main podcast generation crew
    gista_crew = Crew(
        agents=[
            # Content Assessment Department
            gista_agents["content_assessment"]["content_validator"],
            gista_agents["content_assessment"]["content_analyst"], 
            gista_agents["content_assessment"]["technical_analyst"],
            gista_agents["content_assessment"]["research_specialist"],
            
            # Script Production Department
            gista_agents["script_production"]["readout_script_writer"],
            gista_agents["script_production"]["segment_script_alpha"],
            gista_agents["script_production"]["segment_script_beta"],
            gista_agents["script_production"]["segment_script_gamma"],
            gista_agents["script_production"]["segment_script_omega"],
            gista_agents["script_production"]["transcript_generator"],
            
            # Voice Generation Department
            gista_agents["voice_generation"]["segment_voice_alpha"],
            gista_agents["voice_generation"]["segment_voice_beta"],
            gista_agents["voice_generation"]["segment_voice_gamma"],
            gista_agents["voice_generation"]["segment_voice_omega"]
        ],
        tasks=tasks,
        verbose=VERBOSE_OUTPUT,
        memory=True  # Keep memory enabled for context across tasks
    )
    
    # Execute with content source input
    return gista_crew.kickoff(inputs={"content_source": content_source})

# Alternative: Create separate crews for each major phase
def create_gista_pipeline(content_source):
    """
    Create and run a pipeline of crews for podcast generation
    
    Args:
        content_source (str): URL or file path to source content
    """
    # Get all agents
    gista_agents = create_gista_agents()
    
    # 1. Content Assessment Crew
    content_assessment_crew = Crew(
        agents=[agent for agent in gista_agents["content_assessment"].values()],
        tasks=create_all_gista_tasks(gista_agents)[:9],  # First 9 tasks are content assessment
        verbose=VERBOSE_OUTPUT,
        memory=True
    )
    
    # 2. Script Generation Crew
    script_crew = Crew(
        agents=[agent for agent in gista_agents["script_production"].values()],
        tasks=create_script_production_tasks(gista_agents["script_production"]),
        verbose=VERBOSE_OUTPUT,
        memory=True
    )
    
    # 3. Voice Generation Crew
    voice_crew = Crew(
        agents=[agent for agent in gista_agents["voice_generation"].values()],
        tasks=create_voice_generation_tasks(
            voice_agents=gista_agents["voice_generation"],
            script_agents=gista_agents["script_production"]
        ),
        verbose=VERBOSE_OUTPUT,
        memory=True
    )
    
    # Execute pipeline
    try:
        # Start with content assessment
        content_result = content_assessment_crew.kickoff(
            inputs={"content_source": content_source}
        )
        
        if isinstance(content_result, dict) and content_result.get("content_status") == "CLEARED":
            # Generate scripts
            script_result = script_crew.kickoff(
                inputs={"content_analysis": content_result}
            )
            
            # Generate voice content
            voice_result = voice_crew.kickoff(
                inputs={"script_data": script_result}
            )
            
            return {
                "status": "completed",
                "content_analysis": content_result,
                "script_generation": script_result,
                "voice_generation": voice_result
            }
        else:
            return {
                "status": "content_rejected",
                "details": content_result
            }
            
    except Exception as e:
        print(f"Error in pipeline: {str(e)}")
        raise

def create_content_approval_crew(content_source: str):
    """
    Create and run a crew for content approval
    
    Args:
        content_source (str): URL, PDF path, or DOCX path to source content
        
    Returns:
        dict: Results from the content approval process
    """
    # Validate settings
    validate_settings()
    
    # Create content approval team
    approval_team = ContentApprovalTeam(verbose=bool(VERBOSE_OUTPUT))
    
    try:
        # Process the content
        result = approval_team.process_content(content_source)
        return result
    except Exception as e:
        print(f"Error in content approval: {str(e)}")
        return {
            "status": "error",
            "error_message": str(e),
            "error_type": type(e).__name__
        }

def run_approval_tests():
    """Run the content approval test suite"""
    print("\nRunning Content Approval Tests...")
    print("=" * 50)
    
    try:
        # Run all test categories
        test_result = run_content_approval_tests(verbose=bool(VERBOSE_OUTPUT))
        return test_result
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        return 1

if __name__ == "__main__":
    # Add this at the start
    check_environment()

    # Example usage for content creation
    topic = get_topic("technology")
    content_result = create_content_crew(topic)
    print("Content Creation Result:", content_result)
    
    # Example usage for support
    support_result = create_support_crew(
        inquiry=(
            "I need help with setting up a Crew "
            "and kicking it off, specifically "
            "how can I add memory to my crew? "
            "Can you provide guidance?"
        ),
        person="Ike",
        customer="Gister App"
    )
    print("Support Result:", support_result)

    # Example usage for travel planning
    travel_result = create_travel_crew(inputs={})
    print("Travel Planning Result:", travel_result)

    # Example usage for testing travel crew
    test_travel_result = create_test_travel_crew()
    print("Test Travel Planning Result:", test_travel_result)

    # Example usage for Gista podcast generation
    content_source = "https://example.com/article"
    
    # Using single crew
    podcast_result = create_gista_crew(content_source)
    print("Podcast Generation Result:", podcast_result)
    
    # Or using pipeline of crews
    pipeline_result = create_gista_pipeline(content_source)
    print("Pipeline Generation Result:", pipeline_result)

    # Example usage for content approval
    approval_result = create_content_approval_crew(content_source)
    print("Content Approval Result:", approval_result)
    
    # Run content approval tests
    if "--test" in sys.argv:
        sys.exit(run_approval_tests())
