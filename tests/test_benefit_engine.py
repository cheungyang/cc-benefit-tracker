import pytest
from starlette.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app
from datetime import date

client = TestClient(app)

@patch('app.main.get_db_connection')
def test_get_user_benefits_claimed(mock_get_db):
    mock_conn = MagicMock()
    mock_cur = mock_conn.cursor.return_value
    mock_get_db.return_value = mock_conn
    
    # User's benefits
    mock_cur.fetchall.return_value = [
        {
            "benefit_id": "b1",
            "card_name": "Amex Gold",
            "benefit_name": "Uber Cash",
            "amount": 10.00,
            "category": "Dining",
            "frequency": "monthly"
        }
    ]
    
    # Claimed in current window
    mock_cur.fetchone.return_value = {"id": "claim1"}
    
    with patch('app.main.date') as mock_date:
        mock_date.today.return_value = date(2026, 5, 26)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        
        response = client.get("/api/user/benefits")
        
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "CLAIMED"
    assert data[0]["days_remaining"] == 6
    assert data[0]["reset_date"] == "2026-06-01"

@patch('app.main.get_db_connection')
def test_get_user_benefits_not_claimed(mock_get_db):
    mock_conn = MagicMock()
    mock_cur = mock_conn.cursor.return_value
    mock_get_db.return_value = mock_conn
    
    mock_cur.fetchall.return_value = [
        {
            "benefit_id": "b1",
            "card_name": "Amex Gold",
            "benefit_name": "Uber Cash",
            "amount": 10.00,
            "category": "Dining",
            "frequency": "monthly"
        }
    ]
    
    # NOT claimed in current window (fetchone return None)
    # AND CLAIMED in previous window (to avoid MISSED)
    mock_cur.fetchone.side_effect = [
        None,             # current window check
        {"id": "prev-cl"} # previous window check
    ]
    
    with patch('app.main.date') as mock_date:
        mock_date.today.return_value = date(2026, 5, 26)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        
        response = client.get("/api/user/benefits")
        
    assert response.status_code == 200
    data = response.json()
    assert data[0]["status"] == "NOT_CLAIMED"

@patch('app.main.get_db_connection')
def test_get_user_benefits_missed(mock_get_db):
    mock_conn = MagicMock()
    mock_cur = mock_conn.cursor.return_value
    mock_get_db.return_value = mock_conn
    
    mock_cur.fetchall.return_value = [
        {
            "benefit_id": "b1",
            "card_name": "Amex Gold",
            "benefit_name": "Uber Cash",
            "amount": 10.00,
            "category": "Dining",
            "frequency": "monthly"
        }
    ]
    
    # NOT claimed in current AND NOT claimed in previous
    mock_cur.fetchone.side_effect = [
        None, # current
        None  # previous
    ]
    
    with patch('app.main.date') as mock_date:
        mock_date.today.return_value = date(2026, 5, 26)
        mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
        
        response = client.get("/api/user/benefits")
        
    assert response.status_code == 200
    data = response.json()
    assert data[0]["status"] == "MISSED"
