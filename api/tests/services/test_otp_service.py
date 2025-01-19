import pytest
from unittest.mock import patch
from services.otp_service import generate_otp_secret, get_totp_uri, generate_qr_code, verify_otp

def test_generate_otp_secret():
    secret = generate_otp_secret()
    assert len(secret) == 32

def test_get_totp_uri():
    email = "test@example.com"
    otp_secret = "JBSWY3DPEHPK3PXP"
    uri = get_totp_uri(email, otp_secret)
    assert uri.startswith("otpauth://totp/Invoicely:test%40example.com")

def test_generate_qr_code():
    uri = "otpauth://totp/Invoicely:test@example.com?secret=JBSWY3DPEHPK3PXP"
    qr_code = generate_qr_code(uri)
    assert isinstance(qr_code, str)
    assert qr_code.startswith("iVBORw0KGgoAAAANSUhEUgAA")

def test_verify_otp_success():
    otp_secret = "JBSWY3DPEHPK3PXP"
    otp = "123456"
    with patch("pyotp.TOTP.verify", return_value=True) as mock_verify:
        result = verify_otp(otp_secret, otp)
        assert result is True
        mock_verify.assert_called_once_with(otp)

def test_verify_otp_failure():
    otp_secret = "JBSWY3DPEHPK3PXP"
    otp = "123456"
    with patch("pyotp.TOTP.verify", return_value=False) as mock_verify:
        result = verify_otp(otp_secret, otp)
        assert result is False
        mock_verify.assert_called_once_with(otp)
