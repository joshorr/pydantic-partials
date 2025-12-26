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


class AutoPartialModel(PartialModel, auto_partials=True):
    pass
