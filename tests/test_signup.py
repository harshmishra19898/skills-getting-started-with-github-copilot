"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup)
"""
import pytest


class TestSignup:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""

    def test_signup_new_participant_returns_200(self, client, clean_activities):
        """
        Test that signing up a new participant returns a 200 status code
        
        AAA Pattern:
        - Arrange: Test client is ready, new email not in Chess Club
        - Act: Make POST request to sign up new@mergington.edu for Chess Club
        - Assert: Response status is 200
        """
        # Arrange
        activity = "Chess Club"
        email = "new@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200

    def test_signup_adds_participant_to_list(self, client, clean_activities):
        """
        Test that signing up a participant adds them to the activity's participant list
        
        AAA Pattern:
        - Arrange: Test client is ready, new email not in Chess Club
        - Act: Sign up new@mergington.edu for Chess Club
        - Assert: Participant is now in Chess Club's participants list
        """
        # Arrange
        activity = "Chess Club"
        email = "new@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        # Verify participant was added by fetching activities
        activities_response = client.get("/activities")
        data = activities_response.json()
        assert email in data[activity]["participants"]

    def test_signup_returns_success_message(self, client, clean_activities):
        """
        Test that signup returns a success message with the email and activity name
        
        AAA Pattern:
        - Arrange: Test client is ready, new email not in Chess Club
        - Act: Make POST request to sign up new@mergington.edu
        - Assert: Response contains a success message
        """
        # Arrange
        activity = "Chess Club"
        email = "new@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_nonexistent_activity_returns_404(self, client, clean_activities):
        """
        Test that signing up for a non-existent activity returns 404
        
        AAA Pattern:
        - Arrange: Test client is ready, "Fake Club" doesn't exist
        - Act: Make POST request to sign up for non-existent activity
        - Assert: Response status is 404 with appropriate error message
        """
        # Arrange
        activity = "Fake Club"
        email = "test@mergington.edu"
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_already_registered_returns_400(self, client, clean_activities):
        """
        Test that signing up an already-registered participant returns 400
        
        AAA Pattern:
        - Arrange: Test client is ready, michael@mergington.edu is already in Chess Club
        - Act: Try to sign up michael@mergington.edu again for Chess Club
        - Assert: Response status is 400 with appropriate error message
        """
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"  # Already registered in Chess Club
        
        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_same_email_different_activities(self, client, clean_activities):
        """
        Test that the same email can sign up for multiple different activities
        
        AAA Pattern:
        - Arrange: Test client is ready, email not in Programming Class or Gym Class
        - Act: Sign up same email for two different activities
        - Assert: Both signups succeed and participant appears in both activities
        """
        # Arrange
        email = "multi@mergington.edu"
        activity1 = "Programming Class"
        activity2 = "Gym Class"
        
        # Act
        response1 = client.post(
            f"/activities/{activity1}/signup",
            params={"email": email}
        )
        response2 = client.post(
            f"/activities/{activity2}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        # Verify both signups were recorded
        activities_response = client.get("/activities")
        data = activities_response.json()
        assert email in data[activity1]["participants"]
        assert email in data[activity2]["participants"]
