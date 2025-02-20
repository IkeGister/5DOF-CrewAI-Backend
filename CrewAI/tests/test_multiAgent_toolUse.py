import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.agents import create_support_agents
from main import create_support_crew

def display_result(result):
    """Display result in test environment"""
    if isinstance(result, list):
        result = '\n'.join(result)
    print(result)

def test_customer_support():
    """
    Test the customer support multi-agent system
    """
    print("\n=== Testing Customer Support Multi-Agent System ===")
    try:
        support_agent, qa_agent = create_support_agents(customer="Gister App")
        
        result = create_support_crew(
            inquiry=(
                "I need help with setting up a Crew "
                "and kicking it off, specifically "
                "how can I add memory to my crew? "
                "Can you provide guidance?"
            ),
            person="Ike",
            customer="Gister App"
        )
        display_result(result)
        print("✓ Customer support test completed successfully")
    except Exception as e:
        print(f"✗ Customer support test error: {str(e)}")

if __name__ == "__main__":
    test_customer_support()
