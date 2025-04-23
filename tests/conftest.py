import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from api.main import app
from api.db import get_db


@pytest.fixture
def mock_db():
    """Creates a mock SQLAlchemy session"""
    mock_session = MagicMock()
    return mock_session


@pytest.fixture
def test_client(mock_db):
    """Creates a test client for the FastAPI app with a mocked database session"""
    app.dependency_overrides[get_db] = lambda: mock_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
