
def patch_missing_to_make_falsy():
    """ By default, Pydantic's `MISSING` is truthy.
        If you want it to be falsy instead, call this method to patch
        Sentinel typing-extension type to have a way to set the bool value,
        and then set MISSING to return False for it's bool value.

        This will make `MISSING`/`pydantic_partials.partial.Missing` return `False` for it's bool value,
        and therefore be 100% backwards-compatible with pydantic_partials v2.

        By default, MISSING will be left unpatched unless `patch_missing_to_make_falsy()` is explicit called.
    """
    from pydantic_core import MISSING
    from typing_extensions import Sentinel

    # Patch MISSING to return `False` boolean value.
    Sentinel._patch__bool_value = True
    Sentinel.__bool__ = lambda self: self._patch__bool_value
    MISSING._patch__bool_value = False


def remove_patch_missing_to_make_falsy():
    from pydantic_core import MISSING
    from typing_extensions import Sentinel

    # Remove the extra attributes.
    if hasattr(Sentinel, '_patch__bool_value'):
        del Sentinel._patch__bool_value
    if hasattr(MISSING, '_patch__bool_value'):
        del MISSING._patch__bool_value
    if hasattr(Sentinel, '__bool__'):
        del Sentinel.__bool__
