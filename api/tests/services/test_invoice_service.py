import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi import UploadFile
from services.invoice_service import InvoiceService
from dtos.invoice_dtos import InvoiceCreateDTO, InvoiceDTO
from enums.category import InvoiceCategory
from enums.status import InvoiceStatus
from enums.importance import Importance
from io import BytesIO

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.fixture
def mock_user():
    return MagicMock(id=1)

@pytest.fixture
def mock_file():
    return UploadFile(filename="test.pdf", file=BytesIO(b"test content"))

@pytest.mark.asyncio
async def test_create_invoice_success(mock_db, mock_user, mock_file):
    dto = InvoiceCreateDTO(
        name="MyInvoice",
        vendor="TestVendor",
        amount=100.0,
        status=InvoiceStatus.PENDING,
        importance=Importance.LOW,
        emission_date="2023-01-01",
        due_date="2024-01-01",
        file=mock_file,
        user_id=1,
        category=InvoiceCategory.OTHER,
        path="test/path",
        content="Test content",
        notes="Some notes",
        duplicate=False,
        incomplete=False
    )
    fake_invoice = InvoiceDTO(
        id=1,
        name="MyInvoice",
        user_id=1,
        category=InvoiceCategory.OTHER,
        path="uploads/test.pdf",
        vendor="TestVendor",
        amount=100.0,
        status=InvoiceStatus.PENDING,
        importance=Importance.LOW,
        notes="Some notes",
        duplicate=False,
        incomplete=False,
        emission_date="2023-01-01T00:00:00",
        due_date="2024-01-01T00:00:00"
    )
    with patch("services.invoice_service.detect_category", return_value=("TestCategory", "FileContent")) as mock_detect, \
         patch("services.invoice_service.os.remove") as mock_remove, \
         patch("services.invoice_service.InvoiceRepository.create", return_value=fake_invoice) as mock_repo:
        result = await InvoiceService.create(dto, mock_db, mock_user)
        assert result == fake_invoice
        mock_detect.assert_called_once()
        mock_remove.assert_called_once()
        mock_repo.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_invoices(mock_db, mock_user):
    expected_invoices = [
        InvoiceDTO(
            id=1,
            name="Invoice1",
            user_id=1,
            category=InvoiceCategory.OTHER,
            path="uploads/invoice1.pdf",
            vendor="Vendor1",
            amount=100.0,
            status=InvoiceStatus.PENDING,
            importance=Importance.LOW,
            notes="Notes1",
            duplicate=False,
            incomplete=False,
            emission_date="2023-01-01T00:00:00",
            due_date="2024-01-01T00:00:00"
        ),
        InvoiceDTO(
            id=2,
            name="Invoice2",
            user_id=1,
            category=InvoiceCategory.OTHER,
            path="uploads/invoice2.pdf",
            vendor="Vendor2",
            amount=200.0,
            status=InvoiceStatus.PENDING,
            importance=Importance.LOW,
            notes="Notes2",
            duplicate=False,
            incomplete=False,
            emission_date="2023-01-01T00:00:00",
            due_date="2024-01-01T00:00:00"
        )
    ]
    with patch("services.invoice_service.InvoiceRepository.get_all", return_value=expected_invoices) as mock_repo:
        result = await InvoiceService.get_all(mock_db, mock_user)
        assert len(result) == 2
        mock_repo.assert_called_once()

@pytest.mark.asyncio
async def test_get_invoice_by_id_success(mock_db, mock_user):
    invoice = InvoiceDTO(
        id=1,
        name="Invoice1",
        user_id=1,
        category=InvoiceCategory.OTHER,
        path="uploads/invoice1.pdf",
        vendor="Vendor1",
        amount=100.0,
        status=InvoiceStatus.PENDING,
        importance=Importance.LOW,
        notes="Notes1",
        duplicate=False,
        incomplete=False,
        emission_date="2023-01-01T00:00:00",
        due_date="2024-01-01T00:00:00"
    )
    with patch("services.invoice_service.InvoiceRepository.get_by_id", return_value=invoice) as mock_repo:
        result = await InvoiceService.get_by_id(1, mock_db, mock_user)
        assert result.id == 1
        mock_repo.assert_called_once()

