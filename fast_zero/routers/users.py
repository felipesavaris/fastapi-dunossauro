from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import Message, UserList, UserSchemaIn, UserSchemaOut
from fast_zero.security import get_current_user, get_password_hash

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/users', tags=['users'])


def check_invalid_user(user: User) -> None:
    if not user:
        raise HTTPException(status_code=404, detail='User not found')


@router.post('/', status_code=201, response_model=UserSchemaOut)
def create_user(user: UserSchemaIn, session: Session):
    db_user = session.scalar(select(User.username == user.username))

    if db_user:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )

    hashed_password = get_password_hash(user.password)

    db_user = User(
        username=user.username, password=hashed_password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@router.get('/', status_code=200, response_model=UserList)
def read_users(session: Session, skip: int = 0, limit: int = 100):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return UserList(users=users)


@router.get('/{user_id}', status_code=200, response_model=UserSchemaOut)
def read_user(user_id: int, session: Session):
    db_user = session.scalar(select(User).where(User.id == user_id))

    check_invalid_user(user=db_user)

    return db_user


@router.put('/{user_id}', status_code=200, response_model=UserSchemaOut)
def update_user(
    user_id: int,
    user: UserSchemaIn,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    current_user.username = user.username
    current_user.password = get_password_hash(user.password)
    current_user.email = user.email

    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete('/{user_id}', status_code=200, response_model=Message)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(status_code=400, detail='Not enough permissions')

    session.delete(current_user)
    session.commit()

    return Message(message='User deleted')
