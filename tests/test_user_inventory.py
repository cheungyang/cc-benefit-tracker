import pytest
from starlette.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

@patch('app.main.get_db_connection')
def test_get_user_cards_empty(mock_get_db):
    mock_conn = MagicMock()
    mock_cur = mock_conn.cursor.return_value
    mock_get_db.return_value = mock_conn
    mock_cur.fetchall.return_value = []
    
    response = client.get("/api/user/cards")
    assert response.status_code == 200
    assert response.json() == []

@patch('app.main.get_db_connection')
def test_add_user_card_success(mock_get_db):
    mock_conn = MagicMock()
    mock_cur = mock_conn.cursor.return_value
    mock_get_db.return_value = mock_conn
    
    # Side effect for fetchone:
    # 1. card exists in master
    # 2. card NOT in user inventory
    # 3. returning id from insert
    mock_cur.fetchone.side_effect = [
        {"id": "card-uuid"}, # Master check
        None,                # Duplicate check
        {"id": "new-assoc-id"} # Insert returning
    ]
    
    response = client.post("/api/user/cards", json={"card_id": "card-uuid"})
    assert response.status_code == 201
    assert response.json()["card_id"] == "card-uuid"
    assert response.json()["id"] == "new-assoc-id"

@patch('app.main.get_db_connection')
def test_add_user_card_conflict(mock_get_db):
    mock_conn = MagicMock()
    mock_cur = mock_conn.cursor.return_value
    mock_get_db.return_value = mock_conn
    
    mock_cur.fetchone.side_effect = [
        {"id": "card-uuid"}, # Found in master
        {"id": "exist-id"}   # ALREADY in user inventory
    ]
    
    response = client.post("/api/user/cards", json={"card_id": "card-uuid"})
    assert response.status_code == 409

@patch('app.main.get_db_connection')
def test_delete_user_card_success(mock_get_db):
    mock_conn = MagicMock()
    mock_cur = mock_conn.cursor.return_value
    mock_get_db.return_value = mock_conn
    
    # rowcount > 0 means something was deleted
    mock_cur.rowcount = 1
    
    response = client.delete("/api/user/cards/assoc-uuid")
    assert response.status_code == 204

@patch('app.main.get_db_connection')
def test_delete_user_card_not_found(mock_get_db):
    mock_conn = MagicMock()
    mock_cur = mock_conn.cursor.return_value
    mock_get_db.return_value = mock_conn
    
    mock_cur.rowcount = 0
    
    response = client.delete("/api/user/cards/nonexistent")
    assert response.status_code == 404
