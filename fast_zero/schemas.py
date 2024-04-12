from pydantic import BaseModel, EmailStr


class Message(BaseModel):
    message: str


class Base(BaseModel):
    id: int | None  # acredito que o none não t.á funfando como opcional


class UserSchemaBase(BaseModel):
    username: str
    email: EmailStr


class UserSchemaOut(Base, UserSchemaBase):  # schema UserPublic no site
    pass


class UserSchemaIn(UserSchemaBase):
    password: str


class UserDB(Base, UserSchemaIn):
    pass


class UserList(BaseModel):
    users: list[UserSchemaOut]
