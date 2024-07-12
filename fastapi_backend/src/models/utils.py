from typing import Type, TypeVar, Annotated, Any

from pydantic import GetCoreSchemaHandler
from pydantic_core import CoreSchema


class NotNullable:
    def __get_pydantic_core_schema__(
            self, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        schema = handler(source)
        assert schema["type"] == "nullable"
        return schema["schema"]  # type: ignore


T = TypeVar("T")
Omissible = Annotated[T | None, NotNullable()]
