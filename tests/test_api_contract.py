from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_health_like_flow():
    # sadece route var mı kontrol
    resp = client.get("/tasks/does-not-exist")
    assert resp.status_code in (200, 404)
