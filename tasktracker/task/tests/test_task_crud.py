from ..models import Task
import pytest

@pytest.mark.django_db
def test_create_task(api_client, user_jwt, db):
    client = api_client()
    access_token, user = user_jwt
    client.force_authenticate(user=user, token=access_token)
    response = client.post('/api/v1/tasks/', {
        'description': 'test',
        'due_date': '2012-12-12',
        'owner': 'http://0.0.0.0:8000/api/v1/users/1/'
    })

    assert response.status_code == 201

    response = client.get('/api/v1/tasks/1/')
    assert response.status_code == 200

    # смотри это я сверху так заменил проверку в бд
    # assert Task.objects.filter(owner=user)
