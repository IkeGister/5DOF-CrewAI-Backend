import warnings
import os
from crewai import Crew
from agents.agents import create_content_agents, create_support_agents, create_travel_agents
from tasks.crewAI_tasks import create_content_tasks, customer_support_task, create_travel_tasks, test_travel_agent_task
from config.topics import get_topic, get_all_topics
from config.settings import VERBOSE_OUTPUT, validate_settings

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

if __name__ == "__main__":
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

    # Add this at the start of your main function or notebook cell
    check_environment()