@pytest.mark.asyncio
async def test_get_invoice_by_id_not_found(mock_db, mock_user):
    with patch("services.invoice_service.InvoiceRepository.get_by_id", return_value=None):
        with pytest.raises(Exception) as exc_info:
            await InvoiceService.get_by_id(999, mock_db, mock_user)
        assert "not found" in str(exc_info.value)

@pytest.mark.asyncio
async def test_get_unpaid_by_due_date(mock_db):
    with patch("services.invoice_service.InvoiceRepository.get_unpaid_by_due_date", return_value=[]) as mock_repo:
        result = await InvoiceService.get_unpaid_by_due_date("2024-01-01", mock_db)
        assert result == []
        mock_repo.assert_called_once()

@pytest.mark.asyncio
async def test_get_unpaid_by_due_date_range(mock_db):
    with patch("services.invoice_service.InvoiceRepository.get_unpaid_by_due_date_range", return_value=[]) as mock_repo:
        result = await InvoiceService.get_unpaid_by_due_date_range("2023-01-01", "2023-12-31", mock_db)
        assert result == []
        mock_repo.assert_called_once()

@pytest.mark.asyncio
async def test_get_all_unpaid_overdue(mock_db):
    with patch("services.invoice_service.InvoiceRepository.get_all_unpaid_overdue", return_value=[]) as mock_repo:
        result = await InvoiceService.get_all_unpaid_overdue(mock_db)
        assert result == []
        mock_repo.assert_called_once()

@pytest.mark.asyncio
async def test_update_invoice_success(mock_db, mock_user, mock_file):
    invoice_dto = InvoiceDTO(
        id=1,
        name="MyOldInvoice",
        user_id=1,
        category=InvoiceCategory.OTHER,
        path="uploads/oldfile.pdf",
        vendor="OldVendor",
        amount=50.0,
        status=InvoiceStatus.PENDING,
        importance=Importance.LOW,
        notes="Test notes",
        duplicate=False,
        incomplete=False,
        emission_date="2023-01-01T00:00:00",
        due_date="2024-01-01T00:00:00"
    )
    with patch("services.invoice_service.InvoiceRepository.get_by_id", return_value=invoice_dto), \
         patch("services.invoice_service.InvoiceRepository.update", return_value=invoice_dto) as mock_update:
        update_dto = InvoiceCreateDTO(
            name="MyUpdatedInvoice",
            vendor="VendorUpdated",
            amount=123.4,
            status=InvoiceStatus.PENDING,
            importance=Importance.HIGH,
            emission_date="2023-06-01",
            due_date="2024-01-01",
            file=mock_file,
            user_id=1,
            category=InvoiceCategory.OTHER,
            path="uploads/newfile.pdf",
            content="Updated content",
            notes="Updated notes",
            duplicate=False,
            incomplete=False
        )
        result = await InvoiceService.update_invoice(1, update_dto, mock_db, mock_user)
        assert result == invoice_dto
        mock_update.assert_called_once()

@pytest.mark.asyncio
async def test_delete_invoice_success(mock_db, mock_user):
    invoice_dto = InvoiceDTO(
        id=1,
        name="Invoice1",
        user_id=1,
        category=InvoiceCategory.OTHER,
        path="uploads/invoice1.pdf",
        vendor="Vendor1",
        amount=100.0,
        status=InvoiceStatus.PENDING,
        importance=Importance.LOW,
        notes="Notes1",
        duplicate=False,
        incomplete=False,
        emission_date="2023-01-01T00:00:00",
        due_date="2024-01-01T00:00:00"
    )
    with patch("services.invoice_service.InvoiceRepository.get_by_id", return_value=invoice_dto), \
         patch("services.invoice_service.InvoiceRepository.delete_by_id", return_value=None) as mock_delete:
        await InvoiceService.delete_invoice(1, mock_db, mock_user)
        mock_delete.assert_called_once()

@pytest.mark.asyncio
async def test_get_total_by_vendor_in_date_range(mock_db, mock_user):
    with patch("services.invoice_service.InvoiceRepository.get_total_by_vendor_in_date_range", return_value=[]) as mock_repo:
        result = await InvoiceService.get_total_by_vendor_in_date_range("2023-01-01", "2023-12-31", mock_db, mock_user)
        assert result == []
        mock_repo.assert_called_once()