import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all("participants" in v for v in data.values())

def test_signup_and_unregister():
    # Use a test email and activity
    test_email = "pytest-student@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))

    # Sign up
    signup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert signup.status_code in (200, 400)  # 400 if already signed up

    # Check participant is in list
    activities = client.get("/activities").json()
    assert test_email in activities[activity]["participants"]

    # Unregister
    unregister = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert unregister.status_code == 200
    # Check participant is removed
    activities = client.get("/activities").json()
    assert test_email not in activities[activity]["participants"]
