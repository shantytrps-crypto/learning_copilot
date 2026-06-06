"""Tests for the GET /activities endpoint"""
import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities"""
    # Arrange
    expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
    
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert response.status_code == 200
    assert isinstance(data, dict)
    for activity_name in expected_activities:
        assert activity_name in data


def test_get_activities_contains_required_fields(client):
    """Test that each activity has required fields"""
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_details in activities.items():
        for field in required_fields:
            assert field in activity_details, f"Missing {field} in {activity_name}"
        assert isinstance(activity_details["participants"], list)


def test_get_activities_participants_are_strings(client):
    """Test that all participants are email strings"""
    # Arrange (none needed, using initial state)
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_details in activities.items():
        for participant in activity_details["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant, f"Invalid email format: {participant}"
