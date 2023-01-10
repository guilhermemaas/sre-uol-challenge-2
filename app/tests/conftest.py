import pytest
import sys 

#sys.path.insert(0, '../')
#from app import app as flask_app
#from github import GitHubApi
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

