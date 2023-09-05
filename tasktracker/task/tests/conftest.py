import pytest
from rest_framework.test import APIClient


client = APIClient()

@pytest.fixture
def user_credentials():
    return {
        'username': 'test',
        'password': '1111',
        'email': 'test@test.com',
        'city': 'testcity'
    }

@pytest.fixture
def task_credentials():
    return {
        'description': 'test',
        'due_date': '2012-12-12',
        'owner': 'http://0.0.0.0:8000/api/v1/users/1/'
    }
