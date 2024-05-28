# Json Modeling Library

Provides easy way to map dict to/from Full-Fledged 'JsonModel' object.

![PythonSupport](https://img.shields.io/static/v1?label=python&message=%203.8|%203.9|%203.10|%203.11&color=blue?style=flat-square&logo=python)
![PyPI version](https://badge.fury.io/py/xmodel.svg?)

## Documentation

**[📄 Detailed Documentation](https://xyngular.github.io/py-xmodel/latest/)** | **[🐍 PyPi](https://pypi.org/project/xmodel/)**

## Getting Started

???+ warning "Alpha Software!"
    This is pre-release Alpha software, based on another code base and
    the needed changes to make a final release version are not yet
    completed. Everything is subject to change!


```shell
poetry install xmodel
```

or

```shell
pip install xmodel
```

Very basic example:

```python
from xmodel import JsonModel

class MyModel(JsonModel):
    some_attr: str

json_dict_input = {'some_attr': 'a-value'}    

obj = MyModel(json_dict_input)
assert obj.some_attr == 'a-value'

json_dict = obj.api.json()
assert json_dict == json_dict_input
```
