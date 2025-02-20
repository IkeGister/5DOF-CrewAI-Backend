"""
Test script to verify imports and basic initialization
"""
try:
    print("Testing imports...")
    from src.CrewAI.agents.gistaApp_agents.content_approval_team.content_approval_team import ContentApprovalTeam
    from src.CrewAI.agents.gistaApp_agents.content_approval_team.content_approval_agents import create_content_validator_agent
    from src.CrewAI.agents.gistaApp_agents.content_approval_team.content_approval_tools import get_all_content_approval_tools
    from src.CrewAI.config.settings import VERBOSE_OUTPUT, validate_settings

    print("\nTesting initialization...")
    # Try to create a team
    team = ContentApprovalTeam(verbose=True)
    
    print("\nTesting tool creation...")
    # Try to get tools
    tools = get_all_content_approval_tools()
    
    print("\nTesting agent creation...")
    # Try to create an agent
    agent = create_content_validator_agent(tools=tools)
    
    print("\nAll basic components initialized successfully!")

except Exception as e:
    print(f"\nError occurred: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    raise 