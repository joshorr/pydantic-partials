import typing
from typing import Any, TypeVar, Annotated, TypeAlias

from pydantic import BaseModel

from .config import PartialConfigDict
from .meta import PartialMeta
from .sentinels import Missing, MissingType, AutoPartialExcludeMarker

from logging import getLogger

log = getLogger(__name__)


PM = TypeVar('PM')
Partial: TypeAlias = PM | MissingType
""" Can be used to manually mark a variable as Partial, which means it can have a `Missing`
    assigned to it. 
"""

PME = TypeVar('PME')
AutoPartialExclude = Annotated[PME, AutoPartialExcludeMarker]


class PartialModel(
    BaseModel,

    # Need metaclass to examine fields for missing type
    # and also to auto-add missing type if desired.
    metaclass=PartialMeta,

    # Needed so `Missing` default values will be validated and therefore the `PydanticOmit` will be
    # raised and inform Pydantic to ignore/omit the field value.
    validate_default=True
):
    """
    Class Args:

    - auto_partials: For more details see `pydantic_partials.config.PartialConfigDict.auto_partials`.
        - If `Default`: Inherit behavior from parent/model_config; otherwise defaults to `True`.
        - If `True` (default): Will automatically make all fields on the model `Partial`.
        - If `False`: User needs to mark individual fields as `Partial` where they want.
    """

    config_dict: typing.ClassVar[PartialConfigDict]

    def __init__(self, *args, **kwargs):
        """ Pydantic partial model class, with ability to easily dynamically omit fields when serializing a model.
        """
        super().__init__(*args, **kwargs)

    if not typing.TYPE_CHECKING:

        # We put `__getattr__` in a non-TYPE_CHECKING block because otherwise, mypy allows arbitrary attribute access
        def __getattr__(self, item: str) -> Any:
            try:
                return super().__getattr__(item)
            except AttributeError:
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


class AutoPartialModel(PartialModel, auto_partials=True):
    pass
