import pytest
from rest_framework.test import APIClient
from userprofile.models import Profile


@pytest.fixture
def api_client():
    return APIClient

@pytest.fixture
def user_credentials():
    return {
        'username': 'test',
        'password': '1111',
        'email': 'test@test.com',
        'city': 'testcity'
    }

@pytest.fixture
def user_jwt(user_credentials, api_client, db):
    user = Profile.objects.create_user(**user_credentials)
    response = api_client().post('/api/v1/token/', user_credentials)
    return response.json().get('access_token'), user