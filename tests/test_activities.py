"""
Tests for the GET /activities endpoint.
"""

import pytest


class TestGetActivities:
    """Tests for retrieving all activities."""

    def test_get_all_activities_returns_success(self, client):
        """
        Test that GET /activities returns a successful response.
        
        Arrange: Set up test client
        Act: Make GET request to /activities
        Assert: Status code is 200 and response contains activities
        """
        # Arrange
        expected_status = 200

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == expected_status

    def test_get_activities_returns_correct_structure(self, client):
        """
        Test that activities have the correct data structure.
        
        Arrange: Set up test client
        Act: Make GET request to /activities
        Assert: Response contains expected activity fields
        """
        # Arrange
        expected_fields = {"description", "schedule", "max_participants", "participants"}

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        assert isinstance(activities, dict)
        assert len(activities) > 0
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert isinstance(activity_data, dict)
            assert expected_fields.issubset(activity_data.keys())

    def test_get_activities_participants_is_list(self, client):
        """
        Test that participants field is a list of emails.
        
        Arrange: Set up test client
        Act: Make GET request to /activities
        Assert: Participants field is a list
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_data in activities.values():
            assert isinstance(activity_data["participants"], list)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
                assert "@" in participant

    def test_get_activities_max_participants_is_integer(self, client):
        """
        Test that max_participants is an integer.
        
        Arrange: Set up test client
        Act: Make GET request to /activities
        Assert: max_participants is an integer
        """
        # Arrange & Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_data in activities.values():
            assert isinstance(activity_data["max_participants"], int)
            assert activity_data["max_participants"] > 0
