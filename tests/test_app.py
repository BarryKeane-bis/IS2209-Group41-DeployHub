import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200

def test_status(client):
    res = client.get("/status")
    assert res.status_code == 200
def test_data_endpoint_returns_expected_keys(client):
    res = client.get("/data")
    assert res.status_code == 200
    json_data = res.get_json()
    assert "exercises" in json_data
    assert "plans" in json_data
    assert "muscle_group" in json_data

def test_data_endpoint_default_muscle(client):
    res = client.get("/data")
    json_data = res.get_json()
    assert json_data["muscle_group"] == "chest"

def test_data_endpoint_custom_muscle(client):
    res = client.get("/data?muscle=biceps")
    json_data = res.get_json()
    assert json_data["muscle_group"] == "biceps"

def test_plans_get(client):
    res = client.get("/plans")
    assert res.status_code == 200

def test_plans_post(client):
    res = client.post("/plans", json={"name": "Test Plan", "user_id": "george"})
    assert res.status_code in [200, 201, 503]

def test_health_returns_json(client):
    res = client.get("/health")
    json_data = res.get_json()
    assert json_data["status"] == "ok"

def test_status_returns_json(client):
    res = client.get("/status")
    json_data = res.get_json()
    assert "status" in json_data
