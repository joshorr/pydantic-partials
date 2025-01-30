from decimal import Decimal
from typing import Union, Annotated
import json

import pytest
from pydantic import model_validator, field_validator, ValidationError, ConfigDict
from pydantic.fields import FieldInfo, Field
from zoneinfo import ZoneInfo
import datetime as dt

from pydantic_partials.partial import PartialModel, Partial, AutoPartialModel

from pydantic_partials import PartialConfigDict
from pydantic_partials.sentinels import Missing, MissingType


# from pydantic_lazy.remote import RemoteModel
def utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def test_basic():
    class TestModel(AutoPartialModel):
        a: int
        b: Annotated['int | str', 2]
        c: Decimal
        d: dt.datetime | MissingType

    a = TestModel(a=Missing)

    assert a.a is Missing
    assert a.b is Missing
    assert a.c is Missing
    assert a.d is Missing

    a.a = 1
    assert a.a == 1

    a.a = Missing
    assert a.a is Missing

    # Make sure assigning it multiple times in a row is fine
    a.a = Missing
    a.a = Missing

    assert a.model_dump() == {}

    d_date = utc()

    a.d = d_date
    a.a = 2

    assert a.model_dump() == {'a': 2, 'd': d_date}
    assert a.model_dump_json() == f'{{"d":"{d_date.isoformat().replace("+00:00", "Z")}","a":2}}'


def test_select_fields():
    class TestModel(PartialModel, validate_assignment=True):
        a: Partial[int] = Missing
        b: Annotated['int | str', 2] | MissingType = Missing
        c: Decimal
        d: dt.datetime | MissingType = Missing

    class TestModelAutoViaConfig(TestModel):
        model_config = PartialConfigDict(auto_partials=True)

    a2 = TestModelAutoViaConfig()
    # Field `c` is a partial field via `auto_partials`, so this should work fine.
    a2.c = Missing

    class TestModel2(TestModel, auto_partials=True):
        e: Partial[str] = Missing

    a = TestModel(c='1.3')

    assert a.a is Missing
    assert a.b is Missing
    assert a.c == Decimal('1.3')
    assert a.d is Missing

    # Field `c` is not a partial field, so this should error out due to `validate_assignment=True`.
    with pytest.raises(ValidationError):
        a.c = Missing

    a.a = 1
    assert a.a == 1

    a.a = Missing
    assert a.a is Missing

    # Make sure assigning it multiple times in a row is fine
    a.a = Missing
    a.a = Missing

    assert a.model_dump() == {'c': Decimal('1.3')}

    d_date = utc()

    a.d = d_date
    a.a = 2

    assert a.model_dump() == {'a': 2, 'd': d_date, 'c': Decimal('1.3')}

    # Compare dicts so field/value order is irrelevant.
    assert json.loads(a.model_dump_json()) == {
        'a': 2,
        'd': d_date.isoformat().replace("+00:00", "Z"),
        'c': '1.3'
    }
