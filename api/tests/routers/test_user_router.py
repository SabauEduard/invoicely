from unittest.mock import AsyncMock, patch
import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient
from main import app
from services.user_service import UserService
from dtos.user_dtos import UserDTO, UserCreateDTO

client = TestClient(app)

@pytest.fixture
def mock_db():
    return AsyncMock()

def test_get_users_success(mock_db):
    expected_users = [
        UserDTO(id=1, email="user1@example.com", first_name="User", last_name="One", is_2fa_enabled=False, role_id=1, creation_date="2022-01-01T00:00:00", deletion_date=None),
        UserDTO(id=2, email="user2@example.com", first_name="User", last_name="Two", is_2fa_enabled=False, role_id=2, creation_date="2022-01-01T00:00:00", deletion_date=None)
    ]
    with patch.object(UserService, 'get_all', return_value=expected_users) as mock_get_all:
        response = client.get("/users/")
        assert response.status_code == 200

def test_get_user_success(mock_db):
    expected_user = UserDTO(id=1, email="user1@example.com", first_name="User", last_name="One", is_2fa_enabled=False, role_id=1, creation_date="2022-01-01T00:00:00", deletion_date=None)
    with patch.object(UserService, 'get_by_id', return_value=expected_user) as mock_get_by_id:
        response = client.get("/users/1")
        assert response.status_code == 200

def test_get_user_not_found(mock_db):
    with patch.object(UserService, 'get_by_id', side_effect=HTTPException(status_code=404, detail="User not found")):
        response = client.get("/users/999")
        assert response.status_code == 404

def test_create_user_success(mock_db):
    new_user = UserCreateDTO(email="newuser@example.com", first_name="New", last_name="User", password="password", role_id=1)
    created_user = UserDTO(id=3, email="newuser@example.com", first_name="New", last_name="User", is_2fa_enabled=False, role_id=1, creation_date="2022-01-01T00:00:00", deletion_date=None)
    with patch.object(UserService, 'create', return_value=created_user) as mock_create:
        response = client.post("/users/", json=new_user.dict())
        assert response.status_code == 201

def test_create_user_duplicate(mock_db):
    new_user = UserCreateDTO(email="existinguser@example.com", first_name="Existing", last_name="User", password="password", role_id=1)
    with patch.object(UserService, 'create', side_effect=HTTPException(status_code=400, detail="User already exists")):
        response = client.post("/users/", json=new_user.dict())
        assert response.status_code == 400
        assert response.json() == {"detail": "User already exists"}

def test_delete_user_success(mock_db):
    with patch.object(UserService, 'delete_user', return_value=None) as mock_delete:
        response = client.delete("/users/1")
        assert response.status_code == 204

def test_delete_user_not_found(mock_db):
    with patch.object(UserService, 'delete_user', side_effect=HTTPException(status_code=404, detail="User not found")):
        response = client.delete("/users/999")
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}

def test_update_user_success(mock_db):
    updated_user = UserCreateDTO(email="updateduser@example.com", first_name="Updated", last_name="User", password="newpassword", role_id=1)
    returned_user = UserDTO(id=1, email="updateduser@example.com", first_name="Updated", last_name="User", is_2fa_enabled=False, role_id=1, creation_date="2022-01-01T00:00:00", deletion_date=None)
    with patch.object(UserService, 'update_user', return_value=returned_user) as mock_update:
        response = client.put("/users/1", json=updated_user.dict())
        assert response.status_code == 200

def test_update_user_not_found(mock_db):
    updated_user = UserCreateDTO(email="updateduser@example.com", first_name="Updated", last_name="User", password="newpassword", role_id=1)
    with patch.object(UserService, 'update_user', side_effect=HTTPException(status_code=404, detail="User not found")):
        response = client.put("/users/999", json=updated_user.dict())
        assert response.status_code == 404
        assert response.json() == {"detail": "User not found"}
