## 1. Datastore (DuckDB + Parquet)
- [x] 1.1 Add `duckdb` dependency and remove `pymongo` from the dependency set
- [x] 1.2 Bundle Parquet datasets as package data at `russiannames/data/{names,surnames,midnames}.parquet`
- [x] 1.3 Create `russiannames/datastore.py` with `NamesDatastore`:
  - [x] 1.3.1 Open an in-memory DuckDB connection
  - [x] 1.3.2 Lazily load each Parquet dataset into a native table and create an index on `text`
  - [x] 1.3.3 Resolve dataset location: explicit arg → `RUSSIANNAMES_DATA_DIR` → bundled package data (via `importlib.resources`)
  - [x] 1.3.4 Implement `find_one(dataset, text) -> dict | None` with parameterized queries, returning rows as dicts with `ethnic` as a list

## 2. Parser migration
- [x] 2.1 Replace `MongoClient()` init in `NamesParser.__init__` with `NamesDatastore` (keep no-arg construction; add optional `data_dir`)
- [x] 2.2 Replace every `ncoll/scoll/mcoll.find_one({'text': X})` in `parse()` with `datastore.find_one(...)`, preserving result dicts
- [x] 2.3 Replace the `find_one` calls in `classify()` and keep gender/ethnic aggregation identical
- [x] 2.4 Remove `from pymongo import MongoClient` and the `NAMES_DB` constant from `parser.py`
- [x] 2.5 Clean up `u''` literals and any Py2 idioms in `parser.py`

## 3. Data pipeline modernization (remove MongoDB)
- [x] 3.1 Rewrite `processor.py` to build the datasets into Parquet without MongoDB (DuckDB); retire the `fullnames` collection path
- [x] 3.2 Remove all `coll.save()`, `coll.remove()`, `find().count()`, `create_index()` and other pymongo calls
- [x] 3.3 Remove/replace dead references (`self.parse_name`) and fix `sorted(..., lambda x, y: ...)` cmp usages
- [x] 3.4 Fix `reader.py` Python 3 issues (drop `str.encode/decode`, fix `sorted` cmp lambda, text-mode UTF-8 I/O)
- [x] 3.5 Ensure `data/jsonl/norm.py` (or its replacement) is Python 3 compatible

## 4. Packaging & compatibility
- [x] 4.1 Add PEP 621 `pyproject.toml` (setuptools backend) with metadata, deps, and Parquet package-data config
- [x] 4.2 Remove/retire `setup.py`, `setup.cfg` legacy metadata and update `requirements.txt`
- [x] 4.3 Update classifiers/`requires-python` to Python 3.9+; drop 2.x and 3.3–3.6
- [x] 4.4 Modernize the CLI: implement `russiannames/cli.py` with `argparse` and expose a `rusnames` console-script entry point; drop unused `click`
- [x] 4.5 Modernize `scripts/cross-check.py` (remove bare `except:`, keep it runnable)

## 5. Tests
- [x] 5.1 Add `tests/` with `pytest`
- [x] 5.2 Cover documented `parse()` formats and the README examples (incl. gender values `m/f/u/-`)
- [x] 5.3 Cover `classify()` README examples (ethnics + gender)
- [x] 5.4 Add a datastore test (bundled datasets load; existing vs missing key lookup)
- [x] 5.5 Add a rebuild parity check that DuckDB consumes freshly built Parquet

## 6. Docs & cleanup
- [x] 6.1 Update `README.md`: remove MongoDB/`mongorestore` instructions; document DuckDB/Parquet + install/usage
- [x] 6.2 Update `docs/`/`HISTORY.rst` for the new backend and version bump
- [x] 6.3 Confirm no MongoDB code remains on the runtime path (BSON data kept in git history only)
- [x] 6.4 Update `tox.ini`/CI to test on supported Python 3 versions

## 7. Validation
- [x] 7.1 Run the test suite; confirm all pass (18 passed)
- [x] 7.2 Build the wheel and verify datasets are included and `NamesParser()` works from a clean install
- [x] 7.3 Run `openspec validate refactor-storage-to-duckdb --strict`
