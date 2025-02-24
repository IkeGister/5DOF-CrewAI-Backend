"""
Currently refactoring: Original implementation is commented out below.
New implementation focuses on content approval functionality.
"""

import warnings
import os
import sys
from crewai import Crew
from .config.settings import VERBOSE_OUTPUT, validate_settings
from .agents.gistaApp_agents.content_approval_team.content_approval_team import ContentApprovalTeam
from flask import Flask, request, jsonify

# Suppress warnings
warnings.filterwarnings('ignore')

def check_environment():
    """Check if required environment variables are set"""
    print(f"OpenAI API Key present: {'OPENAI_API_KEY' in os.environ}")
    if 'OPENAI_API_KEY' not in os.environ:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

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
        # Get crew, tasks and guidelines
        crew, read_task, guidelines = approval_team.start_podcast_production_flow(content_source)
        
        if crew and read_task and guidelines:
            # Execute the read guidelines task
            result = crew.kickoff(inputs={"guidelines": guidelines})
            
            return {
                "status": "guidelines_reviewed",
                "result": result,
                "message": "Guidelines have been reviewed and understood",
                "next_step": "content_validation"
            }
        else:
            return {
                "status": "error",
                "message": "Failed to prepare podcast production flow"
            }
            
    except Exception as e:
        print(f"Error in content approval: {str(e)}")
        return {
            "status": "error",
            "error_message": str(e),
            "error_type": type(e).__name__
        }

app = Flask(__name__)

