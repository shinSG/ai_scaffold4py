from fastapi.testclient import TestClient

from agent_scaffold.api.main import app


def test_health_endpoint() -> None:
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
