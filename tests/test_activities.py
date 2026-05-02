"""
Tests for the activities endpoint (GET /activities)
"""
import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""

    def test_get_all_activities_returns_200(self, client, clean_activities):
        """
        Test that GET /activities returns a 200 status code
        
        AAA Pattern:
        - Arrange: Test client is ready with clean activities data
        - Act: Make GET request to /activities
        - Assert: Response status is 200
        """
        # Arrange & Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200

    def test_get_all_activities_returns_json(self, client, clean_activities):
        """
        Test that GET /activities returns valid JSON
        
        AAA Pattern:
        - Arrange: Test client is ready with clean activities data
        - Act: Make GET request to /activities
        - Assert: Response can be parsed as JSON
        """
        # Arrange & Act
        response = client.get("/activities")
        
        # Assert
        assert response.headers["content-type"] == "application/json"
        data = response.json()
        assert isinstance(data, dict)

    def test_get_activities_returns_all_activities(self, client, clean_activities):
        """
        Test that GET /activities returns all activity records
        
        AAA Pattern:
        - Arrange: Test client is ready with 9 activities in clean state
        - Act: Make GET request to /activities
        - Assert: Response contains all 9 expected activities
        """
        # Arrange & Act
        response = client.get("/activities")
        data = response.json()
        
        # Assert
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Studio",
            "Theater Club",
            "Debate Team",
            "Science Club"
        ]
        assert len(data) == 9
        for activity_name in expected_activities:
            assert activity_name in data

    def test_activity_structure_is_correct(self, client, clean_activities):
        """
        Test that each activity has the required structure
        
        AAA Pattern:
        - Arrange: Test client is ready with clean activities data
        - Act: Make GET request to /activities and get first activity
        - Assert: Activity has all required fields with correct types
        """
        # Arrange & Act
        response = client.get("/activities")
        data = response.json()
        first_activity = data["Chess Club"]
        
        # Assert
        assert "description" in first_activity
        assert "schedule" in first_activity
        assert "max_participants" in first_activity
        assert "participants" in first_activity
        assert isinstance(first_activity["description"], str)
        assert isinstance(first_activity["schedule"], str)
        assert isinstance(first_activity["max_participants"], int)
        assert isinstance(first_activity["participants"], list)

    def test_activities_have_participants(self, client, clean_activities):
        """
        Test that activities have the expected participants
        
        AAA Pattern:
        - Arrange: Test client is ready with clean activities data
        - Act: Make GET request to /activities
        - Assert: Chess Club has michael and daniel as participants
        """
        # Arrange & Act
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        
        # Assert
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
        assert len(chess_club["participants"]) == 2
