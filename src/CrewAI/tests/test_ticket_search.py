import unittest
import os
from ..tools.ticket_search_tool import TicketSearchTool

class TestTicketSearch(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test"""
        self.ticket_search_tool = TicketSearchTool()
        # Ensure SERPER_API_KEY is set
        if not os.getenv("SERPER_API_KEY"):
            os.environ["SERPER_API_KEY"] = "5591e3125ff4adc849b11d93ef95a91bfb615972"

    def test_ticket_search(self):
        """Test basic ticket search functionality"""
        results = self.ticket_search_tool.run(
            full_name="John Doe",
            email="john.doe@example.com",
            traveling_from="Los Angeles",
            traveling_to="New York",
            travel_date="2023-10-15",
            return_date="2023-10-20",
            flight_class="Economy",
            luggage_number=2,
            travel_companions=1,
            companion_type="Pet",
            pet_type="Dog",
            preferred_flight="Direct"
        )
        
        # Verify results structure
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) > 0)
        
        # Verify required information is present
        result_text = '\n'.join(results)
        required_info = [
            "Los Angeles",
            "New York",
            "2023-10-15",
            "John Doe",
            "john.doe@example.com",
            "Economy",
            "Pet",
            "Dog"
        ]
        
        for info in required_info:
            self.assertIn(info, result_text)

    def test_travel_details_method(self):
        """Test the _get_travel_details helper method"""
        details = self.ticket_search_tool._get_travel_details(
            full_name="Jane Smith",
            email="jane.smith@example.com",
            traveling_from="San Francisco",
            traveling_to="Chicago",
            travel_date="2023-11-01",
            return_date="2023-11-05",
            flight_class="Business",
            luggage_number=1,
            travel_companions=0,
            companion_type=None,
            pet_type=None,
            preferred_flight="Any",
            flexible_dates=True
        )
        
        # Verify all fields are present
        expected_fields = [
            "full_name",
            "email",
            "traveling_from",
            "traveling_to",
            "travel_date",
            "return_date",
            "flight_class",
            "luggage_number",
            "travel_companions",
            "companion_type",
            "pet_type",
            "preferred_flight",
            "flexible_dates"
        ]
        
        for field in expected_fields:
            self.assertIn(field, details)
        
        # Verify specific values
        self.assertEqual(details["full_name"], "Jane Smith")
        self.assertEqual(details["email"], "jane.smith@example.com")
        self.assertEqual(details["luggage_number"], 1)
        self.assertTrue(details["flexible_dates"])

    def test_invalid_email(self):
        """Test handling of invalid email"""
        with self.assertRaises(ValueError):
            self.ticket_search_tool.run(
                full_name="Test User",
                email="invalid-email",  # Invalid email format
                traveling_from="Boston",
                traveling_to="Miami",
                travel_date="2023-12-01",
                flight_class="Economy",
                luggage_number=1,
                travel_companions=0
            )

if __name__ == '__main__':
    unittest.main(verbosity=2) 