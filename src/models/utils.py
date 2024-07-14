from pydantic import BaseModel, ConfigDict, GetJsonSchemaHandler
from pydantic.alias_generators import to_camel
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema


class TunedModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        use_enum_values=True,
        from_attributes=True,
        extra="ignore",
    )

    @classmethod
    def __get_pydantic_json_schema__(
            cls, core_schema: CoreSchema, handler: GetJsonSchemaHandler
    ) -> JsonSchemaValue:
        """Remove nullablity from optional fields."""
        _json_schema = handler(core_schema)
        json_schema = handler.resolve_ref_schema(_json_schema)
        if "properties" not in json_schema:
            return _json_schema
        required = json_schema.get("required", [])
        changed = False
        for key, prop in json_schema["properties"].items():
            if prop.get("default", "") is not None:
                continue
            if key in required:
                continue
            # remove nullablilty
            changed = True
            del prop["default"]
            if prop.get("anyOf") is None:
                continue
            non_nullable = [t for t in prop["anyOf"] if t.get("type") != "null"]
            if len(non_nullable) == 1:
                del prop["anyOf"]
                prop.update(non_nullable[0])
            else:
                prop["anyOf"] = non_nullable
        return json_schema if changed else _json_schema
