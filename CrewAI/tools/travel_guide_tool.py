import os
from crewai_tools import BaseTool, SerperDevTool
from pydantic.v1 import BaseModel, Field  # Change to v1 explicitly
from typing import List, Optional, Type

class TravelGuideSchema(BaseModel):
    """Schema for the travel guide tool - defines required and optional fields"""
    location: str = Field(..., description="The location to search for accommodations and attractions.")
    travel_date: str = Field(..., description="The date of travel in YYYY-MM-DD format.")
    return_date: Optional[str] = Field(None, description="The return date in YYYY-MM-DD format (optional).")

    class Config:
        orm_mode = True  # Add this for v1 compatibility

class TravelGuideTool(BaseTool):
    name: str = "Travel Guide Tool"
    description: str = "Provides information on weather, accommodations, and attractions."
    args_schema: Type[BaseModel] = TravelGuideSchema
    search_tool: Optional[SerperDevTool] = None  # Declare search_tool as class variable

    def __init__(self):
        super().__init__(
            name=self.name,
            description=self.description
        )
        self.search_tool = SerperDevTool()
        if not os.getenv("SERPER_API_KEY"):
            os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY", "your-default-key")

    def _run(self, **kwargs) -> List[str]:
        if not self.search_tool:
            self.search_tool = SerperDevTool()
        
        location = kwargs['location']
        travel_date = kwargs['travel_date']
        
        weather_results = self.search_tool._run(
            search_query=f"weather in {location} on {travel_date}")
        
        hotel_results = self.search_tool._run(
            search_query=f"hotels in {location} on {travel_date}")
        
        attractions_results = self.search_tool._run(
            search_query=f"tourist attractions in {location}")

        return [
            f"Weather in {location} on {travel_date}: {weather_results}",
            f"Hotels in {location}: {hotel_results}",
            f"Tourist Attractions in {location}: {attractions_results}"
        ]

    def test(self):
        try:
            # Test the tool
            self._run(location="New York", travel_date="2024-05-01")
            print("✓ Test travel agent passed")
        except Exception as e:
            print(f"✗ Test travel agent error: {str(e)}")
            import traceback
            traceback.print_exc() 