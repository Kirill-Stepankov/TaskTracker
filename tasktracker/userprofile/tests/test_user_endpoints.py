import pytest
from rest_framework.test import APIClient
from task.tests.conftest import (
    user_credentials
)
from tests.conftest import (
    user_jwt,
    access_token,
    valid_jwt_request,
    invalid_jwt_request,
    is_authenticated_mock
)
from rest_framework.permissions import IsAdminUser

client = APIClient()

@pytest.fixture
def is_admin_mock(mocker):
    mock = mocker.patch.object(IsAdminUser, 'has_permission')
    return mock


@pytest.mark.parametrize(
        "is_authenticated, expected_status",
        [
            (True, 204),
            (False, 403)
        ]
)
def test_delete_account(
        is_authenticated,
        expected_status,
        is_authenticated_mock,
        user_jwt,
        access_token,
):
    is_authenticated_mock.return_value = is_authenticated

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    response = client.delete(f'/api/v1/users/delete_account/')

    assert response.status_code == expected_status

@pytest.mark.parametrize(
        "is_authenticated, expected_status",
        [
            (True, 200),
            (False, 403)
        ]
)
def test_edit_settings(
        is_authenticated,
        expected_status,
        is_authenticated_mock,
        user_jwt,
        access_token,
        user_credentials
):
    is_authenticated_mock.return_value = is_authenticated

    user_credentials['username'] = 'new'
    user_credentials['email'] = 'newemail@bsu.by'
    user_credentials['city'] = 'new_city'

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    response = client.patch('/api/v1/users/edit_settings/', user_credentials)
    
    assert response.status_code == expected_status

    if expected_status == 200:
        assert response.json().get('username') == user_credentials['username']


@pytest.mark.parametrize(
        "is_authenticated, expected_status",
        [
            (True, 200),
            (False, 403)
        ]
)
def test_get_settings(
        is_authenticated,
        expected_status,
        is_authenticated_mock,
        user_jwt,
        access_token,
):
    is_authenticated_mock.return_value = is_authenticated

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    response = client.get('/api/v1/users/my_settings/')
    
    assert response.status_code == expected_status

@pytest.mark.parametrize(
        "is_admin, expected_status",
        [
            (True, 200),
            (False, 403)
        ]
)
def test_get_users(
        is_admin,
        expected_status,
        is_admin_mock,
        user_jwt,
        access_token,
):
    is_admin_mock.return_value = is_admin

    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    response = client.get('/api/v1/users/')
    
    assert response.status_code == expected_status