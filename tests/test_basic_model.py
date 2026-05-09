from decimal import Decimal
from typing import Annotated
import json

import pytest
from pydantic import ValidationError, computed_field, Field, BaseModel
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
    assert a.model_dump_json() == f'{{"a":2,"d":"{d_date.isoformat().replace("+00:00", "Z")}"}}'


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


def test_explicitly_defined():
    class TestModel(PartialModel):
        attr_1: str
        attr_2: Partial[str] = Missing

    obj = TestModel(attr_1='value-1')
    out = obj.model_dump_json()
    assert out == '{"attr_1":"value-1"}'


def test_pre_existing_exclude_if_still_consulted():
    IntZeroOrMissing = Annotated[int | MissingType, Field(exclude_if=lambda v: v is Missing)]

    class TestModel(PartialModel):
        attr_1: IntZeroOrMissing
        attr_2: Partial[str] = Missing

    obj = TestModel(attr_1=1)
    out = obj.model_dump_json()


def test_computed_fields_excluded_when_missing():
    class Model(AutoPartialModel):
        # You could add 'MissingType' (ie: 'int | MissingType) as a return type if you want,
        # but it is not necessary for it to work.
        @computed_field()
        def a_computed_field(self) -> int | MissingType:
            return Missing

        h: int = 1

    obj = Model()
    assert obj.model_dump() == {"h": 1}


def test_computed_fields_excluded_when_missing__with_pre_existing_exclude_if():
    class Model(AutoPartialModel):
        # You could add 'MissingType' (ie: 'int | MissingType) as a return type if you want,
        # but it is not necessary for it to work.
        @computed_field(exclude_if=lambda v: v is 0)
        def a_computed_field(self) -> int | MissingType:
            return self.h

        h: int | MissingType = 1

    obj = Model()
    assert obj.model_dump() == {"h": 1, 'a_computed_field': 1}

    obj.h = 0
    assert obj.model_dump() == {"h": 0}

    obj.h = Missing
    assert obj.model_dump() == {}
