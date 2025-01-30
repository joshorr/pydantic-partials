from datetime import datetime

import pytest

from pydantic_partials import Missing, AutoPartialModel
from pydantic import ValidationError, BaseModel

from pydantic_partials.partial import AutoPartialExclude


def test_doc_example__index__3():
    class TestModel(BaseModel):
        name: str
        value: str
        some_null_by_default_field: str | None = None

    class PartialTestModel(AutoPartialModel, TestModel):
        pass

    try:
        # This should produce an error because
        # `name` and `value`are required fields.
        TestModel()  # type: ignore
    except ValidationError as e:
        print(f'Pydantic will state `name` + `value` are required: {e}')
    else:
        raise Exception('Pydantic should have required `required_decimal`.')

        # We inherit from `TestModel` and add `AutoPartialModel` to the mix.

    # `PartialTestModel` can now be allocated without the required fields.
    # Any missing required fields will be marked with the `Missing` value
    # and won't be serialized out.
    obj = PartialTestModel(name='a-name')

    assert obj.name == 'a-name'
    assert obj.value is Missing
    assert obj.some_null_by_default_field is None

    # The `None` field value is still serialized out,
    # only fields with a `Missing` value assigned are skipped.
    assert obj.model_dump() == {
        'name': 'a-name', 'some_null_by_default_field': None
    }


def test_auto_excluded_inheritance_1():
    class TestModel(BaseModel):
        name: str
        value: str
        some_null_by_default_field: str | None = None

    class PartialTestModel(AutoPartialModel, TestModel):
        value: AutoPartialExclude[str]

    with pytest.raises(ValidationError, match=r'1 validation error.*\n *value *\n +Field required') as e_info:
        PartialTestModel()

    PartialTestModel(value='sss')


def test_auto_excluded_inheritance_w_sibling():
    class BaseRequired(BaseModel):
        id: AutoPartialExclude[str]
        created_at: AutoPartialExclude[datetime]

    class TestModel(BaseRequired):
        name: str
        value: str
        some_null_by_default_field: str | None = None

    class PartialTestModel(AutoPartialModel, TestModel):
        pass

    with pytest.raises(
            ValidationError,
            match=r'2 validation errors[\w\W]*'
                  r'id[\w\W]*Field required[\w\W]*'
                  r'created_at[\w\W]*Field required'
    ):
        PartialTestModel()

    PartialTestModel(id='sss', created_at=datetime.now())


def test_auto_excluded_inheritance_w_sibling_2():
    class PartialRequired(AutoPartialModel, auto_partials_exclude={'id', 'created_at'}):
        id: str
        created_at: datetime

    class TestModel(BaseModel):
        id: str
        created_at: datetime
        name: str
        value: str
        some_null_by_default_field: str | None = None

    class PartialTestModel(TestModel, PartialRequired):
        pass

    with pytest.raises(
            ValidationError,
            match=r'2 validation errors[\w\W]*'
                  r'id[\w\W]*Field required[\w\W]*'
                  r'created_at[\w\W]*Field required'
    ):
        PartialTestModel()

    PartialTestModel(id='sss', created_at=datetime.now())
