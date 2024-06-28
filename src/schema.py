from pydantic import BaseModel


class ClientSchema(BaseModel):
    balance: int
    id: int
    name: str


class TariffSchema(BaseModel):
    id: int
    title: str


class FunctionSchema(BaseModel):
    id: int
    title: str
