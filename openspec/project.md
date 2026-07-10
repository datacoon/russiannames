# Project Context

## Purpose
`russiannames` is a Python library that parses Russian full names (ФИО), identifies
the way a name is written (12 supported formats), infers a person's gender, and
provides experimental ethnic-affiliation classification. It ships with reference
datasets of ~375k surnames, ~32k first names, and ~48k patronymics (midnames).

## Tech Stack
- Python 3.9+
- DuckDB (embedded storage/query engine; no server required)
- Apache Parquet (reference datasets / data source for DuckDB)
- setuptools packaging via PEP 621 `pyproject.toml`
- ruff (lint/import sorting), pytest (tests)

## Project Conventions

### Code Style
- 4-space indentation, UTF-8, LF line endings (see `.editorconfig`)
- ruff with `line-length = 100`; lint config lives in `pyproject.toml`
- Prefer explicit, dependency-light implementations (standard library first)

### Architecture Patterns
- Small library with a thin public API:
  - `russiannames.parser.NamesParser.parse(text)` — parse a full name string
  - `russiannames.parser.NamesParser.classify(sn, fn, mn)` — gender + ethnicity
- Rule tables live in `russiannames/consts.py` (regex-based heuristics)
- Reference data is looked up by exact `text` key across three datasets:
  `names`, `surnames`, `midnames` (fields used at runtime: `text`, `count`,
  `gender`, `ethnic`), served by `russiannames/datastore.py` (embedded DuckDB
  over bundled Parquet).
- ETL (`processor.py`, `reader.py`) builds the datasets from frequency TSVs into
  Parquet; it is MongoDB-free and not part of the runtime hot path.

### Testing Strategy
- `pytest` suite under `tests/` covers parse formats, gender resolution,
  classification, the datastore round-trip, CLI invocation, and package-root
  import. Run via `make test` or `pytest`; CI runs the matrix on py3.9–3.13.
- `scripts/cross-check.py` provides an accuracy benchmark that reads its
  labelled input directly from `data/raw/data-distinct.zip`.

### Git Workflow
- `main` branch; feature branches per change.
- Only commit when explicitly requested.

## Domain Context
- Russian personal names have three components: surname (фамилия / `sn`),
  first name (имя / `fn`), patronymic (отчество / `mn`).
- Gender values: `m` (male), `f` (female), `u` (unknown), `-` (unresolved).
- Ethnic keys (experimental): `arab`, `arm`, `geor`, `germ`, `greek`, `jew`,
  `polsk`, `slav`, `tur`.

## Important Constraints
- Runtime name lookups must remain fast; the library is used for bulk parsing.
- Reference datasets are bundled with the package as Parquet files under
  `russiannames/data/`, kept in sync with the canonical `data/parquet/` via
  `make sync-data`.
- Must run with no external database server (embedded engine only).

## External Dependencies
- Runtime: `duckdb` (embedded analytical engine; no server required).
- Dev/test: `pytest`, `ruff`, `coverage`, `build`, `twine`
  (see the `dev` optional-dependencies group in `pyproject.toml`).
