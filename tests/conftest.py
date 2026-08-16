import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient for testing the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test."""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball league and training",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis coaching and friendly matches",
            "schedule": "Mondays and Wednesdays, 3:00 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu", "ryan@mergington.edu"]
        },
        "Art Club": {
            "description": "Painting, drawing, and visual arts exploration",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater productions and acting workshops",
            "schedule": "Thursdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["lucas@mergington.edu", "zoe@mergington.edu"]
        },
        "Debate Team": {
            "description": "Public speaking and competitive debate",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["noah@mergington.edu"]
        },
        "Science Club": {
            "description": "Scientific experiments and exploration",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
        }
    }
    
    # Reset before test
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Reset after test
    activities.clear()
    activities.update(original_activities)
