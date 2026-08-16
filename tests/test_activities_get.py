"""Tests for the GET /activities endpoint."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


class TestActivitiesGet:
    """Test cases for GET /activities endpoint."""
    
    def test_get_activities_returns_200(self, client):
        """Test that GET /activities returns status 200."""
        response = client.get("/activities")
        assert response.status_code == 200
    
    def test_get_activities_returns_dict(self, client):
        """Test that GET /activities returns a dictionary."""
        response = client.get("/activities")
        data = response.json()
        assert isinstance(data, dict)
    
    def test_get_activities_returns_all_9_activities(self, client):
        """Test that GET /activities returns all 9 activities."""
        response = client.get("/activities")
        data = response.json()
        assert len(data) == 9
    
    def test_get_activities_contains_expected_activities(self, client):
        """Test that all expected activity names are present."""
        response = client.get("/activities")
        data = response.json()
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Art Club",
            "Drama Club",
            "Debate Team",
            "Science Club"
        ]
        for activity in expected_activities:
            assert activity in data
    
    def test_get_activities_schema_has_required_fields(self, client):
        """Test that each activity has required fields."""
        response = client.get("/activities")
        data = response.json()
        required_fields = ["description", "schedule", "max_participants", "participants"]
        
        for activity_name, activity_data in data.items():
            for field in required_fields:
                assert field in activity_data, f"Activity {activity_name} missing field {field}"
    
    def test_get_activities_participants_is_list(self, client):
        """Test that participants field is a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity {activity_name} participants should be a list"
    
    def test_get_activities_max_participants_is_integer(self, client):
        """Test that max_participants is an integer."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"Activity {activity_name} max_participants should be an integer"
    
    def test_get_activities_chess_club_has_initial_participants(self, client):
        """Test that Chess Club has initial participants."""
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        
        assert len(chess_club["participants"]) == 2
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]
