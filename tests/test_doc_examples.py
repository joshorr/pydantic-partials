

def test_doc_example__index__1():
    from pydantic_partials import PartialModel, Missing

    class MyModel(PartialModel):
        some_attr: str
        another_field: str

    # By default, Partial fields without any value will get set to a
    # special `Missing` type. Any field that is set to Missing is
    # excluded from the model_dump/model_dump_json.
    obj = MyModel()
    assert obj.some_attr is Missing
    assert obj.model_dump() == {}

    # You can set the real value at any time, and it will behave like expected.
    obj.some_attr = 'hello'
    assert obj.some_attr is 'hello'
    assert obj.model_dump() == {'some_attr': 'hello'}

    # You can always manually set a field to `Missing` directly.
    obj.some_attr = Missing

    # And now it's removed from the model-dump.
    assert obj.model_dump() == {}

    # The json dump is also affected in the same way.
    assert obj.model_dump_json() == '{}'

    # Any non-missing fields will be included when dumping/serializing model.
    obj.another_field = 'assigned-value'

    # After dumping again, we have `another_field` outputted.
    # The `some_attr` field is not present since it's still `Missing`.
    assert obj.model_dump() == {'another_field': 'assigned-value'}


def test_doc_example__index__2():
    from pydantic_partials import PartialModel, Missing, MissingType, Partial
    from decimal import Decimal
    from pydantic import ValidationError

    class TestModel(PartialModel, auto_partials=False):
        # Can use `Partial` generic type
        partial_int: Partial[int] = Missing

        # Or union with `MissingType`
        partial_str: str | MissingType

        required_decimal: Decimal

    try:
        TestModel()
    except ValidationError as e:
        print(f'Pydantic will state `required_decimal` is required: {e}')
    else:
        raise Exception('Pydantic should have required `required_decimal`.')

    obj = TestModel(required_decimal='1.34')

    # You can find out at any time if a field is missing or not:
    assert obj.partial_int is Missing
    assert obj.partial_str is Missing

    assert obj.required_decimal == Decimal('1.34')


def test_doc_example__index__3():
    from pydantic_partials import PartialModel, Missing
    from pydantic import ValidationError, BaseModel

    class TestModel(BaseModel):
        name: str
        value: str
        some_null_by_default_field: str | None = None

    try:
        # This should produce an error because
        # `name` and `value`are required fields.
        TestModel()
    except ValidationError as e:
        print(f'Pydantic will state `name` + `value` are required: {e}')
    else:
        raise Exception('Pydantic should have required `required_decimal`.')

        # We inherit from `TestModel` and add `PartialModel` to the mix.

    class PartialTestModel(PartialModel, TestModel):
        pass

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
