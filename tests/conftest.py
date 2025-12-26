import pytest
from pydantic_partials.make_missing_falsy import patch_missing_to_make_falsy, remove_patch_missing_to_make_falsy


@pytest.fixture(autouse=True, params=[True, False])
def is_missing_falsy(request):
    if not request.param:
        # Make sure we remove the patch, if needed.
        remove_patch_missing_to_make_falsy()
        yield request.param
        return

    patch_missing_to_make_falsy()
    yield request.param
    remove_patch_missing_to_make_falsy()

