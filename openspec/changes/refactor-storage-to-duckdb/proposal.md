# Change: Migrate storage engine from MongoDB to DuckDB over Parquet

## Why
The library requires a running MongoDB server and a `mongorestore` step just to
parse a name, which is heavyweight and fragile for a mostly read-only lookup
workload. The reference datasets are already exported to Parquet, and DuckDB is
an embedded, zero-server analytical engine that reads Parquet natively. Moving to
DuckDB removes the external service dependency, simplifies installation, and lets
us ship the datasets directly with the package. The migration is also the moment
to retire lingering Python 2 code and modernize packaging so the project is fully
Python 3 compatible.

## What Changes
- **BREAKING**: Replace the MongoDB backend with an embedded DuckDB engine that
  reads the bundled Parquet datasets (`names`, `surnames`, `midnames`). No
  database server or `mongorestore` is required anymore.
- **BREAKING**: Remove the `pymongo` dependency and all MongoDB code paths from
  the runtime (`parser.py`) and the ETL/data pipeline (`processor.py`).
- Introduce a `name-datastore` capability: a small storage abstraction that loads
  Parquet into DuckDB and answers exact-match lookups by `text`, plus optional
  configuration of the dataset location.
- Preserve the existing public API and behavior of `NamesParser.parse()` and
  `NamesParser.classify()` (same inputs, same result dicts) on the new backend.
- Rebuild the data pipeline to produce the Parquet datasets without MongoDB and
  fix its Python 3 incompatibilities (byte/str handling, `sorted` cmp lambdas,
  removed pymongo APIs, broken/dead methods).
- Modernize packaging and compatibility: PEP 621 `pyproject.toml`, updated
  dependency set (`duckdb`; remove `pymongo`; drop or properly wire `click`),
  refreshed classifiers/Python version support, `u''` literal cleanup, and a
  pytest test suite.
- Update `README.md` and docs to describe the DuckDB/Parquet setup and remove the
  MongoDB installation instructions.

## Impact
- Affected specs (new capabilities): `name-datastore`, `name-parsing`,
  `name-classification`, `data-pipeline`, `packaging`
- Affected code:
  - `russiannames/parser.py` (swap MongoDB `find_one` calls for datastore lookups)
  - `russiannames/processor.py` (rewrite ETL to Parquet, remove MongoDB)
  - `russiannames/reader.py` (Python 3 fixes)
  - `bin/rusnames.py`, `scripts/cross-check.py` (CLI/tooling modernization)
  - `setup.py` / `setup.cfg` → `pyproject.toml`, `requirements.txt`
  - `README.md`, `docs/`
  - New: `russiannames/datastore.py`, `russiannames/data/*.parquet` (package data),
    `tests/`
- Data: Parquet files under `data/parquet/` become the source of truth; the BSON
  dump and MongoDB export artifacts are retired from the runtime path.
