from fast_zero.schemas import UserSchemaOut


def test_create_user(client):
    data = {
        'username': 'alice',
        'email': 'alice@example.com',
        'password': 'secret',
    }

    response = client.post('/users/', json=data)

    assert response.status_code == 201
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_create_user_return_400_bad_request_error(client, user):
    data = {
        'username': user.username,
        'email': 'alice@example.com',
        'password': 'secret',
    }

    response = client.post('/users/', json=data)

    assert response.status_code == 400
    assert response.json() == {'detail': 'Username already registered'}


def test_read_users_success_with_empty_data(client):
    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_all_users_success(client, user):
    user_schema = UserSchemaOut.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == 200
    assert response.json() == {'users': [user_schema]}


def test_read_user_by_id_return_success_200(client, user):
    user_schema = UserSchemaOut.model_validate(user).model_dump()

    response = client.get(f'/users/{user.id}')

    assert response.status_code == 200
    assert response.json() == user_schema


def test_read_user_by_id_return_error_404_not_found(client):
    response = client.get('/users/0')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Alice A',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        'username': 'Alice A',
        'email': 'alice@example.com',
        'id': user.id,
    }


def test_update_user_with_wrong_user_raise_error_400(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Aice A',
            'email': 'test@tes.com',
            'password': 'secret',
        }
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}


def test_update_user_when_raise_status_code_401(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'Alice A',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_when_raise_status_code_401(client):
    response = client.delete('/users/0')

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_user_when_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Not enough permissions'}
