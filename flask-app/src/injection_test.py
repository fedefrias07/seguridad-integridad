import pytest, random, string

from app import app
from datetime import datetime, timedelta

@pytest.fixture 
def client():
    app.testing = True
    client = app.test_client()
    return client

def test_injection(client):
    
    response = client.get('/usuarios/qlcfcym@gmail.com')
    json_data = response.json
    print(json_data)
    assert response.status_code == 200
    assert json_data["rta"] == "ok"