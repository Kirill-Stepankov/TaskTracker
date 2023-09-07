from task.tests.conftest import (
    user_credentials
)
from tests.conftest import (
    user_jwt,
    access_token,
    valid_jwt_request,
    invalid_jwt_request
)
from userprofile.models import Profile
from userprofile.service import UserService
import pytest
from rest_framework import exceptions
from rest_framework.test import APIClient
from userprofile.permissions import IsAnonymous


client = APIClient()

@pytest.fixture
def is_anonymous_mock(mocker):
    mock = mocker.patch.object(IsAnonymous, 'has_permission')
    return mock

def test_valid_user_jwt(
    user_credentials,
    user_jwt,
    access_token,
    valid_jwt_request,
):
    user_id = UserService().get_user_id(valid_jwt_request)
    user = Profile.objects.filter(pk=user_id).first()

    assert user is not None

    assert user.username == user_credentials.get('username')
    assert user.email == user_credentials.get('email')
    assert user.city == user_credentials.get('city')

def test_invaid_user_jwt(invalid_jwt_request):
     with pytest.raises(exceptions.AuthenticationFailed):
        UserService().get_user_data(invalid_jwt_request)

@pytest.mark.parametrize(
        "is_anonymous, username_or_email_already_exist, expected_code",
        [
            (True, True, 400),
            (True, False, 201),
            (False, True, 401),
            (False, False, 401)
        ]
)
def test_signup(
    is_anonymous,
    username_or_email_already_exist,
    expected_code,
    user_credentials,
    is_anonymous_mock,
    db
):
    is_anonymous_mock.return_value = is_anonymous

    if username_or_email_already_exist:
        Profile.objects.create_user(**user_credentials)

    response = client.post('/api/v1/signup/', user_credentials)

    assert response.status_code == expected_code