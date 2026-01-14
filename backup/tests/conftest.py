import pytest
from ..main import app 

@pytest.fixture
def client():
    """A test client for the app."""
    app.config.update({"TESTING": True}) 
    with app.test_client() as client:
        yield client 