from decimal import ROUND_HALF_EVEN, ROUND_HALF_UP, Decimal

import pytest

from linkhash import provo
from linkhash.provo import exponent, from_minor_units, to_minor_units


def test_version():
    assert provo.__version__ == "0.0.1"


@pytest.mark.parametrize(
    ("code", "places"),
    [("USD", 2), ("eur", 2), (" JPY ", 0), ("KRW", 0), ("KWD", 3), ("BHD", 3), ("CLF", 4)],
)
def test_exponent(code, places):
    assert exponent(code) == places


@pytest.mark.parametrize("code", ["XXX", "US", "", "DOLLARS"])
def test_exponent_unknown(code):
    with pytest.raises(ValueError):
        exponent(code)


@pytest.mark.parametrize(
    ("amount", "code", "minor"),
    [
        ("12.34", "USD", 1234),
        ("12.3", "USD", 1230),
        (12, "USD", 1200),
        (Decimal("0.01"), "EUR", 1),
        ("1000", "JPY", 1000),
        ("1.234", "KWD", 1234),
        ("-5.50", "GBP", -550),
        ("0", "USD", 0),
    ],
)
def test_to_minor_units(amount, code, minor):
    assert to_minor_units(amount, code) == minor


def test_to_minor_units_rejects_excess_precision():
    with pytest.raises(ValueError, match="decimal place"):
        to_minor_units("12.345", "USD")
    with pytest.raises(ValueError):
        to_minor_units("1.5", "JPY")


def test_to_minor_units_rounding():
    assert to_minor_units("12.345", "USD", rounding=ROUND_HALF_EVEN) == 1234
    assert to_minor_units("12.345", "USD", rounding=ROUND_HALF_UP) == 1235


def test_to_minor_units_rejects_float():
    with pytest.raises(TypeError):
        to_minor_units(12.34, "USD")


@pytest.mark.parametrize(
    ("minor", "code", "amount"),
    [(1234, "USD", "12.34"), (1000, "JPY", "1000"), (1234, "KWD", "1.234"), (-550, "GBP", "-5.50")],
)
def test_from_minor_units(minor, code, amount):
    assert from_minor_units(minor, code) == Decimal(amount)


def test_from_minor_units_rejects_non_int():
    with pytest.raises(TypeError):
        from_minor_units(12.0, "USD")
    with pytest.raises(TypeError):
        from_minor_units(True, "USD")


@pytest.mark.parametrize("code", ["USD", "JPY", "KWD", "CLF"])
def test_round_trip(code):
    for minor in (0, 1, 99, 12345, -7):
        assert to_minor_units(from_minor_units(minor, code), code) == minor
