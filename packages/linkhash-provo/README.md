# linkhash-provo

**Provo**: payments toolkit by [Linkhash](https://github.com/linkhash-ai).

> **Status: early development (0.0.x).** The API may change without notice.

## Install

```bash
pip install linkhash-provo
```

## Usage

Convert between major-unit amounts and the integer minor units that payment
APIs use, with the correct ISO 4217 decimal places per currency:

```python
from linkhash import provo

provo.to_minor_units("12.34", "USD")   # 1234
provo.to_minor_units("1000", "JPY")    # 1000  (JPY has no minor unit)
provo.to_minor_units("1.234", "KWD")   # 1234  (KWD has 3 decimal places)
provo.from_minor_units(1234, "USD")    # Decimal('12.34')

provo.to_minor_units("12.345", "USD")  # ValueError: too precise, no silent rounding
provo.to_minor_units(12.34, "USD")     # TypeError: floats are rejected, pass a string

import decimal
provo.to_minor_units("12.345", "USD", rounding=decimal.ROUND_HALF_EVEN)  # 1234
```

## License

Apache-2.0. See [LICENSE](LICENSE).
