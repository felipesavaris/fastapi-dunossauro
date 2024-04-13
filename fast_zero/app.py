from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from fast_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserSchemaIn,
    UserSchemaOut,
)

app = FastAPI()


@app.get('/', status_code=200, response_model=Message)
def read_root():
    return {'message': 'ola pessoas!'}


@app.get('/html', status_code=200, response_class=HTMLResponse)
def read_html():
    return """
        <html>
            <head>
                <title> Nosso olá mundo!</title>
            </head>
            <body>
                <h1> Olá Mundo </h1>
            </body>
        </html>
    """


# templates no fastapi
# https://fastapi.tiangolo.com/pt/advanced/templates/
# =======================

# live de websockets -> usados em html
# https://www.youtube.com/watch?v=EqFzY8dBWHs

"""
-> foi falado sobre:
    ajax
    polling -> se atualiza a cada x tempo
    websocket -> o servidor atualiza quando chegar algo novo
              -> broadcast: manda pra várias conexoes a nova mensagem inserida
        MODELO DE PUSH este é o modelo usado com o broadcast
        modelo full-duplex - modelo bidirecional (ex: chat, jogo... pois estes existem mais de 1 agente  mandando ao mesmo tempo)
"""

database = []


def check_invalid_user(user_id: int) -> None:
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')


@app.post('/users/', status_code=201, response_model=UserSchemaOut)
def create_user(user: UserSchemaIn):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)

    return user_with_id


@app.get('/users/', status_code=200, response_model=UserList)
def read_users():
    return {'users': database}


@app.get('/users/{user_id}', status_code=200, response_model=UserSchemaOut)
def read_user(user_id: int):
    check_invalid_user(user_id=user_id)

    return database[user_id - 1]


@app.put('/users/{user_id}', status_code=200, response_model=UserSchemaOut)
def update_user(user_id: int, user: UserSchemaIn):
    check_invalid_user(user_id=user_id)

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', status_code=200, response_model=Message)
def delete_user(user_id: int):
    check_invalid_user(user_id=user_id)

    del database[user_id - 1]

    return Message(message='User deleted')
