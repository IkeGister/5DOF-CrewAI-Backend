"""
Content Tools Module
===================

This module manages the creation and organization of tools for CrewAI agents.

Tool Assignment Hierarchy:
-------------------------

Tools in CrewAI can be assigned at two levels:

1. Agent Level:
   - Tools assigned directly to an agent are available for all tasks
   - The agent has discretionary use of these tools
   
2. Task Level:
   - Tools assigned to specific tasks override agent-level tools
   - When a task has assigned tools, the agent will ONLY use those tools
   - This provides precise control over tool usage for specific tasks

Visual Representation:
---------------------

                     Assigning Tools
                     
                    ┌──────────────┐
                    │    Tools     │
                    └──────┬───────┘
                           │
                 ┌────────┴────────┐
                 │                  │
        ┌────────┴───────┐    ┌────┴────┐
        │     Agent      │    │  Task   │
        │   (Default)    │    │(Override)│
        └────────────────┘    └─────────┘

Notes:
- Tools assigned to Agent: Available for all tasks (discretionary use)
- Tools assigned to Task: Exclusively used for that specific task
"""

from crewai import Task
from CrewAI.tools.content_gen_tools import (
    create_test_research_tools, 
    create_research_tools, 
    create_directory_tools
)
from CrewAI.tools.ticket_search_tool import TicketSearchTool
from CrewAI.tools.travel_guide_tool import TravelGuideTool


def create_content_tasks(planner, writer, editor):
    """
    Create and return the content creation tasks
    """
    plan = Task(
        description=(
            "1. Prioritize the latest trends, key players, "
                "and noteworthy news on {topic}.\n"
            "2. Identify the target audience, considering "
                "their interests and pain points.\n"
            "3. Develop a detailed content outline including "
                "an introduction, key points, and a call to action.\n"
            "4. Include SEO keywords and relevant data or sources."
        ),
        expected_output="A comprehensive content plan document "
            "with an outline, audience analysis, "
            "SEO keywords, and resources.",
        agent=planner,
    )

    write = Task(
        description=(
            "1. Use the content plan to craft a compelling "
                "blog post on {topic}.\n"
            "2. Incorporate SEO keywords naturally.\n"
            "3. Sections/Subtitles are properly named "
                "in an engaging manner.\n"
            "4. Ensure the post is structured with an "
                "engaging introduction, insightful body, "
                "and a summarizing conclusion.\n"
            "5. Proofread for grammatical errors and "
                "alignment with the brand's voice.\n"
        ),
        expected_output="A well-written blog post "
            "in markdown format, ready for publication, "
            "each section should have 2 or 3 paragraphs.",
        agent=writer,
    )

    edit = Task(
        description=("Proofread the given blog post for "
                     "grammatical errors and "
                     "alignment with the brand's voice."),
        expected_output="A well-written blog post in markdown format, "
                        "ready for publication, "
                        "each section should have 2 or 3 paragraphs.",
        agent=editor
    )

    return [plan, write, edit]


def customer_support_task(support_agent, qa_agent):
    """
    Create tasks for customer support workflow
    
    Args:
        support_agent: The customer support agent
        qa_agent: The quality assurance agent
        
    Returns:
        list: List of tasks for the support workflow
    """
    docs_scrape_tool = create_test_research_tools()[0]

    support_inquiry = Task(
        description=(
            "{customer} just reached out with a super important ask:\n"
            "{inquiry}\n\n"
            "{person} from {customer} is the one that reached out. "
            "Make sure to use everything you know "
            "to provide the best support possible."
            "You must strive to provide a complete "
            "and accurate response to the customer's inquiry."
        ),
        expected_output=(
            "A detailed, informative response to the "
            "customer's inquiry that addresses "
            "all aspects of their question.\n"
            "The response should include references "
            "to everything you used to find the answer, "
            "including external data or solutions. "
            "Ensure the answer is complete, "
            "leaving no questions unanswered, and maintain a helpful and friendly "
            "tone throughout."
        ),
        tools=[docs_scrape_tool],
        agent=support_agent
    )

    quality_review = Task(
        description=(
            "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
            "Ensure that the answer is comprehensive, accurate, and adheres to the "
            "high-quality standards expected for customer support.\n"
            "Verify that all parts of the customer's inquiry "
            "have been addressed "
            "thoroughly, with a helpful and friendly tone.\n"
            "Check for references and sources used to "
            "find the information, "
            "ensuring the response is well-supported and "
            "leaves no questions unanswered."
        ),
        expected_output=(
            "A final, detailed, and informative response "
            "ready to be sent to the customer.\n"
            "This response should fully address the "
            "customer's inquiry, incorporating all "
            "relevant feedback and improvements.\n"
            "Don't be too formal, we are a chill and cool company "
            "but maintain a professional and friendly tone throughout."
        ),
        agent=qa_agent
    )
    
    return [support_inquiry, quality_review]



