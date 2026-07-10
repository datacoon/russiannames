## Context
`russiannames` performs exact-match lookups by a `text` key against three
datasets (`names`, `surnames`, `midnames`). Today those live in MongoDB and are
accessed via `find_one({'text': X})` in `parser.py`, and the datasets are built
by a MongoDB-heavy ETL in `processor.py`. The datasets are already exported to
Parquet (`data/parquet/*.parquet`) with schemas and row counts matching the
documented totals.

Verified facts (local inspection):
- DuckDB 1.4.2 and Python 3.13 available; datasets read cleanly.
- Row counts: `names` 32,134; `surnames` 375,449; `midnames` 48,274.
- Parquet schemas:
  - `names(count BIGINT, text VARCHAR, ethnic VARCHAR[], lett VARCHAR, gender VARCHAR)`
  - `surnames(count BIGINT, gender VARCHAR, ethnic VARCHAR[], f_form VARCHAR, fname VARCHAR, text VARCHAR)`
  - `midnames(count BIGINT, gender VARCHAR, ethnic VARCHAR[], lett VARCHAR, fname VARCHAR, text VARCHAR)`
- `ethnic` is a list column in Parquet — it maps directly to the list that
  `classify()` iterates over, and to the `ethnic` field parser reads.

Runtime fields actually consumed by `parser.py`: `text`, `count`, `gender`,
`ethnic`. The `fname`, `f_form`, `lett` fields are unused at runtime (ETL only).

## Goals / Non-Goals
- Goals:
  - Remove all MongoDB usage and the `pymongo` dependency.
  - Use the Parquet files as the DuckDB data source, bundled with the package.
  - Preserve `NamesParser.parse()` / `classify()` behavior and result shapes.
  - Achieve full Python 3 (3.9+) compatibility and modern packaging.
- Non-Goals:
  - Changing parsing heuristics, rule tables, or supported formats.
  - Re-deriving/cleaning the datasets' content (we reuse existing Parquet).
  - Adding a network/server mode or a new public API surface beyond an optional
    dataset-path configuration.

## Decisions

### Decision: Embedded DuckDB loaded from bundled Parquet
Introduce `russiannames/datastore.py` with a `NamesDatastore` class that:
- Opens an in-memory DuckDB connection (`duckdb.connect()`), no server.
- Loads each Parquet dataset into a native in-memory table on first use
  (`CREATE TABLE names AS SELECT * FROM read_parquet(<path>)`), then creates an
  ART index on `text` (`CREATE INDEX ... ON names(text)`) for fast point lookups.
- Exposes `find_one(dataset, text) -> dict | None` returning a row as a plain
  dict (column name → value), so `parser.py` keeps using `row['count']`,
  `row['gender']`, `row['ethnic']` unchanged.
- Uses parameterized queries (`WHERE text = ?`) to avoid quoting/injection issues.

Rationale: loading into native tables + index gives sub-millisecond point lookups
without a server, and keeps the parser's dict-based access pattern intact. Total
data is ~7 MB, trivial to hold in memory.

Alternatives considered:
- Query Parquet files directly per call without loading tables — simpler but each
  `find_one` scans Parquet; too slow for bulk parsing.
- Load into Python dicts and drop DuckDB entirely — fastest, but the requirement
  is explicitly to use DuckDB as the engine, and DuckDB keeps future SQL/ETL and
  the `ethnic` list handling clean.

### Decision: Dataset location resolution
Bundle the three Parquet files as package data at `russiannames/data/*.parquet`
and resolve them with `importlib.resources`. Allow overrides via:
1. `NamesParser(data_dir=...)` / `NamesDatastore(data_dir=...)` argument, then
2. `RUSSIANNAMES_DATA_DIR` environment variable, then
3. bundled package data (default).

Rationale: keeps zero-config usage working (`NamesParser()`), matches how the
BSON dump was shipped before, and supports custom/rebuilt datasets.

Note: `parser.py` currently constructs `MongoClient()` in `__init__`; the new
`NamesParser.__init__` will build a `NamesDatastore` instead. The public
constructor stays callable with no args.

### Decision: Rebuild the data pipeline without MongoDB
Rewrite `processor.py` (and fix `reader.py`) so the datasets can be regenerated
from raw sources into Parquet using DuckDB/pandas, replacing the `coll.save()` /
`find()` / `create_index()` MongoDB operations. Retire the `fullnames`
collection, which is not used at runtime. Fix Python 3 breakages: `str.decode`,
Py2 `cmp`-style `sorted(..., lambda x, y: ...)`, `.count()`, and the dead
`self.parse_name()` references.

Rationale: "remove all MongoDB dependencies" includes the ETL. Since valid
Parquet already exists, the pipeline becomes a reproducibility tool rather than a
blocker; runtime does not depend on it.

### Decision: Packaging & compatibility modernization
- Replace `setup.py` + `setup.cfg` metadata with a PEP 621 `pyproject.toml`
  (setuptools backend), including Parquet as package data.
- Dependencies: add `duckdb`; remove `pymongo`. Remove the unused `click` or wire
  the CLI to it — chosen approach: drop `click` and implement the CLI with the
  standard library `argparse`, exposed as a `rusnames` console-script entry point.
- Update classifiers to Python 3.9–3.13; drop 3.3–3.6 and Py2 artifacts.
- Clean up `u''` literals and Py2 print/encode idioms.
- Add a `pytest` suite covering documented `parse()` formats, gender values, and
  `classify()` examples from the README.

## Risks / Trade-offs
- In-memory load adds a one-time startup cost (~tens of ms) per process →
  acceptable; mitigated by lazy loading and per-process reuse of one datastore.
- DuckDB `text` values must match parser normalization (`.title()`, strip `.`).
  The Parquet `text` is already stored in the same normalized form MongoDB used,
  so lookups remain equivalent → covered by a cross-check test.
- Bundling ~7 MB of Parquet increases wheel size → acceptable and smaller than
  the previous BSON dump workflow.

## Migration Plan
1. Add `datastore.py` + bundle Parquet as package data (no behavior change yet).
2. Switch `parser.py` to use `NamesDatastore`; keep result dicts identical.
3. Remove `pymongo` from deps/imports; modernize packaging and CLI.
4. Rewrite `processor.py`/`reader.py` for Parquet + Python 3.
5. Add tests; run `scripts/cross-check.py` to confirm parity with prior behavior.
6. Update README/docs.

Rollback: revert to the previous commit; the MongoDB code path and BSON dump
remain in git history if a fallback is needed.

## Open Questions
- Should the rebuilt data pipeline live in the shipped package or move to a
  `tools/`/`scripts/` location excluded from the wheel? (Leaning: keep dataset
  build out of the runtime package; ship only the Parquet + reader.)
- Minimum supported Python version: proposed 3.9; confirm before finalizing.
