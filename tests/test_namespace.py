"""Checks that every distribution shares the `linkhash` namespace cleanly.

Run with all packages installed together (see README).
"""

import importlib

import linkhash


def test_linkhash_is_a_namespace_package():
    # A regular package (one with linkhash/__init__.py) has __file__ set and
    # would hide the subpackages shipped by other distributions.
    assert getattr(linkhash, "__file__", None) is None
    assert len(list(linkhash.__path__)) >= 1


def test_all_subpackages_import_together():
    for name in ("linkhash.core", "linkhash.provo"):
        importlib.import_module(name)
    from linkhash import core, provo

    assert provo.to_minor_units("1.00", "USD") == 100
    assert core.quantize("1.005", 2) == core.to_decimal("1.00")
