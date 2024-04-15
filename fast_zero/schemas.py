from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class Base(BaseModel):
    id: int


class UserSchemaBase(BaseModel):
    username: str
    email: EmailStr


class UserSchemaOut(Base, UserSchemaBase):  # schema UserPublic no site
    # converte o modelo do sqlalchemy para que o pydantic consiga ler
    model_config = ConfigDict(from_attributes=True)


class UserSchemaIn(UserSchemaBase):
    password: str


# class UserDB(Base, UserSchemaIn):
#     # usando apenas quando o DB era em memória
#     pass


class UserList(BaseModel):
    users: list[UserSchemaOut]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
