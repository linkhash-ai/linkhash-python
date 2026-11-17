"""Strict decimal helpers for exact (e.g. monetary) arithmetic."""

from __future__ import annotations

from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation
from typing import Union

DecimalLike = Union[Decimal, int, str]


def to_decimal(value: DecimalLike) -> Decimal:
    """Convert ``value`` to a finite :class:`~decimal.Decimal`.

    Floats are rejected because binary floats cannot represent most decimal
    fractions exactly (``0.1 + 0.2 != 0.3``); pass a string instead.
    Booleans, NaN and infinities are rejected too.
    """
    if isinstance(value, bool) or not isinstance(value, (Decimal, int, str)):
        raise TypeError(
            f"expected Decimal, int or str, got {type(value).__name__}"
            + (" (use a string such as '12.34' instead of a float)" if isinstance(value, float) else "")
        )
    try:
        result = Decimal(value.strip() if isinstance(value, str) else value)
    except InvalidOperation:
        raise ValueError(f"not a decimal number: {value!r}") from None
    if not result.is_finite():
        raise ValueError(f"not a finite number: {value!r}")
    return result


def quantize(value: DecimalLike, places: int, rounding: str = ROUND_HALF_EVEN) -> Decimal:
    """Round ``value`` to ``places`` decimal places.

    Uses banker's rounding (half to even) by default; pass any
    :mod:`decimal` rounding constant, e.g. ``decimal.ROUND_HALF_UP``.
    """
    if isinstance(places, bool) or not isinstance(places, int) or places < 0:
        raise ValueError(f"places must be a non-negative int, got {places!r}")
    return to_decimal(value).quantize(Decimal(1).scaleb(-places), rounding=rounding)
