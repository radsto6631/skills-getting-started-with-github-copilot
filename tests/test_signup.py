"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


class TestSignupEndpoint:
    """Tests for signing up students to activities."""

    def test_successful_signup(self, client, sample_activity_name, sample_email):
        """
        Test that a student can successfully sign up for an activity.
        
        Arrange: Set up test client with activity name and student email
        Act: Make POST request to signup endpoint
        Assert: Status is 200 and response contains success message
        """
        # Arrange
        activity = sample_activity_name
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity in data["message"]

    def test_signup_prevents_duplicate_registration(
        self, client, sample_activity_name, existing_email
    ):
        """
        Test that a student cannot sign up twice for the same activity.
        
        Arrange: Use an email already registered for the activity
        Act: Make POST request to signup endpoint with duplicate email
        Assert: Status is 400 and error message indicates student already signed up
        """
        # Arrange
        activity = sample_activity_name
        email = existing_email

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_for_nonexistent_activity_returns_404(
        self, client, sample_email
    ):
        """
        Test that signing up for a non-existent activity returns 404.
        
        Arrange: Set up test client with invalid activity name
        Act: Make POST request to signup endpoint with non-existent activity
        Assert: Status is 404 and error message indicates activity not found
        """
        # Arrange
        activity = "Nonexistent Activity"
        email = sample_email

        # Act
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_adds_participant_to_activity(self, client, sample_activity_name, sample_email):
        """
        Test that signing up adds the participant to the activity's participant list.
        
        Arrange: Set up test client
        Act: Sign up a student, then fetch activities
        Assert: New participant appears in the activity's participants list
        """
        # Arrange
        activity = sample_activity_name
        email = sample_email

        # Act
        client.post(f"/activities/{activity}/signup", params={"email": email})
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert email in activities[activity]["participants"]

    def test_signup_updates_availability(self, client, sample_activity_name, sample_email):
        """
        Test that signing up decreases the available spots for the activity.
        
        Arrange: Get initial participant count
        Act: Sign up a student
        Assert: Participant count increases by 1
        """
        # Arrange
        activity = sample_activity_name
        email = sample_email
        
        initial_response = client.get("/activities")
        initial_participants = len(initial_response.json()[activity]["participants"])

        # Act
        client.post(f"/activities/{activity}/signup", params={"email": email})
        updated_response = client.get("/activities")
        updated_participants = len(updated_response.json()[activity]["participants"])

        # Assert
        assert updated_participants == initial_participants + 1
