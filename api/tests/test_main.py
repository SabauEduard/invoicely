import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_send_email_reminders():
    response = client.get("/email")
    assert response.status_code == 200
    assert response.content == b'Email reminders sent'

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.content == b'OK'