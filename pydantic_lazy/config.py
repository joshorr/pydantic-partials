from pydantic import ConfigDict


class PartialConfigDict(ConfigDict):
    partial_auto: bool
    """
    Defaults to True.
    
    If True: When class is created, all required attributes will be made partial, and their default set to `Missing`.
        This means that all attributes that don't have any default or default_factory defined will automatically have
        `MissingType` added to their annotation and field default set to `Missing`.
    
    If False: Class won't automatically add partial fields, adding them to individual fields will be up to the user.
        Keep in mind that in addition to adding the `MissingType` to the type-hint/annotation you'll also probably
        want to set the default value of the field to `Missing`; otherwise without a default value of some sort,
        a value will be required when validating the model object.
    """
