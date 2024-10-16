from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    token: str


class Product(BaseModel):
    name: str
    id: int
