# linkhash

Shared core utilities for [Linkhash](https://github.com/linkhash-ai) Python libraries.

> **Status: early development (0.0.x).** The API may change without notice.

`linkhash` is the root of the `linkhash.*` namespace. Each Linkhash product
ships as its own distribution (for example `linkhash-provo` → `linkhash.provo`),
and this package provides `linkhash.core`, the helpers they share.

## Install

```bash
pip install linkhash
```

## Usage

Strict, exact decimal handling, suitable for money:

```python
from linkhash.core import quantize, to_decimal

to_decimal("12.34")      # Decimal('12.34')
to_decimal(0.1)          # TypeError: floats are rejected, pass a string
quantize("2.345", 2)     # Decimal('2.34')  (banker's rounding by default)
```

## License

Apache-2.0. See [LICENSE](LICENSE).
