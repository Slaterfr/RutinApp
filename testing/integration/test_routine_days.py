import pytest


def test_create_day_with_valid_weekday(client, auth_headers_a):
    """User should be able to create a routine day with a scheduled weekday (0=Monday..6=Sunday)."""
    create_routine_res = client.post(
        "/routines/",
        json={"name": "Weekly Split", "days_per_week": 3, "estimated_hours": 3.0},
        headers=auth_headers_a
    )
    assert create_routine_res.status_code == 200
    routine_id = create_routine_res.json()["id"]

    # Add Day with Monday (0)
    day_res = client.post(
        f"/routines/{routine_id}/days",
        json={
            "day_number": 1,
            "day_name": "Push Day",
            "focus_area": "Chest, Shoulders, Triceps",
            "weekday": 0
        },
        headers=auth_headers_a
    )
    assert day_res.status_code == 200
    day_data = day_res.json()
    assert day_data["weekday"] == 0
    day_id = day_data["id"]

    # Verify retrieval via GET /routines/{id}/days
    get_days_res = client.get(f"/routines/{routine_id}/days")
    assert get_days_res.status_code == 200
    days = get_days_res.json()
    assert len(days) == 1
    assert days[0]["weekday"] == 0

    # Verify retrieval via GET /routines/{id}
    get_routine_res = client.get(f"/routines/{routine_id}")
    assert get_routine_res.status_code == 200
    routine_info = get_routine_res.json()
    assert len(routine_info["days"]) == 1
    assert routine_info["days"][0]["weekday"] == 0


def test_update_day_weekday(client, auth_headers_a):
    """User should be able to update an existing day's weekday."""
    create_routine_res = client.post(
        "/routines/",
        json={"name": "Leg Split", "days_per_week": 2, "estimated_hours": 2.0},
        headers=auth_headers_a
    )
    routine_id = create_routine_res.json()["id"]

    # Add Day initially on Wednesday (2)
    day_res = client.post(
        f"/routines/{routine_id}/days",
        json={
            "day_number": 1,
            "day_name": "Leg Day",
            "focus_area": "Quads, Hamstrings",
            "weekday": 2
        },
        headers=auth_headers_a
    )
    day_id = day_res.json()["id"]

    # Update day to Friday (4)
    update_res = client.put(
        f"/routines/{routine_id}/days/{day_id}",
        json={"weekday": 4},
        headers=auth_headers_a
    )
    assert update_res.status_code == 200
    assert update_res.json()["weekday"] == 4


def test_create_day_without_weekday(client, auth_headers_a):
    """Weekday should remain optional for backward compatibility."""
    create_routine_res = client.post(
        "/routines/",
        json={"name": "Flexible Routine", "days_per_week": 1, "estimated_hours": 1.0},
        headers=auth_headers_a
    )
    routine_id = create_routine_res.json()["id"]

    day_res = client.post(
        f"/routines/{routine_id}/days",
        json={
            "day_number": 1,
            "day_name": "Full Body",
            "focus_area": "All"
        },
        headers=auth_headers_a
    )
    assert day_res.status_code == 200
    assert day_res.json()["weekday"] is None


def test_weekday_validation_out_of_bounds(client, auth_headers_a):
    """Weekday values outside 0-6 should fail validation (HTTP 422)."""
    create_routine_res = client.post(
        "/routines/",
        json={"name": "Boundaries Test", "days_per_week": 1, "estimated_hours": 1.0},
        headers=auth_headers_a
    )
    routine_id = create_routine_res.json()["id"]

    # Weekday = 7 (Invalid)
    res_high = client.post(
        f"/routines/{routine_id}/days",
        json={
            "day_number": 1,
            "day_name": "Invalid Day",
            "focus_area": "None",
            "weekday": 7
        },
        headers=auth_headers_a
    )
    assert res_high.status_code == 422

    # Weekday = -1 (Invalid)
    res_low = client.post(
        f"/routines/{routine_id}/days",
        json={
            "day_number": 1,
            "day_name": "Invalid Day",
            "focus_area": "None",
            "weekday": -1
        },
        headers=auth_headers_a
    )
    assert res_low.status_code == 422


def test_get_and_update_routine_with_multiple_days(client, auth_headers_a):
    """Verify GET and PUT /routines/{id} serialize days without DetachedInstanceError and sort properly."""
    create_res = client.post(
        "/routines/",
        json={"name": "PPL Full", "days_per_week": 3, "estimated_hours": 4.5},
        headers=auth_headers_a
    )
    assert create_res.status_code == 200
    routine_id = create_res.json()["id"]

    # Add day 1: Friday (4)
    client.post(
        f"/routines/{routine_id}/days",
        json={"day_number": 2, "day_name": "Pull", "focus_area": "Back", "weekday": 4},
        headers=auth_headers_a
    )
    # Add day 2: Monday (0)
    client.post(
        f"/routines/{routine_id}/days",
        json={"day_number": 1, "day_name": "Push", "focus_area": "Chest", "weekday": 0},
        headers=auth_headers_a
    )

    # 1. GET /routines/{id}
    get_res = client.get(f"/routines/{routine_id}")
    assert get_res.status_code == 200
    data = get_res.json()
    assert data["name"] == "PPL Full"
    assert len(data["days"]) == 2
    # Ensure sorted by weekday: Monday (0) first, Friday (4) second
    assert data["days"][0]["day_name"] == "Push"
    assert data["days"][0]["weekday"] == 0
    assert data["days"][1]["day_name"] == "Pull"
    assert data["days"][1]["weekday"] == 4

    # 2. PUT /routines/{id}
    put_res = client.put(
        f"/routines/{routine_id}",
        json={"name": "PPL Full Updated", "estimated_hours": 5.0},
        headers=auth_headers_a
    )
    assert put_res.status_code == 200
    updated_data = put_res.json()
    assert updated_data["name"] == "PPL Full Updated"
    assert updated_data["estimated_hours"] == 5.0
    assert len(updated_data["days"]) == 2
    assert updated_data["days"][0]["day_name"] == "Push"

