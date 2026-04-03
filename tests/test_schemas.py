import pytest
from pydantic import ValidationError


def test_user_create_requires_valid_email():
    from app.users.schemas import UserCreate
    with pytest.raises(ValidationError):
        UserCreate(email="not-an-email", password="password123")


def test_user_create_valid():
    from app.users.schemas import UserCreate
    user = UserCreate(email="test@example.com", password="password123")
    assert user.email == "test@example.com"


def test_task_create_requires_title():
    from app.tasks.schemas import TaskCreate
    with pytest.raises(ValidationError):
        TaskCreate()


def test_task_update_all_fields_optional():
    from app.tasks.schemas import TaskUpdate
    update = TaskUpdate()  # should not raise
    assert update.title is None
    assert update.is_done is None


def test_token_response_default_type():
    from app.auth.schemas import TokenResponse
    token = TokenResponse(access_token="abc123")
    assert token.token_type == "bearer"


def test_user_response_from_attributes():
    from app.users.schemas import UserResponse
    from datetime import datetime, timezone

    class FakeUser:
        id = 1
        email = "a@b.com"
        created_at = datetime(2026, 1, 1, tzinfo=timezone.utc)

    schema = UserResponse.model_validate(FakeUser())
    assert schema.id == 1
    assert schema.email == "a@b.com"
