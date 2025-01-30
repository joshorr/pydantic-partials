- [Pydantic Partials](#pydantic-partials)
    * [Documentation](#documentation)
    * [Quick Start](#quick-start)
        + [Install](#install)
        + [Introduction](#introduction)
        + [Basic Example](#basic-example)
        + [Inheritable](#inheritable)
        + [Exclude Fields From Auto Partials](#exclude-fields-from-auto-partials)
        + [Auto Partials Configuration](#auto-partials-configuration)

# Pydantic Partials

An easy way to add or create partials for Pydantic models.

[![PythonSupport](https://img.shields.io/static/v1?label=python&message=%203.10|%203.11|%203.12|%203.13&color=blue?style=flat-square&logo=python)](https://pypi.org/project/pydantic-partials/)
[![PyPI version](https://badge.fury.io/py/pydantic_partials.svg?)](https://pypi.org/project/pydantic-partials/)

## Documentation

**[📄 Detailed Documentation](https://joshorr.github.io/pydantic-partials/latest/)** | **[🐍 PyPi](https://pypi.org/project/pydantic-partials/)**

[//]: # (--8<-- [start:readme])

## Important Upgrade from v1.x to 2.x Notes

I decided to make the default behavior of `PartialModel` not be automatic anymore.

I made a new class named `AutoPartialModel` that works exactly the same as the old v1.x `PartialModel` previously did.

To upgrade, simply replace `PartialModel` with `AutoPartialModel`, and things will work exactly as they did before.
The `auto_partials` configuration option is still present and if present will still override the base-class setting.

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

### Two Partial Base Class Options

There are two options to inherit from:

- `PartialModel`
  - With this one, you must explicitly set which fields are partial
  - To get correct static type checking, you also can also set a partial field's default value to `Missing`.
- `AutoPartialModel`
  - This automatically applies partial behavior to every attribute that does not already have a default value.


Let's first look at a basic example.

### Explicitly Defined Partials - Basic Example

Very basic example of a simple model with explicitly defined partial fields, follows:

```python
from pydantic_partials import PartialModel, Missing, Partial, MissingType
from pydantic import ValidationError

class MyModel(PartialModel):
    some_field: str
    partial_field: Partial[str] = Missing
    
    # Alternate Syntax:
    alternate_syntax_partial_field: str | MissingType = Missing
    

# By default, `Partial` fields without any value will get set to a
# special `Missing` type. Any field that is set to Missing is
# excluded from the model_dump/model_dump_json.
obj = MyModel(some_field='a-value')
assert obj.partial_field is Missing
assert obj.model_dump() == {'some_field': 'a-value'}

# You can set the real value at any time, and it will behave like expected.
obj.partial_field = 'hello'
assert obj.partial_field == 'hello'
assert obj.model_dump() == {'some_field': 'a-value', 'partial_field': 'hello'}

# You can always manually set a field to `Missing` directly.
obj.partial_field = Missing

# And now it's removed from the model-dump.
assert obj.model_dump() == {'some_field': 'a-value'}

# The json dump is also affected in the same way.
assert obj.model_dump_json() == '{"some_field":"a-value"}'

try:
    # This should produce an error because
    # `some_field` is a required field.
    MyModel()
except ValidationError as e:
    print(f'Pydantic will state `some_field` + `value` are required: {e}')
else:
    raise Exception('Pydantic should have required `some_field`.')
```

### Automatically Defined Partials - Basic Example

Very basic example of a simple model with automatically defined partial fields, follows:

```python
from pydantic_partials import AutoPartialModel, Missing

class MyModel(AutoPartialModel):
    some_attr: str
    another_field: str

# By default, automatic defined partial fields without any value will get set to a
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

With `AutoPartialModel`, you can inherit from a model to make an automatic partial-version of the inherited fields:

```python
from pydantic_partials import AutoPartialModel, Missing
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

class PartialTestModel(AutoPartialModel, TestModel):
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

### Exclude Fields from Automatic Partials (AutoPartialModel)

You can exclude specific fields from the automatic partials via these means:

- `AutoPartialExclude[...]`
  - This puts a special `Annotated` item on field to mark it as excluded.
- `class PartialRequired(PartialModel, auto_partials_exclude={'id', 'created_at'}):`
  - This way provides them via class argument `auto_partials_exclude`
- Or via the standard `model_config`
  - `model_config = {'auto_partials_exclude': {'id', 'created_at'}}`
  - A dict, using `auto_partials_exclude` as the key and a set of field names as the value.

Any of these methods are inheritable.
You can override an excluded value by explicitly marking a field as Partial via `some_field: Partial[str]`

Here is an example using the `AutoPartialExclude` method, also showing how it can inherit.

```python
from pydantic_partials import AutoPartialModel, AutoPartialExclude, Missing
from pydantic import BaseModel, ValidationError
from datetime import datetime
import pytest

class PartialRequired(AutoPartialModel):
    id: AutoPartialExclude[str]
    created_at: AutoPartialExclude[datetime]

class TestModel(BaseModel):
    id: str
    created_at: datetime
    name: str
    value: str
    some_null_by_default_field: str | None = None

class PartialTestModel(TestModel, PartialRequired):
    pass

# Will raise validation error for the two fields excluded from auto-partials
with pytest.raises(
    ValidationError,
    match=r'2 validation errors[\w\W]*'
          r'id[\w\W]*Field required[\w\W]*'
          r'created_at[\w\W]*Field required'
):
    # This should raise a 'ValidationError'
    PartialTestModel()  # type: ignore

# If we give them values, we get no ValidationError
obj = PartialTestModel(id='some-value', created_at=datetime.now())  # type: ignore

# And fields have the expected values.
assert obj.id == 'some-value'
assert obj.name is Missing
```

### Auto Partials Configuration

Normally you would simply inherit from either `PartialModel` or `AutoPartialModel`, depending on the desired behavior you want.

But you can also configure the auto-partials aspect via class paramters or the `model_config` attribute:

```python
from pydantic_partials import PartialModel, PartialConfigDict, AutoPartialModel

# `PartialModel` uses `auto_partials` as `False` by default, but we can override that if you want via class argument:
class TestModel1(PartialModel, auto_partials=True):
    ...

# Or via `model_config`
# (PartialConfigDict inherits from Pydantic's `ConfigDict`,
#  so you have all of Pydantic's options still available).
class TestModel2(AutoPartialModel):
    model_config = PartialConfigDict(auto_partials=False)
    ...
```

You can disable this automatic function. This means you have complete control of exactly which field 
can be partial or not.  You can use either the generic `Partial[...]` generic or a union with `MissingType`
to mark a field as a partial field.  The generic simple makes the union to MissingType for you.

```python
from pydantic_partials import PartialModel, Missing, MissingType, Partial
from decimal import Decimal
from pydantic import ValidationError

class TestModel(PartialModel):
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
