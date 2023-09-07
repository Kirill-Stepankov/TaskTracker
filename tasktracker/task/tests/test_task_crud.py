import pytest
from rest_framework.test import APIClient
from rest_framework.permissions import IsAuthenticated
from task.permissions import IsAdminOrIsOwner
from tests.conftest import (
    user_jwt,
    access_token
)
from task.models import Task


client = APIClient()

@pytest.fixture
def is_authenticated_mock(mocker):
    mock = mocker.patch.object(IsAuthenticated, 'has_permission')
    return mock

@pytest.fixture
def is_admin_or_is_self_mock(mocker):
    mock = mocker.patch.object(IsAdminOrIsOwner, 'has_object_permission')
    return mock

@pytest.fixture
def task(
    task_credentials,
    user_jwt,
    access_token,
):
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
    response = client.post('/api/v1/tasks/', task_credentials)
    return Task.objects.filter(owner=user_jwt).first()





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


@pytest.mark.parametrize(
        "is_admin_or_is_self, expected_status",
        [
            (True, 200),
            (False, 403)
        ]
)
def test_get_task(
        is_admin_or_is_self_mock,
        is_admin_or_is_self,
        expected_status,
        user_jwt,
        access_token,
        task,
):
    is_admin_or_is_self_mock.return_value = is_admin_or_is_self

    response = client.get(f'/api/v1/tasks/{task.pk}/')

    assert response.status_code == expected_status


@pytest.mark.parametrize(
        "is_admin_or_is_self, expected_status",
        [
            (True, 200),
            (False, 403)
        ]
)
def test_update_task(
        is_admin_or_is_self,
        expected_status,
        task_credentials,
        is_admin_or_is_self_mock,
        user_jwt,
        access_token,
        task,
):
    is_admin_or_is_self_mock.return_value = is_admin_or_is_self

    task_credentials['description'] = 'new desc'
    task_credentials['due_date'] = '2020-10-10'

    response = client.put(f'/api/v1/tasks/{task.pk}/', task_credentials)

    assert response.status_code == expected_status

    if expected_status == 200:
        assert response.json().get('description') == task_credentials['description']


@pytest.mark.parametrize(
        "is_admin_or_is_self, expected_status",
        [
            (True, 204),
            (False, 403)
        ]
)
def test_delete_task(
        is_admin_or_is_self,
        expected_status,
        task_credentials,
        is_admin_or_is_self_mock,
        user_jwt,
        access_token,
        task,
):
    is_admin_or_is_self_mock.return_value = is_admin_or_is_self

    response = client.delete(f'/api/v1/tasks/{task.pk}/')

    assert response.status_code == expected_status


