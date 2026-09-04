import pytest
from jose import jwt
from datetime import datetime, timezone
from config import Config

def test_login_success(client, user_a):
    """Test successful login returns access and refresh tokens with user metadata."""
    response = client.post(
        "/login",
        data={"username": user_a.email, "password": "Password123!"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["type"] == "bearer"
    assert data["user_id"] == user_a.id
    assert data["username"] == user_a.username


def test_jwt_claims_and_signature(client, user_a):
    """Verify that the generated JWT has the correct claims and signature."""
    response = client.post(
        "/login",
        data={"username": user_a.email, "password": "Password123!"}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]

    # Decode and verify JWT claims
    payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.TOKEN_ALGORITHM])
    assert payload.get("user_id") == user_a.id
    assert "exp" in payload

    # Expiration should be in the future
    exp_timestamp = payload["exp"]
    current_timestamp = datetime.now(timezone.utc).timestamp()
    assert exp_timestamp > current_timestamp


def test_login_wrong_password(client, user_a):
    """Test login with an incorrect password fails."""
    response = client.post(
        "/login",
        data={"username": user_a.email, "password": "WrongPassword!"}
    )
    assert response.status_code in [401, 403]


def test_login_nonexistent_user(client):
    """Test login with a non-existent email fails."""
    response = client.post(
        "/login",
        data={"username": "doesnotexist@example.com", "password": "Password123!"}
    )
    assert response.status_code in [401, 404]


def test_refresh_token_lifecycle(client, user_a):
    """Test using a valid refresh token yields a new valid access token."""
    login_res = client.post(
        "/login",
        data={"username": user_a.email, "password": "Password123!"}
    )
    refresh_token = login_res.json()["refresh_token"]

    # Request new access token using refresh token
    refresh_res = client.post(
        "/refresh",
        json={"refresh_token": refresh_token}
    )
    assert refresh_res.status_code == 200
    new_token = refresh_res.json()["access_token"]
    assert new_token is not None

    # Verify new token's claim
    payload = jwt.decode(new_token, Config.SECRET_KEY, algorithms=[Config.TOKEN_ALGORITHM])
    assert payload.get("user_id") == user_a.id


def test_refresh_token_invalid(client):
    """Test refreshing with an invalid token fails with 401."""
    response = client.post(
        "/refresh",
        json={"refresh_token": "non-existent-or-tampered-token"}
    )
    assert response.status_code == 401


def test_logout_revokes_token(client, user_a):
    """Test that logging out revokes the refresh token so it cannot be used again."""
    login_res = client.post(
        "/login",
        data={"username": user_a.email, "password": "Password123!"}
    )
    refresh_token = login_res.json()["refresh_token"]

    # Logout
    logout_res = client.post(
        "/logout",
        json={"refresh_token": refresh_token}
    )
    assert logout_res.status_code == 200
    assert logout_res.json()["detail"] == "Logged out successfully"

    # Subsequent refresh with the revoked token must fail
    second_refresh = client.post(
        "/refresh",
        json={"refresh_token": refresh_token}
    )
    assert second_refresh.status_code == 401


def test_protected_route_without_token(client):
    """Test that accessing a protected endpoint without an Authorization header returns 401."""
    routine_payload = {
        "name": "Morning Cardio",
        "days_per_week": 3,
        "estimated_hours": 2.0
    }
    response = client.post("/routines/", json=routine_payload)
    assert response.status_code == 401


def test_protected_route_with_malformed_token(client):
    """Test that accessing a protected endpoint with an invalid token returns 401."""
    routine_payload = {
        "name": "Morning Cardio",
        "days_per_week": 3,
        "estimated_hours": 2.0
    }
    response = client.post(
        "/routines/",
        json=routine_payload,
        headers={"Authorization": "Bearer invalid.fake.token"}
    )
    assert response.status_code == 401


def test_protected_route_with_valid_token(client, auth_headers_a):
    """Test that a valid token allows access to protected routes."""
    routine_payload = {
        "name": "Strength Training",
        "days_per_week": 4,
        "estimated_hours": 5.0
    }
    response = client.post(
        "/routines/",
        json=routine_payload,
        headers=auth_headers_a
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Strength Training"
