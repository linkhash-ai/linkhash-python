"""Convert between major-unit amounts and integer minor units (ISO 4217).

Payment APIs usually exchange amounts as integers in the currency's minor
unit: 12.34 USD is ``1234`` (cents), 1000 JPY is ``1000`` (no minor unit),
1.234 KWD is ``1234`` (fils).
"""

from __future__ import annotations

from decimal import Decimal
from typing import Dict, Optional

from linkhash.core import DecimalLike, to_decimal

# ISO 4217 minor-unit exponents for active currency codes. Codes not listed
# here use 2 decimal places. Some payment processors deviate from ISO for a
# few currencies (e.g. ISK, HUF, TWD); check your processor's documentation.
_NON_DEFAULT_EXPONENTS: Dict[str, int] = {
    # 0 decimal places
    "BIF": 0, "CLP": 0, "DJF": 0, "GNF": 0, "ISK": 0, "JPY": 0, "KMF": 0,
    "KRW": 0, "PYG": 0, "RWF": 0, "UGX": 0, "UYI": 0, "VND": 0, "VUV": 0,
    "XAF": 0, "XOF": 0, "XPF": 0,
    # 3 decimal places
    "BHD": 3, "IQD": 3, "JOD": 3, "KWD": 3, "LYD": 3, "OMR": 3, "TND": 3,
    # 4 decimal places
    "CLF": 4, "UYW": 4,
}

_TWO_DECIMAL = frozenset(
    """
    AED AFN ALL AMD AOA ARS AUD AWG AZN BAM BBD BDT BMD BND BOB BOV BRL BSD
    BTN BWP BYN BZD CAD CDF CHE CHF CHW CNY COP COU CRC CUP CVE CZK DKK DOP
    DZD EGP ERN ETB EUR FJD FKP GBP GEL GHS GIP GMD GTQ GYD HKD HNL HTG HUF
    IDR ILS INR IRR JMD KES KGS KHR KPW KYD KZT LAK LBP LKR LRD LSL MAD MDL
    MGA MKD MMK MNT MOP MRU MUR MVR MWK MXN MXV MYR MZN NAD NGN NIO NOK NPR
    NZD PAB PEN PGK PHP PKR PLN QAR RON RSD RUB SAR SBD SCR SDG SEK SGD SHP
    SLE SOS SRD SSP STN SVC SYP SZL THB TJS TMT TOP TRY TTD TWD TZS UAH USD
    USN UYU UZS VED VES WST XCD XCG YER ZAR ZMW ZWG
    """.split()
)


def exponent(currency: str) -> int:
    """Return the number of minor-unit decimal places for ``currency``.

    ``currency`` is an ISO 4217 alphabetic code (case-insensitive).
    Raises :class:`ValueError` for unknown codes.
    """
    if not isinstance(currency, str):
        raise TypeError(f"currency must be a str, got {type(currency).__name__}")
    code = currency.strip().upper()
    if code in _NON_DEFAULT_EXPONENTS:
        return _NON_DEFAULT_EXPONENTS[code]
    if code in _TWO_DECIMAL:
        return 2
    raise ValueError(f"unknown ISO 4217 currency code: {currency!r}")


def to_minor_units(amount: DecimalLike, currency: str, *, rounding: Optional[str] = None) -> int:
    """Convert a major-unit ``amount`` to integer minor units.

    >>> to_minor_units("12.34", "USD")
    1234
    >>> to_minor_units("1000", "JPY")
    1000

    By default an amount with more precision than the currency allows raises
    :class:`ValueError` rather than silently losing money. Pass a
    :mod:`decimal` rounding constant (e.g. ``decimal.ROUND_HALF_EVEN``) to
    round instead.
    """
    places = exponent(currency)
    value = to_decimal(amount).scaleb(places)
    whole = value.to_integral_value(rounding=rounding) if rounding else value.to_integral_value()
    if rounding is None and whole != value:
        raise ValueError(
            f"{amount!r} has more than {places} decimal place(s) for {currency.strip().upper()}; "
            "pass rounding=... to round"
        )
    return int(whole)


def from_minor_units(minor: int, currency: str) -> Decimal:
    """Convert integer minor units back to a major-unit :class:`~decimal.Decimal`.

    >>> from_minor_units(1234, "USD")
    Decimal('12.34')
    """
    if isinstance(minor, bool) or not isinstance(minor, int):
        raise TypeError(f"minor must be an int, got {type(minor).__name__}")
    return Decimal(minor).scaleb(-exponent(currency))
