import pytest
from userprofile.models import Profile
from rest_framework.test import APIClient


client = APIClient()

@pytest.fixture
def user_jwt(user_credentials, db):
    user = Profile.objects.create_user(**user_credentials)
    return user

@pytest.fixture
def access_token(user_credentials):
    response = client.post('/api/v1/token/', user_credentials)
    return response.json().get('access_token')