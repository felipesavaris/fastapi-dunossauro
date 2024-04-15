from jwt import decode

from fast_zero.security import Settings, create_access_token

settings = Settings()


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data=data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']  # Testa se o valor foi add ao token
