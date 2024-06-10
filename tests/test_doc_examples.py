

def test_doc_example__index__1():
    from pydantic_partials import PartialModel, Missing, Partial

    class MyModel(PartialModel):
        some_attr: str
        another_field: str

    # By default, Partial fields without any value will get set to a special `Missing` type.
    # Any field that is set to Missing is excluded from the model_dump/model_dump_json
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

    # And now it's removed from the model-dump.
    assert obj.model_dump() == {'another_field': 'assigned-value'}


def test_doc_example__index__2():
    from pydantic_partials import PartialModel, Missing, MissingType, Partial, PartialConfigDict
    from decimal import Decimal
    from pydantic import ValidationError

    class TestModel(PartialModel, auto_partials=False):
        partial_int: Partial[int] = Missing
        partial_str: str | MissingType
        required_decimal: Decimal

    try:
        TestModel()
    except ValidationError as e:
        print(f'Pydantic will state `required_decimal` is required: {e}')
    else:
        raise Exception('Pydantic should have required `required_decimal`.')

    obj = TestModel(required_decimal='1.34')

    assert obj.partial_int is Missing
    assert obj.partial_str is Missing
    assert obj.required_decimal == Decimal('1.34')
