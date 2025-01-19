import pytest
from unittest.mock import patch, MagicMock
from services.role_service import RoleService
from dtos.role_dtos import RoleCreateDTO, RoleDTO

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.mark.asyncio
async def test_create_role_success(mock_db):
    role_create_dto = RoleCreateDTO(name="Admin")
    fake_role = RoleDTO(id=1, name="Admin")
    with patch("services.role_service.RoleRepository.create", return_value=fake_role) as mock_repo:
        result = await RoleService.create(role_create_dto, mock_db)
        assert result == fake_role
        mock_repo.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_roles(mock_db):
    expected_roles = [
        RoleDTO(id=1, name="Admin"),
        RoleDTO(id=2, name="User")
    ]
    with patch("services.role_service.RoleRepository.get_all", return_value=expected_roles) as mock_repo:
        result = await RoleService.get_all(mock_db)
        assert len(result) == 2
        mock_repo.assert_called_once()

@pytest.mark.asyncio
async def test_get_role_by_id_success(mock_db):
    role = RoleDTO(id=1, name="Admin")
    with patch("services.role_service.RoleRepository.get_by_id", return_value=role) as mock_repo:
        result = await RoleService.get_by_id(1, mock_db)
        assert result.id == 1
        mock_repo.assert_called_once()

@pytest.mark.asyncio
async def test_get_role_by_id_not_found(mock_db):
    with patch("services.role_service.RoleRepository.get_by_id", return_value=None):
        with pytest.raises(Exception) as exc_info:
            await RoleService.get_by_id(999, mock_db)
        assert "not found" in str(exc_info.value)

@pytest.mark.asyncio
async def test_delete_role_success(mock_db):
    role = RoleDTO(id=1, name="Admin")
    with patch("services.role_service.RoleRepository.get_by_id", return_value=role), \
         patch("services.role_service.RoleRepository.delete_by_id", return_value=None) as mock_delete:
        await RoleService.delete(1, mock_db)
        mock_delete.assert_called_once()
