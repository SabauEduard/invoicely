import pytest
from fastapi import HTTPException
from unittest.mock import patch, MagicMock, AsyncMock
from services.tag_service import TagService
from dtos.tag_dtos import TagCreateDTO, TagDTO, TagsCreateDTO

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.mark.asyncio
async def test_create_tag_success(mock_db):
    tags_create_dto = TagsCreateDTO(tags=["Tag1", "Tag2"])
    existing_tags = [TagDTO(id=1, name="Tag1")]
    with patch("services.tag_service.TagRepository.get_all", return_value=existing_tags) as mock_get_all, \
         patch("services.tag_service.TagRepository.create", return_value=TagDTO(id=2, name="Tag2")) as mock_create:
        await TagService.create(tags_create_dto, mock_db)
        mock_get_all.assert_called_once()
        mock_create.assert_called_once_with(TagCreateDTO(tag="Tag2"), mock_db)

@pytest.mark.asyncio
async def test_get_all_tags(mock_db):
    expected_tags = [
        TagDTO(id=1, name="Tag1"),
        TagDTO(id=2, name="Tag2")
    ]
    with patch("services.tag_service.TagRepository.get_all", return_value=expected_tags) as mock_repo:
        result = await TagService.get_all(mock_db)
        assert len(result) == 2
        mock_repo.assert_called_once()

@pytest.mark.asyncio
async def test_get_tag_by_id_success(mock_db):
    tag = TagDTO(id=1, name="Tag1")
    with patch("services.tag_service.TagRepository.get_by_id", return_value=tag) as mock_repo:
        result = await TagService.get_by_id(1, mock_db)
        assert result.id == 1
        mock_repo.assert_called_once()

@pytest.mark.asyncio
async def test_get_tag_by_id_not_found(mock_db):
    with patch("services.tag_service.TagRepository.get_by_id", return_value=None):
        with pytest.raises(HTTPException) as exc_info:
            await TagService.get_by_id(999, mock_db)
        assert exc_info.value.status_code == 404
        assert "Tag with this id not found" in str(exc_info.value.detail)

@pytest.mark.asyncio
async def test_delete_tag_success(mock_db):
    tag = TagDTO(id=1, name="Tag1")
    with patch("services.tag_service.TagRepository.get_by_id", return_value=tag), \
         patch("services.tag_service.TagRepository.delete_by_id", return_value=None) as mock_delete:
        await TagService.delete(1, mock_db)
        mock_delete.assert_called_once()
