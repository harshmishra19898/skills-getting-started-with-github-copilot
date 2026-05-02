import copy
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


# Capture the original activities state at module load time
_ORIGINAL_ACTIVITIES = copy.deepcopy(activities)


@pytest.fixture
def client():
    """Fixture providing a TestClient for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def clean_activities():
    """
    Fixture that resets the activities dict to its original state before and after each test.
    This ensures test isolation by preventing state from leaking between tests.
    Uses deepcopy to ensure nested objects (dicts, lists) are fresh copies each time.
    """
    # Reset activities to the original state before test (with fresh deep copies)
    activities.clear()
    activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))
    
    yield activities
    
    # Reset activities to the original state after test (with fresh deep copies)
    activities.clear()
    activities.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))
