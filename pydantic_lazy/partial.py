import typing
from typing import Any, get_args, get_origin, TypeVar

from pydantic import BaseModel

from pydantic._internal._model_construction import ModelMetaclass
from pydantic_core import PydanticUndefined
from xsentinels import Default
from xsentinels.default import DefaultType

from . import PartialConfigDict
from .missing import Missing, MissingType

from logging import getLogger

log = getLogger(__name__)


PM = TypeVar('PM')
Partial = PM | MissingType
""" Can be used to manually mark a variable as Partial, which means it can have a `Missing`
    assigned to it. 
"""

LM = TypeVar('LM')
Lazy = typing.Annotated[LM, Missing]
""" Can be used to manually mark a variable as Lazy, which means that if it's missing that
    the model can retrieved/resolved on-demand, lazily. If it can't be resolved an exception is raised.
"""


# metaclass to make all fields in a model optional, useful for PATCH requests
class _PartialMeta(ModelMetaclass):
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

    def __new__(
        cls,
        name: str,
        bases: tuple[type],
        namespaces: dict[str, Any],
        *,

        # If Default: Inherit behavior from parent/model_config.
        # If True (default): Will automatically make all fields on the model partials.
        # If False: User needs to mark individual fields as partial where they want.
        partial_auto: bool | DefaultType = Default,

        # A private/internal detail for generic base subclasses that want to also change the fields,
        # this prevents having to rebuild the class a second time.
        _PartialMeta__delay_rebuild: bool = False,

        # Pass along other class arguments to Pydantic and any __init_subclass__ methods.
        **kwargs
    ):
        # if 'all_partial' not in kwargs:
        #     kwargs['all_partial'] = True

        # Create the class first...
        cls: type[BaseModel] = super().__new__(cls, name, bases, namespaces, **kwargs)  # type: ignore

        # We now have the fields Pydantic found and can now easily add our MissingType's as needed.
        # Then a model_rebuild is forced to update the class schema to include the MissingType annotations.

        if partial_auto is not Default:
            cls.model_config['partial_auto'] = partial_auto

        need_rebuild = False
        if cls.model_config.get('partial_auto', True):
            for k, v in cls.model_fields.items():
                for e in v.metadata:
                    if e is Missing:
                        # todo: lazy vs partial???

                if v.default is PydanticUndefined and v.default_factory is None:
                    v.annotation = v.annotation | MissingType
                    v.default = Missing
                    need_rebuild = True

        _partial_fields = set()
        for k, v in cls.model_fields.items():
            field_type = v.annotation
            print(f'FieldType={field_type}')
            if get_origin(field_type) is None:
                if field_type is MissingType:
                    _partial_fields.add(k)
                continue

            for arg_type in get_args(field_type):
                if arg_type is MissingType:
                    _partial_fields.add(k)
                    break

        cls.model_partial_fields = _partial_fields

        if need_rebuild and not _PartialMeta__delay_rebuild:
            cls.model_rebuild(force=True)
        return cls


class PartialModel(
    BaseModel,

    # Need metaclass to examine fields for missing type
    # and also to auto-add missing type if desired.
    metaclass=_PartialMeta,

    # Needed so `Missing` default values will be validated and therefore the `PydanticOmit` will be
    # raised and inform Pydantic to ignore/omit the field value.
    validate_default=True
):
    def model_resolve_missing_lazy(self, field_name: str) -> Any:
        """
        Gives opportunity to resolve a Missing value for a Lazy field.
        By default, we don't know how to resolve anything, and so we will just return `Missing`,
        indicating it was unresolved.
        """
        # By default, we don't know how to resolve anything
        return Missing

    if not typing.TYPE_CHECKING:

        # We put `__getattr__` in a non-TYPE_CHECKING block because otherwise, mypy allows arbitrary attribute access
        def __getattr__(self, item: str) -> Any:
            try:
                return super().__getattr__(item)
            except AttributeError:
                if item in type(self).model_lazy_fields:
                    return self.model_resolve_missing_lazy(item)

                # Determine if value is 'Missing' or if we need to propagate the error...
                if item in type(self).model_partial_fields:
                    return Missing
                raise

        def __setattr__(self, key, value):
            # Right now, if a `raise PydanticOmit()` is done during validation while `validate_assignment=True` is on,
            # it will raise an error in Pydantic. I am assuming this is a bug,
            # because validation via `Model.model_validate()` works just fine when raising a `PydanticOmit`.
            # For now, as a work-around, I look for `Missing` values when set on object and ignore the set if found.
            #
            # Whenever a 'Missing' value is set, the user wants to ignore the field value, so we delete it if it exists.
            # I might rather keep the `Missing' value on the object, but there is currently
            # no easy way to exclude the value from the json output until they get something like this done:
            # https://github.com/pydantic/pydantic/discussions/5461#discussioncomment-7411977
            #
            # But on the other hand, I can use `def __getattr__` to lazily resolve any Missing values
            # instead of using __getattribute__; which is much more efficient... So I may stick with it in any case.
            # Lazily resolving would be for something like an ORM like object that wants to lazily lookup relationships.
            if value is Missing and key in type(self).model_partial_fields:
                try:
                    delattr(self, key)
                except AttributeError:
                    pass
            else:
                super().__setattr__(key, value)
