from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)



def test_protected_route_without_key_is_401():
    r = client.get("/api/v1/mcp/tools")
    assert r.status_code == 401






def test_security_headers_present():
    r = client.get("/")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "DENY"
    assert "Content-Security-Policy" in r.headers