from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_generate_conversation_api():
    payload = {
        "description": "Sustainability in smart cities",
        "interests": ["green energy", "public transport"],
        "bio": "test bio"
        
    }
    response = client.post("/generate-conversation", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "topics" in data
    assert "suggestions" in data

def test_fact_check_api():
    response = client.post("/fact-check", json={"query": "solar energy"})
    assert response.status_code == 200
    data = response.json()
    assert "summary" in data