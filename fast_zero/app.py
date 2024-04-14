from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserSchemaIn, UserSchemaOut

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

# database = []


def check_invalid_user(user: User) -> None:
    # verificaçao usada quando o DB era em memória
    # if user_id > len(database) or user_id < 1:
    if not user:
        raise HTTPException(status_code=404, detail='User not found')


@app.post('/users/', status_code=201, response_model=UserSchemaOut)
def create_user(user: UserSchemaIn, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User.username == user.username))

    if db_user:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', status_code=200, response_model=UserList)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return UserList(users=users)


@app.get('/users/{user_id}', status_code=200, response_model=UserSchemaOut)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    check_invalid_user(user=db_user)

    return db_user


@app.put('/users/{user_id}', status_code=200, response_model=UserSchemaOut)
def update_user(
    user_id: int, user: UserSchemaIn, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))

    check_invalid_user(user=db_user)

    # user_with_id = UserDB(**user.model_dump(), id=user_id)
    # database[user_id - 1] = user_with_id
    # return user_with_id

    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email

    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}', status_code=200, response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    check_invalid_user(user=db_user)

    session.delete(db_user)
    session.commit()

    return Message(message='User deleted')
