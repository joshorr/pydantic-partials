import typing
from typing import Any, get_args, get_origin, TypeVar, Iterable

from pydantic import BaseModel

from pydantic._internal._model_construction import ModelMetaclass
from pydantic_core import PydanticUndefined
from xsentinels import Default
from xsentinels.default import DefaultType

from .config import PartialConfigDict
from .sentinels import Missing, MissingType, AutoPartialExcludeMarker

from logging import getLogger


# metaclass to make all fields in a model optional, useful for PATCH requests
class PartialMeta(ModelMetaclass):
    """ Metaclass of `pydantic_partials.partial.PartialModel`, used to support partial fields,
        including the ability ot automatically apply `pydantic_partials.partial.Partial`[...] to fields
        via `pydantic_partials.config.PartialConfigDict.auto_partials` configuration option.
    """
    model_partial_fields: typing.ClassVar[set[str]]
    """ Set of strings representing field names that can be missing from validation/serialization.
        If they are missing, they will return the `Missing` sentinel value and the field will be entirely
        skipped when serializing the model.

        If not missing, they will return their normal value, be included in serializing the model
        and otherwise act normally.

        If any type has their type-hint unioned with `MissingType` it will be a partial field.
        If `auto_add_missing_type` is True (default is True), then all fields on model will automatically
        be unioned with MissingType.
    """

    config_dict: PartialConfigDict
    """ Adding some extra/new config options on-top of the already pre-existing Pydantic ones.
        Seemed like a good place to put them, as it deals with configuration of the class model behavior.
    """

    def __new__(
            cls,
            name: str,
            bases: tuple[type],
            namespaces: dict[str, Any],
            *,

            auto_partials: bool | DefaultType = Default,
            auto_partials_exclude: Iterable[str] | DefaultType = Default,

            # A private/internal detail for generic base subclasses that want to also change the fields,
            # this prevents having to rebuild the class a second time; if this is True then the subclass
            # is responsible for calling rebuild when finished.
            ___PartialMeta__delay_rebuild: bool = False,

            **kwargs
    ):
        """

        Args:
            auto_partials: For more details see `pydantic_partials.config.PartialConfigDict.auto_partials`.
                If `Default`: Inherit behavior from parent/model_config; otherwise defaults to `True`.
                If `True` (default): Will automatically make all fields on the model `Partial`.
                If `False`: User needs to mark individual fields as `Partial` where they want.

            auto_partials_exclude: A set of strings of field names to exclude from automatic partials.
                If you explicitly mark a field as a Partial, this won't effect that. THis only effects
                automatically applied partial fields.

                You can also use `pydantic_partials.partial.AutoPartialExclude` to more easily mark fields as excluded.
                For more details see `pydantic_partials.config.PartialConfigDict.auto_partials_exclude`.

            **kwargs: Passed along other class arguments to Pydantic and any __init_subclass__ methods.
        """
        # Create the class first...
        cls: type[BaseModel] = super().__new__(cls, name, bases, namespaces, **kwargs)  # type: ignore

        # We now have the fields Pydantic found and can now easily add our MissingType's as needed.
        # Then a model_rebuild is forced to update the class schema to include the MissingType/LazyType annotations,
        # and any needed changes to the field default value.

        if auto_partials is not Default:
            cls.model_config['auto_partials'] = auto_partials

        if auto_partials_exclude:
            cls.model_config['auto_partials_exclude'] = set(auto_partials_exclude)

        final_auto_exclude = cls.model_config.get('auto_partials_exclude', set())
        for c in cls.__mro__:
            parent_config = getattr(c, 'model_config', set())
            if not parent_config:
                continue

            final_auto_exclude.update(parent_config.get('auto_partials_exclude', set()))

        need_rebuild = False

        partial_fields = set()
        for k, v in cls.model_fields.items():
            field_type = v.annotation
            origin = get_origin(field_type)
            if origin is None:
                if field_type is MissingType:
                    partial_fields.add(k)

            # TODO: Check that `field_type` is a union?
            for arg_type in get_args(field_type):
                if arg_type is MissingType:
                    partial_fields.add(k)

            for mdv in v.metadata:
                # If we find the marker AND we are not already marked as a partial_field,
                # add field to auto-exclude list.
                if mdv is AutoPartialExcludeMarker and k not in partial_fields:
                    final_auto_exclude.add(k)

        if final_auto_exclude:
            cls.model_config['auto_partials_exclude'] = final_auto_exclude

        final_partial_auto = cls.model_config.get('auto_partials', True)
        if final_partial_auto is not False:
            # I'll be putting in more options for `final_partial_auto` in the near future,
            # so just check for `is True` for now.
            if final_partial_auto is not True:
                raise ValueError(f'Invalid/Unknown `partial_auto` config value ({final_partial_auto}), use bool value.')

            for k, v in cls.model_fields.items():
                if k in partial_fields:
                    # The field is already a Partial
                    continue

                if k in final_auto_exclude:
                    # The field is excluded.
                    continue

                if v.default is PydanticUndefined and v.default_factory is None:
                    v.annotation = v.annotation | MissingType
                    partial_fields.add(k)
                    need_rebuild = True

        fields = cls.model_fields
        for k in partial_fields:
            v = fields[k]
            if v.default is PydanticUndefined and v.default_factory is None:
                v.default = Missing
                need_rebuild = True

        cls.model_partial_fields = partial_fields

        if need_rebuild and not ___PartialMeta__delay_rebuild:
            cls.model_rebuild(force=True)
        return cls

