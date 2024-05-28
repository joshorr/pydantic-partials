from typing import Any---
title: Getting Started
---
## Getting Started

```shell
poetry install pydantic-lazy
```

or

```shell
pip install pydantic-lazy
```

Very basic example:

```python
from pydantic_lazy import LazyModel, Missing, Partial

class MyModel(LazyModel):
    some_attr: Partial[str]

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
assert obj.model_dump() == {}
```


## Lazily Fetch Fields

```python
from typing import Any
from pydantic_lazy import LazyModel, Missing, Partial

class MyModel(LazyModel):
    def model_resolve_missing(self, field_name: str) -> Any:
        # ... Lookup the `field_name` and return its value
        if field_name == 'some_attr':
            return "fetched"
        # You can also return Missing to indicate that it's still missing/unfetchable.
        return Missing
    some_attr: Partial[str]
    another_attr: Partial[int]

# Resolve function called whenever a Missing value would otherwise be returned.
assert MyModel().some_attr == 'fetched'
assert MyModel().another_attr is Missing
assert MyModel(some_attr='other-value').some_attr == 'other-value'

```