@app.route('/api/content/approve', methods=['POST'])
def initiate_content_approval():
    try:
        # Get gist data from request
        data = request.get_json()  # Changed from request.json
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data received'}), 400
            
        gist_data = data.get('gistData', {})
        user_id = data.get('userId', '')
        gist_id = data.get('gistId', '')

        if not all([gist_data, user_id, gist_id]):
            return jsonify({
                'success': False,
                'error': 'Missing required data'
            }), 400

        # Initialize content approval team
        approval_team = ContentApprovalTeam(verbose=True)
        
        # Start the approval workflow
        result = approval_team.start_podcast_production_flow(
            content_source=gist_data['link']  # or other relevant field
        )

        return jsonify({
            'success': True,
            'message': 'Content approval workflow initiated',
            'data': result
        })

    except Exception as e:
        print(f"Error in content approval: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == "__main__":
    check_environment()
    
    # Normal flow
    content_source = "https://example.com/article"
    approval_result = create_content_approval_crew(content_source)
    print("Content Approval Result:", approval_result)

    app.run(host='0.0.0.0', port=5000)

"""
Original implementation below - currently being refactored
"""

# import warnings
# import os
# import sys
# from crewai import Crew
# from CrewAI.agents.agents import create_content_agents, create_support_agents, create_travel_agents
# from CrewAI.tasks.crewAI_tasks import create_content_tasks, customer_support_task, create_travel_tasks, test_travel_agent_task
# from CrewAI.config.topics import get_topic, get_all_topics
# from CrewAI.config.settings import VERBOSE_OUTPUT, validate_settings
# from CrewAI.agents.gistaApp_agents.gista_agents import create_gista_agents
# from CrewAI.tasks.gistaApp_tasks.gista_tasks import (
#     create_all_gista_tasks,
#     create_script_production_tasks,
#     create_voice_generation_tasks,
# )
# from CrewAI.agents.gistaApp_agents.content_approval_team.content_approval_team import ContentApprovalTeam
# from CrewAI.agents.gistaApp_agents.content_approval_team.run_content_approval_tests import run_content_approval_tests
#
# def create_content_crew(topic):
#     """
#     Create and run a crew for content creation
#     
#     Args:
#         topic (str): The topic to create content about
#     """
#     validate_settings()
#     planner, writer, editor = create_content_agents()
#     tasks = create_content_tasks(planner, writer, editor)
#     content_crew = Crew(
#         agents=[planner, writer, editor],
#         tasks=tasks,
#         verbose=VERBOSE_OUTPUT
#     )
#     return content_crew.kickoff(inputs={"topic": topic})
#
# def create_support_crew(inquiry, person, customer="Gister App"):
#     """
#     Create and run a crew for customer support
#     """
#     validate_settings()
#     support_agent, qa_agent = create_support_agents(customer=customer)
#     tasks = customer_support_task(
#         support_agent=support_agent,
#         qa_agent=qa_agent
#     )
#     support_crew = Crew(
#         agents=[support_agent, qa_agent],
#         tasks=tasks,
#         verbose=VERBOSE_OUTPUT,
#         memory=True
#     )
#     return support_crew.kickoff(inputs={
#         "inquiry": inquiry,
#         "person": person,
#         "customer": customer
#     })
#
# def create_travel_crew(inputs):
#     """Create and run a crew for travel planning"""
#     validate_settings()
#     travel_planner_consultant, travel_info_coordinator = create_travel_agents()
#     tasks = create_travel_tasks(travel_planner_consultant, travel_info_coordinator, inputs)
#     travel_crew = Crew(
#         agents=[travel_planner_consultant, travel_info_coordinator],
#         tasks=tasks,
#         verbose=VERBOSE_OUTPUT
#     )
#     return travel_crew.kickoff(inputs=inputs)
#
# def create_test_travel_crew():
#     """Create and run a test crew for travel planning"""
#     validate_settings()
#     travel_planner_consultant, travel_info_coordinator = create_travel_agents()
#     tasks = test_travel_agent_task(travel_planner_consultant, travel_info_coordinator)
#     test_travel_crew = Crew(
#         agents=[travel_planner_consultant, travel_info_coordinator],
#         tasks=tasks,
#         verbose=VERBOSE_OUTPUT
#     )
#     return test_travel_crew.kickoff(inputs={})
#
# def create_gista_crew(content_source):
#     """
#     Create and run a crew for podcast generation
#     """
#     validate_settings()
#     gista_agents = create_gista_agents()
#     tasks = create_all_gista_tasks(gista_agents)
#     gista_crew = Crew(
#         agents=[
#             gista_agents["content_assessment"]["content_validator"],
#             gista_agents["content_assessment"]["content_analyst"], 
#             gista_agents["content_assessment"]["technical_analyst"],
#             gista_agents["content_assessment"]["research_specialist"],
#             gista_agents["script_production"]["readout_script_writer"],
#             gista_agents["script_production"]["segment_script_alpha"],
#             gista_agents["script_production"]["segment_script_beta"],
#             gista_agents["script_production"]["segment_script_gamma"],
#             gista_agents["script_production"]["segment_script_omega"],
#             gista_agents["script_production"]["transcript_generator"],
#             gista_agents["voice_generation"]["segment_voice_alpha"],
#             gista_agents["voice_generation"]["segment_voice_beta"],
#             gista_agents["voice_generation"]["segment_voice_gamma"],
#             gista_agents["voice_generation"]["segment_voice_omega"]
#         ],
#         tasks=tasks,
#         verbose=VERBOSE_OUTPUT,
#         memory=True
#     )
#     return gista_crew.kickoff(inputs={"content_source": content_source})
#
# def create_gista_pipeline(content_source):
#     """Create and run a pipeline of crews for podcast generation"""
#     gista_agents = create_gista_agents()
#     
#     content_assessment_crew = Crew(
#         agents=[agent for agent in gista_agents["content_assessment"].values()],
#         tasks=create_all_gista_tasks(gista_agents)[:9],
#         verbose=VERBOSE_OUTPUT,
#         memory=True
#     )
#     
#     script_crew = Crew(
#         agents=[agent for agent in gista_agents["script_production"].values()],
#         tasks=create_script_production_tasks(gista_agents["script_production"]),
#         verbose=VERBOSE_OUTPUT,
#         memory=True
#     )
#     
#     voice_crew = Crew(
#         agents=[agent for agent in gista_agents["voice_generation"].values()],
#         tasks=create_voice_generation_tasks(
#             voice_agents=gista_agents["voice_generation"],
#             script_agents=gista_agents["script_production"]
#         ),
#         verbose=VERBOSE_OUTPUT,
#         memory=True
#     )
#     
#     try:
#         content_result = content_assessment_crew.kickoff(
#             inputs={"content_source": content_source}
#         )
#         
#         if isinstance(content_result, dict) and content_result.get("content_status") == "CLEARED":
#             script_result = script_crew.kickoff(
#                 inputs={"content_analysis": content_result}
#             )
#             
#             voice_result = voice_crew.kickoff(
#                 inputs={"script_data": script_result}
#             )
#             
#             return {
#                 "status": "completed",
#                 "content_analysis": content_result,
#                 "script_generation": script_result,
#                 "voice_generation": voice_result
#             }
#         else:
#             return {
#                 "status": "content_rejected",
#                 "details": content_result
#             }
#             
#     except Exception as e:
#         print(f"Error in pipeline: {str(e)}")
#         raise
#
# if __name__ == "__main__":
#     check_environment()
#     
#     # Example usage for content creation
#     topic = get_topic("technology")
#     content_result = create_content_crew(topic)
#     print("Content Creation Result:", content_result)
#     
#     # Example usage for support
#     support_result = create_support_crew(
#         inquiry="I need help with setting up a Crew and kicking it off...",
#         person="Ike",
#         customer="Gister App"
#     )
#     print("Support Result:", support_result)
#
#     # Example usage for travel planning
#     travel_result = create_travel_crew(inputs={})
#     print("Travel Planning Result:", travel_result)
#
#     # Example usage for testing travel crew
#     test_travel_result = create_test_travel_crew()
#     print("Test Travel Planning Result:", test_travel_result)
#
#     # Example usage for Gista podcast generation
#     content_source = "https://example.com/article"
#     
#     # Using single crew
#     podcast_result = create_gista_crew(content_source)
#     print("Podcast Generation Result:", podcast_result)
#     
#     # Or using pipeline of crews
#     pipeline_result = create_gista_pipeline(content_source)
#     print("Pipeline Generation Result:", pipeline_result)
#
#     # Example usage for content approval
#     approval_result = create_content_approval_crew(content_source)
#     print("Content Approval Result:", approval_result)
#     
#     if "--test" in sys.argv:
#         sys.exit(run_approval_tests())
