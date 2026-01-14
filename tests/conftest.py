
# conftest.py
import pytest

@pytest.fixture
def app():
    from main import create_app
    app = create_app()
    app.config.update({"TESTING": True})
    yield app
 
@pytest.fixture
def client(app):
    return app.test_client()
