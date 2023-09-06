import pytest
from rest_framework.test import APIClient
from rest_framework.permissions import IsAuthenticated
from tests.conftest import (
    user_jwt,
    access_token
)
from userprofile.models import Profile


client = APIClient()

@pytest.fixture
def is_authenticated_mock(mocker):
    mock = mocker.patch.object(IsAuthenticated, 'has_permission')
    return mock


@pytest.mark.parametrize(
        "is_authenticated, expected_status",
        [
            (True, 201),
            (False, 401)
        ]
)
def test_create_task( 
        is_authenticated,
        expected_status,
        task_credentials,
        is_authenticated_mock,
        user_jwt,
        access_token,
        ):
    is_authenticated_mock.return_value = is_authenticated

    client.credentials(HTTP_AUTHORIZATION='Token ' + access_token)
    response = client.post('/api/v1/tasks/', task_credentials)

    assert response.status_code == expected_status
