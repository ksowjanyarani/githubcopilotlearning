"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


class TestSignup:
    """Test cases for POST /activities/{activity_name}/signup endpoint."""
    
    def test_signup_valid_activity_valid_email_returns_200(self, client):
        """Test successful signup for a valid activity with valid email."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        assert response.status_code == 200
    
    def test_signup_valid_activity_valid_email_adds_participant(self, client):
        """Test that signup adds participant to activity."""
        email = "newstudent@mergington.edu"
        initial_count = len(activities["Chess Club"]["participants"])
        
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response.status_code == 200
        assert len(activities["Chess Club"]["participants"]) == initial_count + 1
        assert email in activities["Chess Club"]["participants"]
    
    def test_signup_valid_activity_valid_email_returns_success_message(self, client):
        """Test that successful signup returns appropriate message."""
        email = "newstudent@mergington.edu"
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Chess Club" in data["message"]
    
    def test_signup_invalid_activity_returns_404(self, client):
        """Test that signup to non-existent activity returns 404."""
        response = client.post(
            "/activities/NonExistent%20Activity/signup?email=student@mergington.edu"
        )
        assert response.status_code == 404
    
    def test_signup_invalid_activity_returns_error_detail(self, client):
        """Test that 404 includes error detail."""
        response = client.post(
            "/activities/NonExistent%20Activity/signup?email=student@mergington.edu"
        )
        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]
    
    def test_signup_duplicate_email_returns_400(self, client):
        """Test that duplicate signup returns 400 error."""
        email = "michael@mergington.edu"  # Already in Chess Club
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response.status_code == 400
    
    def test_signup_duplicate_email_returns_error_detail(self, client):
        """Test that duplicate signup includes error detail."""
        email = "michael@mergington.edu"
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()
    
    def test_signup_does_not_add_duplicate(self, client):
        """Test that duplicate signup does not add participant."""
        email = "michael@mergington.edu"
        initial_count = len(activities["Chess Club"]["participants"])
        
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        # Verify participant was not added
        assert len(activities["Chess Club"]["participants"]) == initial_count
    
    def test_signup_different_activities_independent(self, client):
        """Test that signup to one activity doesn't affect another."""
        email = "test@mergington.edu"
        
        # Sign up for Chess Club
        response1 = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response1.status_code == 200
        
        # Should still be able to sign up for Programming Class
        response2 = client.post(
            f"/activities/Programming%20Class/signup?email={email}"
        )
        assert response2.status_code == 200
        assert email in activities["Programming Class"]["participants"]
    
    def test_signup_special_characters_in_email(self, client):
        """Test signup with special characters in email."""
        from urllib.parse import quote
        email = "student+test@mergington.edu"
        encoded_email = quote(email, safe='')
        response = client.post(
            f"/activities/Basketball%20Team/signup?email={encoded_email}"
        )
        assert response.status_code == 200
        assert email in activities["Basketball Team"]["participants"]
    
    def test_signup_multiple_participants_sequence(self, client):
        """Test adding multiple participants sequentially."""
        emails = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]
        initial_count = len(activities["Drama Club"]["participants"])
        
        for email in emails:
            response = client.post(
                f"/activities/Drama%20Club/signup?email={email}"
            )
            assert response.status_code == 200
        
        # Verify all were added
        assert len(activities["Drama Club"]["participants"]) == initial_count + len(emails)
        for email in emails:
            assert email in activities["Drama Club"]["participants"]
