"""Tests for the root GET / endpoint."""

import pytest
from fastapi.testclient import TestClient
from src.app import app


class TestRoot:
    """Test cases for GET / endpoint."""
    
    def test_root_redirects_to_index(self, client):
        """Test that GET / redirects to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code in [301, 302, 303, 307, 308]
        assert "/static/index.html" in response.headers["location"]
    
    def test_root_follows_redirect_to_static_index(self, client):
        """Test that following redirect leads to static files."""
        response = client.get("/", follow_redirects=True)
        # When following redirect, static files are served
        assert response.status_code == 200