def create_travel_tasks(travel_planner_consultant, travel_info_coordinator, inputs):
    """
    Create and return the travel-related tasks
    
    Args:
        travel_planner_consultant: The travel planner and consultant agent
        travel_info_coordinator: The travel information coordinator agent
        inputs: A dictionary containing travel data
        
    Returns:
        list: List of travel-related tasks
    """
    
    # Task 1: Gather Travel Information
    gather_info = Task(
        description=(
            "Gather all necessary travel information from the user:\n"
            "1. Full Name\n"
            "2. Email Address\n"
            "3. Traveling From\n"
            "4. Traveling To\n"
            "5. Travel Date\n"
            "6. Return Date (if applicable)\n"
            "7. Flight Class\n"
            "8. Luggage Number\n"
            "9. Travel Companions\n"
            "10. Companion Type\n"
            "11. Preferred Flight\n"
        ),
        expected_output="All necessary travel information collected from the user.",
        tools=[],
        agent=travel_planner_consultant,
        allow_delegation=False,
        verbose=True
    )

    # Task 2: Search for Tickets
    search_tickets = Task(
        description=(
            "Use the TicketSearchTool to find available tickets based on the gathered information.\n"
            "Ensure to check for the best options and provide a summary of the findings."
        ),
        expected_output="A list of available tickets based on the user's travel preferences.",
        tools=[TicketSearchTool()],
        agent=travel_planner_consultant,
        allow_delegation=False,
        verbose=True
    )

    # Task 3: Use Travel Guide Tool
    travel_guide = Task(
        description=(
            "Use the TravelGuideTool to gather information about the weather, accommodations, and attractions "
            "at the departure and destination locations."
        ),
        expected_output="Weather conditions, hotel options, and tourist attractions at the specified locations.",
        tools=[TravelGuideTool()],
        agent=travel_planner_consultant,
        allow_delegation=False,
        verbose=True
    )

    # Task 4: Summarize Travel Information
    summarize_travel_info = Task(
        description=(
            "Collate the information gathered from the ticket search and travel guide tasks.\n"
            "Present a comprehensive summary to the user, including:\n"
            "1. Available flight options\n"
            "2. Weather conditions at the departure and destination\n"
            "3. Hotel options and tourist attractions\n"
            "Ensure the summary is clear and allows the user to make an informed decision."
        ),
        expected_output="A comprehensive summary of travel options, weather, accommodations, and attractions.",
        agent=travel_info_coordinator,
        allow_delegation=False,
        verbose=True
    )

    return [gather_info, search_tickets, travel_guide, summarize_travel_info]

def test_travel_agent_task(travel_planner_consultant, travel_info_coordinator):
    """
    Test Travel Agent Task with default travel details
    
    Args:
        travel_planner_consultant: The travel planner and consultant agent
        travel_info_coordinator: The travel information coordinator agent
        
    Returns:
        list: List of tasks for the travel agent workflow
    """
    
    # Create an instance of TicketSearchTool
    ticket_search_tool = TicketSearchTool()

    # Default travel details
    travel_details = ticket_search_tool._get_travel_details(
        full_name="Jane Doe",
        email="jane.doe@example.com",
        traveling_from="San Francisco",
        traveling_to="Chicago",
        travel_date="2023-11-01",
        return_date="2023-11-05",
        flight_class="Business",
        luggage_number=1,
        travel_companions=0,
        companion_type=None,
        pet_type=None,
        preferred_flight=None,
        flexible_dates=False
    )

    # Task 1: Gather Travel Information (using the method to get details)
    gather_info = Task(
        description=(
            "Process the following travel details and provide a summary:\n"
            f"Full Name: {travel_details['full_name']}\n"
            f"Email: {travel_details['email']}\n"
            f"Traveling From: {travel_details['traveling_from']}\n"
            f"Traveling To: {travel_details['traveling_to']}\n"
            f"Travel Date: {travel_details['travel_date']}\n"
            f"Return Date: {travel_details['return_date']}\n"
            f"Flight Class: {travel_details['flight_class']}\n"
            f"Luggage Number: {travel_details['luggage_number']}\n"
            f"Travel Companions: {travel_details['travel_companions']}\n"
            f"Preferred Flight: {travel_details['preferred_flight']}\n"
        ),
        expected_output="A summary of travel options based on the provided details.",
        tools=[TicketSearchTool()],
        agent=travel_planner_consultant,
        allow_delegation=False,
        verbose=True
    )

    # Task 2: Summarize Travel Information
    summarize_travel_info = Task(
        description=(
            "Collate the information gathered from the ticket search and travel guide tasks.\n"
            "Present a comprehensive summary to the user, including:\n"
            "1. Available flight options\n"
            "2. Weather conditions at the departure and destination\n"
            "3. Hotel options and tourist attractions\n"
            "Ensure the summary is clear and allows the user to make an informed decision."
        ),
        expected_output="A comprehensive summary of travel options, weather, accommodations, and attractions.",
        tools=[TravelGuideTool()],
        agent=travel_info_coordinator,
        allow_delegation=False,
        verbose=True
    )

    return [gather_info, summarize_travel_info]