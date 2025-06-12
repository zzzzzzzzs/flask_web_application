import os
import sys
sys.path.insert(0, os.getcwd())
from app import app
import pytest

@pytest.fixture(scope='module')
def client():
    with app.test_client() as client:
        yield client


