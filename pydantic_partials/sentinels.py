from typing import Any, Type
from xsentinels.sentinel import Sentinel
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema, PydanticOmit


class MissingType(Sentinel):
    """ Class/Type of `Missing`, a sentinel that is used to indicate if a field is missing its value
        in a `pydantic_partials.partial.PartialModel` subclass.
    """
    # Notes/See (https://docs.pydantic.dev/latest/concepts/json_schema/#modifying-the-schema).

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Type[Any], handler: GetCoreSchemaHandler
    ) -> core_schema.CoreSchema:
        assert source_type is MissingType
        # We never want to serialize any Missing values.
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.is_instance_schema(cls=MissingType),  # core_schema.any_schema(),
            # serialization=core_schema.plain_serializer_function_ser_schema(
            #     cls._serialize,
            #     # return_schema=core_schema.AnySchema
            # )
        )

    @staticmethod
    def _validate(value: Any, info: core_schema.ValidationInfo) -> 'MissingType':
        # If we somehow get a non-Missing value (should not happen), return it unchanged.
        return Missing

    @staticmethod
    def _serialize(value: Any) -> str:
        # We used to want to raise a PydanticOmit here, but now we are using `exclude_if`, which does not need it.
        return "**MISSING**"


# For backwards compatability + I don't really like all upper-case for sentential object (ie: `None`).
Missing = MissingType()


class AutoPartialExcludeMarkerType(Sentinel):
    pass


AutoPartialExcludeMarker = AutoPartialExcludeMarkerType()
""" Used by `pydantic_partials.partial.AutoPartialExclude` to mark a field as excluded from automatic partials.
    See `pydantic_partials.config.PartialConfigDict.auto_partials_exclude` for more details.
"""
