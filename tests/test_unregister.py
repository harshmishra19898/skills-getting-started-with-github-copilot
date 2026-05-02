"""
Tests for the unregister endpoint (DELETE /activities/{activity_name}/unregister)
"""
import pytest


class TestUnregister:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint"""

    def test_unregister_existing_participant_returns_200(self, client, clean_activities):
        """
        Test that unregistering an existing participant returns 200
        
        AAA Pattern:
        - Arrange: Test client is ready, michael@mergington.edu is in Chess Club
        - Act: Make DELETE request to unregister michael@mergington.edu from Chess Club
        - Assert: Response status is 200
        """
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200

    def test_unregister_removes_participant_from_list(self, client, clean_activities):
        """
        Test that unregistering a participant removes them from the activity's list
        
        AAA Pattern:
        - Arrange: Test client is ready, michael@mergington.edu is in Chess Club
        - Act: Unregister michael@mergington.edu from Chess Club
        - Assert: Participant is no longer in Chess Club's participants list
        """
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        # Verify participant was removed
        activities_response = client.get("/activities")
        data = activities_response.json()
        assert email not in data[activity]["participants"]

    def test_unregister_returns_success_message(self, client, clean_activities):
        """
        Test that unregister returns a success message with email and activity name
        
        AAA Pattern:
        - Arrange: Test client is ready, michael@mergington.edu is in Chess Club
        - Act: Make DELETE request to unregister
        - Assert: Response contains a success message
        """
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        data = response.json()
        
        # Assert
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_unregister_nonexistent_activity_returns_404(self, client, clean_activities):
        """
        Test that unregistering from non-existent activity returns 404
        
        AAA Pattern:
        - Arrange: Test client is ready, "Fake Club" doesn't exist
        - Act: Make DELETE request to unregister from non-existent activity
        - Assert: Response status is 404 with appropriate error message
        """
        # Arrange
        activity = "Fake Club"
        email = "test@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_not_signed_up_returns_400(self, client, clean_activities):
        """
        Test that unregistering someone not signed up returns 400
        
        AAA Pattern:
        - Arrange: Test client is ready, nothere@mergington.edu is not in Chess Club
        - Act: Try to unregister nothere@mergington.edu from Chess Club
        - Assert: Response status is 400 with appropriate error message
        """
        # Arrange
        activity = "Chess Club"
        email = "nothere@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_then_signup_again(self, client, clean_activities):
        """
        Test that after unregistering, a participant can sign up again
        
        AAA Pattern:
        - Arrange: Test client is ready, michael@mergington.edu is in Chess Club
        - Act: Unregister michael, then sign up again
        - Assert: Both operations succeed, participant is registered after signup
        """
        # Arrange
        activity = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act - Unregister
        unregister_response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email}
        )
        
        # Act - Sign up again
        signup_response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert unregister_response.status_code == 200
        assert signup_response.status_code == 200
        
        # Verify participant is back in list
        activities_response = client.get("/activities")
        data = activities_response.json()
        assert email in data[activity]["participants"]

    def test_unregister_one_participant_keeps_others(self, client, clean_activities):
        """
        Test that unregistering one participant doesn't affect others in same activity
        
        AAA Pattern:
        - Arrange: Test client is ready, Chess Club has michael and daniel
        - Act: Unregister michael@mergington.edu from Chess Club
        - Assert: michael is removed but daniel remains
        """
        # Arrange
        activity = "Chess Club"
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"
        
        # Act
        response = client.delete(
            f"/activities/{activity}/unregister",
            params={"email": email_to_remove}
        )
        
        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        data = activities_response.json()
        assert email_to_remove not in data[activity]["participants"]
        assert email_to_keep in data[activity]["participants"]
