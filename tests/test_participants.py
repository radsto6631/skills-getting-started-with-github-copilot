"""
Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint.
"""

import pytest


class TestRemoveParticipant:
    """Tests for removing participants from activities."""

    def test_successful_participant_removal(self, client, sample_activity_name, existing_email):
        """
        Test that a participant can be successfully removed from an activity.
        
        Arrange: Set up test client with activity and existing participant
        Act: Make DELETE request to remove participant
        Assert: Status is 200 and response contains success message
        """
        # Arrange
        activity = sample_activity_name
        email = existing_email

        # Act
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_remove_nonexistent_participant_returns_400(self, client, sample_activity_name, sample_email):
        """
        Test that removing a non-existent participant returns a 400 error.
        
        Arrange: Set up test client with activity and non-existent email
        Act: Make DELETE request to remove participant
        Assert: Status is 400 and error message indicates participant not found
        """
        # Arrange
        activity = sample_activity_name
        email = sample_email

        # Act
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "not registered" in data["detail"].lower()

    def test_remove_from_nonexistent_activity_returns_404(self, client, sample_email):
        """
        Test that removing from a non-existent activity returns 404.
        
        Arrange: Set up test client with non-existent activity
        Act: Make DELETE request to remove participant
        Assert: Status is 404 and error message indicates activity not found
        """
        # Arrange
        activity = "Nonexistent Activity"
        email = sample_email

        # Act
        response = client.delete(
            f"/activities/{activity}/participants/{email}"
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_remove_participant_from_activity_list(self, client, sample_activity_name, existing_email):
        """
        Test that removing a participant deletes them from the activity's participant list.
        
        Arrange: Confirm participant is in activity
        Act: Remove the participant
        Assert: Participant no longer appears in the activity's participants list
        """
        # Arrange
        activity = sample_activity_name
        email = existing_email
        
        initial_response = client.get("/activities")
        assert email in initial_response.json()[activity]["participants"]

        # Act
        client.delete(f"/activities/{activity}/participants/{email}")
        updated_response = client.get("/activities")

        # Assert
        assert email not in updated_response.json()[activity]["participants"]

    def test_remove_participant_updates_availability(self, client, sample_activity_name, existing_email):
        """
        Test that removing a participant increases the available spots for the activity.
        
        Arrange: Get initial participant count
        Act: Remove a participant
        Assert: Participant count decreases by 1
        """
        # Arrange
        activity = sample_activity_name
        email = existing_email
        
        initial_response = client.get("/activities")
        initial_participants = len(initial_response.json()[activity]["participants"])

        # Act
        client.delete(f"/activities/{activity}/participants/{email}")
        updated_response = client.get("/activities")
        updated_participants = len(updated_response.json()[activity]["participants"])

        # Assert
        assert updated_participants == initial_participants - 1
