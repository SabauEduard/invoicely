import pyotp
import qrcode
from io import BytesIO
from base64 import b64encode


def generate_otp_secret():
    return pyotp.random_base32()


def get_totp_uri(email, otp_secret):
    totp = pyotp.TOTP(otp_secret)
    return totp.provisioning_uri(email, issuer_name="Invoicely")


def generate_qr_code(uri):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(uri)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    return b64encode(buffer.getvalue()).decode()


def verify_otp(otp_secret, otp):
    totp = pyotp.TOTP(otp_secret)
    return totp.verify(otp)
