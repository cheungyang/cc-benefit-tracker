import pytest
from starlette.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

@patch('app.main.get_db_connection')
def test_get_cards_no_params(mock_get_db):
    # Mock database connection and cursor
    mock_conn = MagicMock()
    mock_cur = mock_conn.cursor.return_value
    mock_get_db.return_value = mock_conn
    
    # Mock data
    mock_cur.fetchall.return_value = [
        {"id": "uuid1", "name": "Amex Gold Card", "issuer": "American Express", "image_url": "url1"},
        {"id": "uuid2", "name": "Chase Sapphire Reserve", "issuer": "Chase", "image_url": "url2"}
    ]
    
    response = client.get("/api/cards")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Amex Gold Card"
    
    mock_cur.execute.assert_called_with("SELECT id, name, issuer, image_url FROM cards")

@patch('app.main.get_db_connection')
def test_get_cards_filter_amex(mock_get_db):
    mock_conn = MagicMock()
    mock_cur = mock_conn.cursor.return_value
    mock_get_db.return_value = mock_conn
    
    mock_cur.fetchall.return_value = [
        {"id": "uuid1", "name": "Amex Gold Card", "issuer": "American Express", "image_url": "url1"}
    ]
    
    response = client.get("/api/cards?q=amex")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "Amex" in data[0]["name"]
    
    mock_cur.execute.assert_called_with(
        "SELECT id, name, issuer, image_url FROM cards WHERE name ILIKE %s OR issuer ILIKE %s",
        ('%amex%', '%amex%')
    )

@patch('app.main.get_db_connection')
def test_get_cards_no_results(mock_get_db):
    mock_conn = MagicMock()
    mock_cur = mock_conn.cursor.return_value
    mock_get_db.return_value = mock_conn
    
    mock_cur.fetchall.return_value = []
    
    response = client.get("/api/cards?q=nonexistent")
    assert response.status_code == 200
    data = response.json()
    assert data == []

@patch('app.main.get_db_connection')
def test_get_cards_db_error(mock_get_db):
    mock_get_db.return_value = None
    
    response = client.get("/api/cards")
    assert response.status_code == 500
    assert response.json() == {"error": "Database connection failed"}
