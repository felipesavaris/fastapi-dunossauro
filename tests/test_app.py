from fast_zero.schemas import UserSchemaOut


def test_root_should_return_200_and_success_message(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'ola pessoas!'}


def test_read_html_should_return_success(client):
    response = client.get('/html')

    assert response.status_code == 200
    assert (
        response.text
        == """
        <html>
            <head>
                <title> Nosso olá mundo!</title>
            </head>
            <body>
                <h1> Olá Mundo </h1>
            </body>
        </html>
    """
    )


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
        'username': 'Teste',
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

    response = client.get('/users/1')

    assert response.status_code == 200
    assert response.json() == user_schema


def test_read_user_by_id_return_error_404_not_found(client):
    response = client.get('/users/0')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
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
        'id': 1,
    }


def test_update_user_when_raise_status_code_404(client):
    response = client.put(
        '/users/0',
        json={
            'username': 'Alice A',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_when_raise_status_code_404(client):
    response = client.delete('/users/0')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}
