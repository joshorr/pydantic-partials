import typing

from pydantic import ConfigDict
from xsentinels.default import DefaultType, Default


class PartialConfigDict(ConfigDict, total=False):
    auto_partials: bool
    """
    Defaults to `True`.
    
    - If `True` (default): When class is created, all required attributes will be made `Partial`,
        and their default set to `Missing`. This means that all attributes that don't have any
        default or default_factory defined will automatically have `MissingType`/`LazyType` added
        to their annotation and field default set to `Missing`/`Lazy`.
        
        Default value will only be modified if it was not already set to something by the user.
        It needs to be modified if nothing is defined to ensure the field is not required.
        This allows Pydantic to create an instance of the model without a value defined
        for partial fields.
    
    - If `False`: Class won't automatically add `Partial` fields.
        Instead adding them to individual fields will be up to the user.
        
        The default value of any fields set by user to be `Partial` will still be adjusted
        unless the user already a default value defined by user for field.
        This ensures that Pydantic won't require the field be assigned a value.
    """

    auto_partials_exclude: set[str]
    """ A set of field names to exclude from the `auto_partials` functionality.
        
        All parent classes `partials_exclude` string sets will be combined
        together for a final exclusion list.
        
        Any partials set manually/directly via the fields annotation will still be a partial field
        regardless if it's referenced in this `auto_partials_exclude` set or not. This only effects
        the way automatic partials are applied.
        
        You can also use `pydantic_partials.partial.AutoPartialExclude` to more easily mark fields as excluded.
    """
