from typing import Any, Type, TypeVar, Annotated

from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema, PydanticOmit
from xsentinels.sentinel import Sentinel


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
        if value is Missing:
            # Keeps the associated attribute 'deleted/omitted' from model.
            raise PydanticOmit()

        # If we somehow get a non-Missing value (should not happen), return it unchanged.
        return value

    @staticmethod
    def _serialize(value: Any) -> 'MissingType':
        # Keeps the associated attribute 'deleted/omitted' from model.
        # raise PydanticOmit()

        # Return same value we got, when requested to try and serialize real data it's not 'Missing',
        # and if it is, that means `Value` is `Missing` and we are fine to return that also.
        # I would love to rase a `raise PydanticOmit()` if `value` is `Missing`, but that does not currently work
        # for Pydantic, so I just return the `Missing` unchanged for now.
        # If there is a serialization error later on about how Pydantic can't turn `Missing` into a `Json`
        # then we can debug the situation
        # (right now PartialModel should delete any attributes that are set to `Missing` to work around this limitation)
        return value


Missing = MissingType()
""" Returned as attribute value when attribute value is missing. Can also be set on attribute to indicate it's missing.
"""


class AutoPartialExcludeMarkerType(Sentinel):
    pass


AutoPartialExcludeMarker = AutoPartialExcludeMarkerType()
""" Used by `pydantic_partials.partial.AutoPartialExclude` to mark a field as excluded from automatic partials.
    See `pydantic_partials.config.PartialConfigDict.auto_partials_exclude` for more details.
"""
