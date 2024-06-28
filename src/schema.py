from typing import List

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


class TariffWithFunctionsSchema(BaseModel):
    id: int
    title: str
    functions: List[FunctionSchema]


class ClientWithTariffsSchema(BaseModel):
    id: int
    name: str
    balance: int
    tariffs: List[TariffSchema]
