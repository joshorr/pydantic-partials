from typing import Any, Type, TypeVar, Annotated

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema, PydanticOmit
from xsentinels.sentinel import Sentinel


class MissingType(Sentinel):
    # See (https://docs.pydantic.dev/latest/concepts/json_schema/#modifying-the-schema).

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        assert source is MissingType
        # We never want to serialize any Missing values.
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.any_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                cls._serialize,
                # return_schema=core_schema.AnySchema
            )
        )

    @staticmethod
    def _validate(value: Any, info: core_schema.ValidationInfo) -> 'MissingType':
        # Keeps the associated attribute 'deleted/omitted' from model.
        raise PydanticOmit()

    @staticmethod
    def _serialize(value: Any) -> 'MissingType':
        # Keeps the associated attribute 'deleted/omitted' from model.
        return Missing


Missing = MissingType()

