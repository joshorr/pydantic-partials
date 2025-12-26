from pydantic_core import MISSING
from pydantic_partials.make_missing_falsy import patch_missing_to_make_falsy, remove_patch_missing_to_make_falsy


def test_patch_missing_to_make_falsy(is_missing_falsy):
    assert MISSING if not is_missing_falsy else not MISSING
    patch_missing_to_make_falsy()
    assert not MISSING
    remove_patch_missing_to_make_falsy()
    assert MISSING
