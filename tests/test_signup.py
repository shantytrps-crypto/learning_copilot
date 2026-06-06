"""Tests for the POST /activities/{activity_name}/signup endpoint"""
import pytest


def test_signup_new_participant(client):
    """Test signing up a new participant for an activity"""
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert new_email in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity"""
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Act
    client.post(f"/activities/{activity_name}/signup?email={new_email}")
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert new_email in activities[activity_name]["participants"]


def test_signup_duplicate_participant_fails(client):
    """Test that signing up a participant twice fails"""
    # Arrange
    activity_name = "Chess Club"
    new_email = "duplicate@mergington.edu"
    
    # Act - First signup
    response1 = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert - First signup succeeds
    assert response1.status_code == 200
    
    # Act - Second signup with same email
    response2 = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert - Second signup fails
    assert response2.status_code == 400
    data = response2.json()
    assert "already signed up" in data["detail"]


def test_signup_already_registered_participant_fails(client):
    """Test that a participant already registered cannot sign up again"""
    # Arrange
    activity_name = "Chess Club"
    existing_participant = "michael@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={existing_participant}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_fails(client):
    """Test that signing up for a non-existent activity fails"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_multiple_participants(client):
    """Test signing up multiple participants to same activity"""
    # Arrange
    activity_name = "Gym Class"
    emails = ["test1@mergington.edu", "test2@mergington.edu", "test3@mergington.edu"]
    
    # Act
    for email in emails:
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        assert response.status_code == 200
    
    # Assert
    response = client.get("/activities")
    gym_participants = response.json()[activity_name]["participants"]
    for email in emails:
        assert email in gym_participants
