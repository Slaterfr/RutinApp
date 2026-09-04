def test_health_check(client):
    """Smoke test: Verify the service is running and /health returns 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
