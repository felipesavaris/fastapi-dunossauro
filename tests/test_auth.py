def test_create_access_token_return_success(client, user):
    data = {'username': user.email, 'password': user.clean_password}

    response = client.post('auth/token', data=data)
    token = response.json()

    assert response.status_code == 201
    assert 'access_token' in token
    assert 'token_type' in token
