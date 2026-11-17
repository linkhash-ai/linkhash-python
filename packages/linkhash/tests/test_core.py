from decimal import ROUND_HALF_UP, Decimal

import pytest

from linkhash.core import __version__, quantize, to_decimal


def test_version():
    assert __version__ == "0.0.1"


@pytest.mark.parametrize(
    ("value", "expected"),
    [("12.34", Decimal("12.34")), (" 7 ", Decimal("7")), (5, Decimal("5")), (Decimal("1.50"), Decimal("1.50"))],
)
def test_to_decimal(value, expected):
    assert to_decimal(value) == expected


@pytest.mark.parametrize("value", [0.1, True, None, [1]])
def test_to_decimal_rejects_types(value):
    with pytest.raises(TypeError):
        to_decimal(value)


@pytest.mark.parametrize("value", ["abc", "", "NaN", "Infinity"])
def test_to_decimal_rejects_values(value):
    with pytest.raises(ValueError):
        to_decimal(value)


def test_quantize_half_even_default():
    assert quantize("2.345", 2) == Decimal("2.34")
    assert quantize("2.355", 2) == Decimal("2.36")


def test_quantize_custom_rounding():
    assert quantize("2.345", 2, rounding=ROUND_HALF_UP) == Decimal("2.35")


def test_quantize_zero_places():
    assert quantize("10.5", 0) == Decimal("10")
    assert str(quantize(3, 2)) == "3.00"


@pytest.mark.parametrize("places", [-1, 1.5, True])
def test_quantize_rejects_bad_places(places):
    with pytest.raises(ValueError):
        quantize("1", places)
