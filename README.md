# linkhash-python

Open-source Python libraries by Linkhash. Every product ships as its own
PyPI distribution under the shared `linkhash.*` import namespace.

| PyPI | Import | Folder |
|---|---|---|
| [`linkhash`](https://pypi.org/project/linkhash/) | `linkhash.core` | [`packages/linkhash`](packages/linkhash) |
| [`linkhash-provo`](https://pypi.org/project/linkhash-provo/) | `linkhash.provo` | [`packages/linkhash-provo`](packages/linkhash-provo) |

## Layout rules

- `linkhash` is an **implicit namespace package**: no distribution may ship
  `src/linkhash/__init__.py`, or it would hide every other product's modules.
  `tests/test_namespace.py` enforces this.
- Each package is versioned and released independently; tag releases as
  `<distribution>/v<version>`, e.g. `linkhash-provo/v0.1.0`.
- Products depend on `linkhash` (core), never on each other's internals.

## Development

```bash
python -m venv .venv && . .venv/bin/activate
pip install pytest -e packages/linkhash -e packages/linkhash-provo
pytest packages tests
```

## License

Apache-2.0. See [LICENSE](LICENSE).
