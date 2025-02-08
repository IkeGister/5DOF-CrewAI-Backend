from crewai_tools import BaseTool, SerperDevTool
from typing import List, Optional, Type
from pydantic.v1 import BaseModel, Field, EmailStr
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

print("Current Environment Variables:")
for key, value in os.environ.items():
    print(f"{key}: {value}")

class TicketSearchSchema(BaseModel):
    """Schema for the ticket search tool - defines all required and optional fields for ticket search"""
    full_name: str = Field(..., description="The full name of the traveler.")
    email: EmailStr = Field(..., description="The email address to send tickets to.")
    traveling_from: str = Field(..., description="The departure location.")
    traveling_to: str = Field(..., description="The destination location.")
    travel_date: str = Field(..., description="The date of travel in YYYY-MM-DD format.")
    return_date: Optional[str] = Field(None, description="The return date in YYYY-MM-DD format (optional).")
    flight_class: str = Field(..., description="The class of travel (e.g., economy, business).")
    luggage_number: int = Field(..., description="The number of luggage pieces.")
    travel_companions: int = Field(..., description="The number of travel companions.")
    companion_type: Optional[str] = Field(None, description="Type of travel companion (e.g., minor, pet).")
    pet_type: Optional[str] = Field(None, description="Type of pet if the companion is a pet.")
    preferred_flight: Optional[str] = Field(None, description="Preferred flight details or 'open' for an open search.")
    flexible_dates: Optional[bool] = Field(False, description="Indicates if the traveler is flexible with travel dates.")

    class Config:
        orm_mode = True

class TicketSearchTool(BaseTool):
    """
    A tool for searching flight tickets using the SerperDev API.
    Successfully handles direct ticket searches with detailed passenger and flight requirements.
    
    Note: While this tool works perfectly for direct ticket searches, any errors when used within
    a CrewAI agent system should be handled in the travel guide tool implementation.
    """
    name: str = "Ticket Search Tool"
    description: str = "Searches for tickets based on various travel details."
    args_schema: Type[BaseModel] = TicketSearchSchema
    search_tool: Optional[SerperDevTool] = None

    def __init__(self):
        super().__init__()
        self.search_tool = SerperDevTool()
        os.environ["SERPER_API_KEY"] = "5591e3125ff4adc849b11d93ef95a91bfb615972"

    def _run(self, **kwargs) -> List[str]:
        """
        Executes the ticket search with the provided parameters.
        
        Args:
            **kwargs: All ticket search parameters as defined in TicketSearchSchema
            
        Returns:
            List[str]: Formatted search results including passenger details and flight options
        """
        search_query = f"flights from {kwargs['traveling_from']} to {kwargs['traveling_to']} on {kwargs['travel_date']}"
        search_results = self.search_tool._run(search_query=search_query)
        
        return [
            f"Found tickets from {kwargs['traveling_from']} to {kwargs['traveling_to']} on {kwargs['travel_date']}:",
            f"Traveler: {kwargs['full_name']}, Email: {kwargs['email']}",
            f"Flight Class: {kwargs['flight_class']}, Luggage: {kwargs['luggage_number']}, Companions: {kwargs['travel_companions']}",
            f"Companion Type: {kwargs.get('companion_type')}, Pet Type: {kwargs.get('pet_type')}",
            f"Preferred Flight: {kwargs.get('preferred_flight', 'Open Search')}",
            "Search Results:",
            search_results
        ]

    def _get_travel_details(self, full_name: str, email: str, traveling_from: str, 
                             traveling_to: str, travel_date: str, return_date: Optional[str], 
                             flight_class: str, luggage_number: int, travel_companions: int, 
                             companion_type: Optional[str], pet_type: Optional[str], 
                             preferred_flight: Optional[str], flexible_dates: Optional[bool] = False) -> dict:
        """Returns the travel details as a dictionary."""
        travel_details = {
            "full_name": full_name,
            "email": email,
            "traveling_from": traveling_from,
            "traveling_to": traveling_to,
            "travel_date": travel_date,
            "return_date": return_date,
            "flight_class": flight_class,
            "luggage_number": luggage_number,
            "travel_companions": travel_companions,
            "companion_type": companion_type,
            "pet_type": pet_type,
            "preferred_flight": preferred_flight,
            "flexible_dates": flexible_dates
        }
        return travel_details 