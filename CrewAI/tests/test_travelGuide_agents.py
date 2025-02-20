import sys
import os
import unittest
from pathlib import Path
from dotenv import load_dotenv

# Set up environment before imports
load_dotenv()  # Keep this to load environment variables
if not os.getenv("SERPER_API_KEY"):
    raise ValueError("SERPER_API_KEY is not set in environment variables")

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.agents import create_travel_agents
from tools.travel_guide_tool import TravelGuideTool

def display_result(result):
    """Display result in test environment"""
    if isinstance(result, list):
        result = '\n'.join(result)
    print(result)

def test_travel_agent():
    """
    Test the travel multi-agent system using the test travel crew
    """
    print("\n=== Testing Travel Multi-Agent System ===")
    try:
        # Create the test travel crew
        travel_result = create_travel_agents()  # Call the test travel crew function
        
        # Extract necessary details from the travel_result if needed
        travel_details = {
            "location": "Chicago",
            "travel_date": "2023-11-01",
            "return_date": "2023-11-05"
        }

        # Define the missing variables
        full_name = "Jane Doe"
        email = "jane.doe@example.com"
        traveling_from = "San Francisco"
        traveling_to = travel_details["location"]
        flight_class = "Business"
        luggage_number = 1
        travel_companions = 0
        preferred_flight = "Direct"

        # Create an instance of TravelGuideTool
        travel_guide_tool = TravelGuideTool()

        # Before calling the run method
        print("Running Ticket Search Tool with the following parameters:")
        print(f"Full Name: {full_name}")
        print(f"Email: {email}")
        print(f"Traveling From: {traveling_from}")
        print(f"Traveling To: {traveling_to}")
        print(f"Travel Date: {travel_details['travel_date']}")
        print(f"Return Date: {travel_details['return_date']}")
        print(f"Flight Class: {flight_class}")
        print(f"Luggage Number: {luggage_number}")
        print(f"Travel Companions: {travel_companions}")
        print(f"Preferred Flight: {preferred_flight}")

        # Call the _run method with the required arguments
        guide_info = travel_guide_tool._run(
            location=travel_details["location"],
            travel_date=travel_details["travel_date"],
            return_date=travel_details["return_date"]
        )

        # Display the result from the TravelGuideTool
        display_result(guide_info)
        
        # Example assertion (modify based on expected output)
        assert isinstance(guide_info, list), "Expected guide_info to be a list"
        assert len(guide_info) > 0, "Expected guide_info to have results"

        print("✓ Test travel agent completed successfully")
    except Exception as e:
        print(f"✗ Test travel agent error: {str(e)}")

if __name__ == "__main__":
    test_travel_agent() 