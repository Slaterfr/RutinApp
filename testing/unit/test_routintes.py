import pytest 
from unittest.mock import Mock, patch, MagicMock
from pydantic import ValidationError
from services.routines import RoutineService
from schemas import Routine
from services.handlers import InvalidData

class TestRoutineService:

    @pytest.fixture
    def routine_service(self):
        return RoutineService()
    
    def test_create_routine_valid(self, routine_service):
        """Test creating a routine with valid data"""
        data = Routine(
            name="PPL",
            days_per_week=3,
            estimated_hours=1.5
        )

        user_id = 1

        # Mock the CRUD create method instead of the session
        with patch.object(routine_service.crud, 'create') as mock_create:
            mock_create.return_value = {
                "id": 1,
                "name": "PPL",
                "days_per_week": 3,
                "estimated_hours": 1.5,
                "owner_id": 1
            }
            
            result = routine_service.create(data, user_id)

            # Verify CRUD create was called with correct data
            assert mock_create.called
            assert result["owner_id"] == user_id
            assert result["name"] == "PPL"

    def test_create_routine_invalid_name(self):
        """Test that empty name raises ValidationError"""
        # Pydantic validates BEFORE the service function
        with pytest.raises(ValidationError):
            Routine(
                name="",
                days_per_week=3,
                estimated_hours=1.5
            )

    def test_create_routine_invalid_days_too_low(self, routine_service):
        """Test that days_per_week < 1 raises ValidationError"""
        with pytest.raises(ValidationError):
            Routine(
                name="Valid Name",
                days_per_week=0,  # Invalid!
                estimated_hours=1.5
            )

    def test_create_routine_invalid_days_too_high(self, routine_service):
        """Test that days_per_week > 7 raises ValidationError"""
        with pytest.raises(ValidationError):
            Routine(
                name="Valid Name",
                days_per_week=8,  # Invalid!
                estimated_hours=1.5
            )