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
