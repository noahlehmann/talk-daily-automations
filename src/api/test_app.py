from unittest.mock import patch, MagicMock

import pytest

from app import app

@pytest.fixture
def client():
    """Set up a test client and ensure app context is available."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        with app.app_context():  # Ensure app context is available
            yield client  # Run tests inside context

@patch("app.db.session")  # Mock the database session
@patch("app.Counter.query")
def test_increment(mock_query, mock_session, client):
    """Test that /increment correctly increases the counter without using the real DB."""
    # Mock Counter.query.first() to return a fake counter object
    mock_counter = MagicMock()
    mock_counter.value = 0
    mock_query.first.return_value = mock_counter

    response = client.get("/increment")

    assert response.status_code == 200
    assert response.json["counter"] == 1  # Should increment the mocked counter

    # Ensure commit was called
    mock_session.add.assert_not_called()  # No new counter should be added
    mock_session.commit.assert_called_once()
