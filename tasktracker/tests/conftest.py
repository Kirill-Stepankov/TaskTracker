import pytest
from userprofile.models import Profile
from rest_framework.test import APIClient
import jwt
from tasktracker.settings import SECRET_KEY
from django.http import HttpRequest

client = APIClient()

@pytest.fixture
def user_jwt(user_credentials, db):
    user = Profile.objects.create_user(**user_credentials)
    return user

@pytest.fixture
def access_token(user_credentials):
    response = client.post('/api/v1/token/', user_credentials)
    return response.json().get('access')

@pytest.fixture
def valid_jwt_request(
    user_jwt,
    access_token
):
    request = HttpRequest()
    request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + access_token
    return request

@pytest.fixture
def invalid_jwt_request():
    request = HttpRequest()
    request.META['HTTP_AUTHORIZATION'] = 'Bearer ' + 'Invalid token'
    return request
