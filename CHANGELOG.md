# Changelog

## 2.0.0 (2026-07-10)

- Replaced the MongoDB backend with an embedded DuckDB engine over bundled
  Parquet datasets; no database server or `mongorestore` step required
- Removed the `pymongo` dependency and the unused `click` dependency
- Rewrote the dataset build pipeline (`processor.py`/`reader.py`) to be
  MongoDB-free and Python 3 compatible
- Modernized packaging (PEP 621 `pyproject.toml`), added a `rusnames` CLI
  entry point and a pytest test suite
- Requires Python 3.9+
- Fixed gender resolution so an explicitly determined gender (Оглы/Кызы, rule,
  or dataset match) is preserved instead of being reset
- Added inline type hints and a `py.typed` marker; `NamesParser` is now
  importable from the package root (`from russiannames import NamesParser`)
- Added GitHub Actions CI (pytest on Python 3.9–3.13 plus ruff lint) and
  consolidated linting on ruff
- Cleaned up rule tables (removed duplicate/dead entries), added a
  `make sync-data` step to keep bundled datasets in sync, and made the
  accuracy benchmark read its input directly from the committed archive

## 1.0.1 (2019-12-10)

- Fixed documentation makefile

## 1.0 (2019-03-03)

- First public release on PyPI and updated github code
