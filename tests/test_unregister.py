"""Tests for the DELETE /activities/{activity_name}/unregister endpoint"""
import pytest


def test_unregister_existing_participant(client):
    """Test unregistering a participant from an activity"""
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={participant_email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert participant_email in data["message"]


def test_unregister_removes_participant(client):
    """Test that unregister actually removes the participant"""
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"
    
    # Act
    client.delete(
        f"/activities/{activity_name}/unregister?email={participant_email}"
    )
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert participant_email not in activities[activity_name]["participants"]


def test_unregister_nonexistent_participant_fails(client):
    """Test that unregistering a non-existent participant fails"""
    # Arrange
    activity_name = "Chess Club"
    nonexistent_email = "nonexistent@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={nonexistent_email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_nonexistent_activity_fails(client):
    """Test that unregistering from a non-existent activity fails"""
    # Arrange
    activity_name = "Nonexistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_twice_fails(client):
    """Test that unregistering the same participant twice fails"""
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"
    
    # Act - First unregister
    response1 = client.delete(
        f"/activities/{activity_name}/unregister?email={participant_email}"
    )
    
    # Assert - First unregister succeeds
    assert response1.status_code == 200
    
    # Act - Second unregister
    response2 = client.delete(
        f"/activities/{activity_name}/unregister?email={participant_email}"
    )
    
    # Assert - Second unregister fails
    assert response2.status_code == 400
    assert "not signed up" in response2.json()["detail"]


def test_unregister_multiple_participants(client):
    """Test unregistering multiple participants from same activity"""
    # Arrange
    activity_name = "Programming Class"
    emails = ["test1@mergington.edu", "test2@mergington.edu"]
    
    # Act - Add participants
    for email in emails:
        client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Act - Remove participants
    for email in emails:
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        assert response.status_code == 200
    
    # Assert
    response = client.get("/activities")
    programming_participants = response.json()[activity_name]["participants"]
    for email in emails:
        assert email not in programming_participants
