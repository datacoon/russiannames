# Changelog

## 2.0.0 (unreleased)

- Replaced the MongoDB backend with an embedded DuckDB engine over bundled
  Parquet datasets; no database server or `mongorestore` step required
- Removed the `pymongo` dependency and the unused `click` dependency
- Rewrote the dataset build pipeline (`processor.py`/`reader.py`) to be
  MongoDB-free and Python 3 compatible
- Modernized packaging (PEP 621 `pyproject.toml`), added a `rusnames` CLI
  entry point and a pytest test suite
- Requires Python 3.9+

## 1.0.1 (2019-12-10)

- Fixed documentation makefile

## 1.0 (2019-03-03)

- First public release on PyPI and updated github code
