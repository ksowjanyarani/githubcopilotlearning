"""Tests for the POST /activities/{activity_name}/unregister endpoint."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestUnregister:
    """Test cases for POST /activities/{activity_name}/unregister endpoint."""
    
    def test_unregister_valid_activity_enrolled_participant_returns_200(self, client):
        """Test successful unregister of an enrolled participant."""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 200
    
    def test_unregister_valid_activity_enrolled_participant_removes_participant(self, client):
        """Test that unregister removes participant from activity."""
        email = "michael@mergington.edu"
        initial_count = len(activities["Chess Club"]["participants"])
        
        response = client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 200
        assert len(activities["Chess Club"]["participants"]) == initial_count - 1
        assert email not in activities["Chess Club"]["participants"]
    
    def test_unregister_valid_activity_enrolled_participant_returns_success_message(self, client):
        """Test that successful unregister returns appropriate message."""
        email = "michael@mergington.edu"
        response = client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Chess Club" in data["message"]
    
    def test_unregister_invalid_activity_returns_404(self, client):
        """Test that unregister from non-existent activity returns 404."""
        response = client.post(
            "/activities/NonExistent%20Activity/unregister?email=student@mergington.edu"
        )
        assert response.status_code == 404
    
    def test_unregister_invalid_activity_returns_error_detail(self, client):
        """Test that 404 includes error detail."""
        response = client.post(
            "/activities/NonExistent%20Activity/unregister?email=student@mergington.edu"
        )
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_unregister_not_enrolled_participant_returns_400(self, client):
        """Test that unregister of non-enrolled participant returns 400."""
        email = "notstudent@mergington.edu"  # Not in Chess Club
        response = client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 400
    
    def test_unregister_not_enrolled_participant_returns_error_detail(self, client):
        """Test that unregister of non-enrolled includes error detail."""
        email = "notstudent@mergington.edu"
        response = client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"].lower()
    
    def test_unregister_double_unregister_returns_400(self, client):
        """Test that unregistering same participant twice returns 400 second time."""
        email = "michael@mergington.edu"
        
        # First unregister should succeed
        response1 = client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response1.status_code == 200
        
        # Second unregister should fail
        response2 = client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response2.status_code == 400
    
    def test_unregister_does_not_affect_other_participants(self, client):
        """Test that unregistering one participant doesn't affect others."""
        email_to_remove = "michael@mergington.edu"
        email_to_keep = "daniel@mergington.edu"
        initial_count = len(activities["Chess Club"]["participants"])
        
        response = client.post(
            f"/activities/Chess%20Club/unregister?email={email_to_remove}"
        )
        assert response.status_code == 200
        
        # Verify other participant still exists
        assert email_to_keep in activities["Chess Club"]["participants"]
        assert len(activities["Chess Club"]["participants"]) == initial_count - 1
    
    def test_unregister_different_activities_independent(self, client):
        """Test that unregister from one activity doesn't affect another."""
        # First add a participant to multiple activities
        email = "test@mergington.edu"
        client.post(f"/activities/Chess%20Club/signup?email={email}")
        client.post(f"/activities/Basketball%20Team/signup?email={email}")
        
        # Unregister from Chess Club
        response = client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 200
        
        # Should still be in Basketball Team
        assert email in activities["Basketball Team"]["participants"]
    
    def test_unregister_restores_spot(self, client):
        """Test that unregistering frees up a participant spot."""
        email = "michael@mergington.edu"
        initial_count = len(activities["Chess Club"]["participants"])
        max_participants = activities["Chess Club"]["max_participants"]
        
        # Verify we have a spot
        spots_left_before = max_participants - initial_count
        
        # Unregister
        response = client.post(
            f"/activities/Chess%20Club/unregister?email={email}"
        )
        assert response.status_code == 200
        
        # Verify spot is available
        new_count = len(activities["Chess Club"]["participants"])
        spots_left_after = max_participants - new_count
        assert spots_left_after == spots_left_before + 1
    
    def test_unregister_multiple_participants_sequence(self, client):
        """Test removing multiple participants sequentially."""
        emails = ["michael@mergington.edu", "daniel@mergington.edu"]
        initial_count = len(activities["Chess Club"]["participants"])
        
        for email in emails:
            response = client.post(
                f"/activities/Chess%20Club/unregister?email={email}"
            )
            assert response.status_code == 200
        
        # Verify all were removed
        assert len(activities["Chess Club"]["participants"]) == initial_count - len(emails)
        for email in emails:
            assert email not in activities["Chess Club"]["participants"]
