from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import DecodeError, decode, encode
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.schemas import TokenData

SECRET_KEY = 'your-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


async def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_expection = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')

        if not username:
            raise credentials_expection
        token_data = TokenData(username=username)
    except DecodeError:
        raise credentials_expection

    user = session.scalar(
        select(User).where(User.email == token_data.username)
    )

    if not user:
        raise credentials_expection

    return user