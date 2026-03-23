"""
Shared test configuration and fixtures for the FastAPI application tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture that provides a TestClient instance with a fresh app state.
    
    Yields:
        TestClient: A test client for making requests to the FastAPI app.
    """
    return TestClient(app)


@pytest.fixture
def sample_activity_name():
    """Sample activity name for testing."""
    return "Chess Club"


@pytest.fixture
def sample_email():
    """Sample student email for testing."""
    return "test.student@mergington.edu"


@pytest.fixture
def existing_email():
    """Email of a participant already signed up for Chess Club."""
    return "michael@mergington.edu"
