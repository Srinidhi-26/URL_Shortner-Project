import pytest
from urlshort import create_app

@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.ficture #this will set up client so testing framework can act as was a browser and testing out the project for us
def client(app):
    return app.test_client