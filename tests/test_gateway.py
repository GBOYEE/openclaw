import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add the polish/openclaw directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'polish', 'openclaw'))

from gateway import app  # FastAPI instance

@pytest.fixture
def client():
    return TestClient(app)

def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok" or data["status"] == "healthy"

def test_auth_missing(client):
    response = client.post("/gateway/auth", json={"test": "data"})
    assert response.status_code in (400, 401, 422)

def test_execute_unauthorized(client):
    response = client.post("/gateway/execute", json={"skill": "test"})
    assert response.status_code in (401, 403)