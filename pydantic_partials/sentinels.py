from xsentinels.sentinel import Sentinel
from pydantic.experimental.missing_sentinel import MISSING as _Pydantic_MISSING

# For backwards compatability + I don't really like all upper-case for sentential object (ie: `None`).
Missing = _Pydantic_MISSING
MissingType = Missing


class AutoPartialExcludeMarkerType(Sentinel):
    pass


AutoPartialExcludeMarker = AutoPartialExcludeMarkerType()
""" Used by `pydantic_partials.partial.AutoPartialExclude` to mark a field as excluded from automatic partials.
    See `pydantic_partials.config.PartialConfigDict.auto_partials_exclude` for more details.
"""
