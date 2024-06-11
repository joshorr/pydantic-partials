- [Pydantic Partials](#pydantic-partials)
    * [Documentation](#documentation)
    * [Quick Start](#quick-start)
        + [Install](#install)
        + [Introduction](#introduction)
        + [Basic Example](#basic-example)
        + [Inheritable](#inheritable)
        + [Automatic Partials Configuration](#automatic-partials-configuration)

# Pydantic Partials

An easy way to add or create partials for Pydantic models.

![PythonSupport](https://img.shields.io/static/v1?label=python&message=%203.10|%203.11|%203.12&color=blue?style=flat-square&logo=python)
![PyPI version](https://badge.fury.io/py/xmodel.svg?)

## Documentation

**[📄 Detailed Documentation](https://joshorr.github.io/pydantic-partials/latest/)** | **[🐍 PyPi](https://pypi.org/project/pydantic-partials/)**

[//]: # (--8<-- [start:readme])

## Quick Start

### Install

```shell
poetry install pydantic-partials
```

or

```shell
pip install pydantic-partials
```

### Introduction

You can create from scratch, or convert existing models to be Partials.
The main purpose will be to add to exiting models, and hence the default
behavior of making all non-default fields partials (configurable).

Let's first look at a basic example.

### Basic Example

Very basic example of a simple model follows:

```python
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
```

By default, all fields without a default value will have the ability to be partial,
and can be missing from both validation and serialization.
This includes any inherited Pydantic fields (from a superclass).


### Inheritable

You can inherit from a model to make a partial-version of the inherited fields:

```python
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
    raise Exception('Field `required_decimal` should be required.')

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
```

Notice that if a field has a default value, it's used instead of marking it as `Missing`.

Also, the `Missing` sentinel value is a separate value vs `None`, allowing one to easily
know if a value is truly just missing or is `None`/`Null`.


### Automatic Partials Configuration

You can turn off automatically applying partials to all non-defaulted fields
via `auto_partials` class argument or modeL_config option:

```python
from pydantic_partials import PartialModel, PartialConfigDict

class TestModel1(PartialModel, auto_partials=False):
    ...

class TestModel2(PartialModel):
    model_config = PartialConfigDict(auto_partials=False)
    ...
```

You can disable this automatic function. This means you have complete control of exactly which field 
can be partial or not.  You can use either the generic `Partial[...]` generic or a union with `MissingType`
to mark a field as a partial field.  The generic simple makes the union to MissingType for you.

Example of disabling auto_partials:

```python
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
```


[//]: # (--8<-- [end:readme])
