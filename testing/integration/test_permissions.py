import pytest
from datetime import date
from models import models

def test_user_cannot_update_another_users_routine(client, auth_headers_a, auth_headers_b):
    """User B should not be able to update User A's routine (HTTP 403)."""
    # 1. User A creates a routine
    create_res = client.post(
        "/routines/",
        json={"name": "User A Leg Day", "days_per_week": 2, "estimated_hours": 3.0},
        headers=auth_headers_a
    )
    assert create_res.status_code == 200
    routine_id = create_res.json()["id"]

    # 2. User B tries to update User A's routine
    update_res = client.put(
        f"/routines/{routine_id}",
        json={"name": "Hijacked Routine by User B"},
        headers=auth_headers_b
    )
    assert update_res.status_code == 403
    assert "Not authorized" in update_res.json().get("message", "")

    # 3. Verify routine name remains unchanged
    get_res = client.get(f"/routines/{routine_id}")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "User A Leg Day"


def test_user_cannot_delete_another_users_routine(client, auth_headers_a, auth_headers_b):
    """User B should not be able to delete User A's routine (HTTP 403)."""
    # 1. User A creates a routine
    create_res = client.post(
        "/routines/",
        json={"name": "User A Push Day", "days_per_week": 3, "estimated_hours": 4.0},
        headers=auth_headers_a
    )
    assert create_res.status_code == 200
    routine_id = create_res.json()["id"]

    # 2. User B tries to delete User A's routine
    del_res = client.delete(
        f"/routines/{routine_id}",
        headers=auth_headers_b
    )
    assert del_res.status_code == 403

    # 3. Verify routine still exists
    get_res = client.get(f"/routines/{routine_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == routine_id


def test_user_can_update_and_delete_own_routine(client, auth_headers_a):
    """User A should be able to update and delete their own routine."""
    create_res = client.post(
        "/routines/",
        json={"name": "Initial Name", "days_per_week": 3, "estimated_hours": 2.0},
        headers=auth_headers_a
    )
    assert create_res.status_code == 200
    routine_id = create_res.json()["id"]

    # Update own routine
    update_res = client.put(
        f"/routines/{routine_id}",
        json={"name": "Updated by Owner"},
        headers=auth_headers_a
    )
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "Updated by Owner"

    # Delete own routine
    del_res = client.delete(f"/routines/{routine_id}", headers=auth_headers_a)
    assert del_res.status_code == 200

    # Verify routine is gone
    get_res = client.get(f"/routines/{routine_id}")
    assert get_res.status_code == 404


def test_user_cannot_add_day_to_another_users_routine(client, auth_headers_a, auth_headers_b):
    """User B should not be able to add a RoutineDay to User A's routine (HTTP 403)."""
    create_res = client.post(
        "/routines/",
        json={"name": "User A Program", "days_per_week": 4, "estimated_hours": 4.0},
        headers=auth_headers_a
    )
    routine_id = create_res.json()["id"]

    # User B attempts to add a day to User A's routine
    day_res = client.post(
        f"/routines/{routine_id}/days",
        json={"day_number": 1, "day_name": "Injected Day", "focus_area": "Arms"},
        headers=auth_headers_b
    )
    assert day_res.status_code == 403


def test_user_cannot_view_another_users_sessions(client, user_a, auth_headers_b):
    """User B should not be able to view User A's private workout sessions (HTTP 403)."""
    response = client.get(
        f"/sessions/users/{user_a.id}/sessions",
        headers=auth_headers_b
    )
    assert response.status_code == 403
    assert "Not authorized" in response.json().get("message", "")


def test_user_cannot_update_or_delete_another_users_session(
    client, user_a, auth_headers_a, auth_headers_b, db_session
):
    """User B should not be able to update or delete User A's workout session (HTTP 403)."""
    # Create routine & session for User A
    create_routine_res = client.post(
        "/routines/",
        json={"name": "User A Routine", "days_per_week": 2, "estimated_hours": 2.0},
        headers=auth_headers_a
    )
    routine_id = create_routine_res.json()["id"]
    # Create day for User A's routine
    day_res = client.post(
        f"/routines/{routine_id}/days",
        json={"day_number": 1, "day_name": "Day 1", "focus_area": "Chest"},
        headers=auth_headers_a
    )
    assert day_res.status_code == 200
    day_id = day_res.json()["id"]

    create_session_res = client.post(
        "/sessions/",
        json={
            "routine_id": routine_id,
            "day_id": day_id,
            "session_date": str(date.today()),
            "notes": "Original user A notes"
        },
        headers=auth_headers_a
    )
    assert create_session_res.status_code == 201
    session_id = create_session_res.json()["id"]

    # User B attempts to update User A's session
    update_res = client.put(
        f"/sessions/{session_id}",
        json={"notes": "Modified by User B"},
        headers=auth_headers_b
    )
    assert update_res.status_code == 403

    # User B attempts to delete User A's session
    del_res = client.delete(
        f"/sessions/{session_id}",
        headers=auth_headers_b
    )
    assert del_res.status_code == 403
