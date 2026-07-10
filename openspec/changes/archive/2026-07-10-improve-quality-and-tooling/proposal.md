# Change: Harden library quality, correctness, tooling and data hygiene

## Why
The v2.0.0 MongoDB→DuckDB migration is functionally complete, but a repository
review surfaced polish and correctness gaps that should be closed before a clean
release: a latent gender-resolution bug that clobbers explicitly-determined
genders, duplicated/dead rule tables, no continuous integration, stale docs and
project metadata, ~13 MB of duplicated/legacy data committed to git, and a
broken accuracy benchmark. Each item is low-risk and independently shippable, but
together they materially improve reliability and maintainability.

## What Changes
- Fix the gender-resolution logic in `parser.py` so an explicitly determined
  gender (e.g. the `Оглы`/`Кызы` branch, dataset match, or rule match) is not
  overwritten with the unresolved value `-` during subsequent re-derivation.
- Remove duplicated/dead rule tables in `consts.py` (the second
  `MIDDLENAME_POSTRULES` definition) and audit unused tables; replace the
  `from .consts import *` wildcard import with explicit names.
- Add **continuous integration**: run pytest across Python 3.9–3.13 plus a lint
  job on every push and pull request.
- Expose `NamesParser` from the package root (`from russiannames import NamesParser`)
  and ship inline type hints with a `py.typed` marker.
- Establish a **single source of truth** for the bundled datasets so
  `data/parquet/` and `russiannames/data/` cannot silently diverge.
- Make the accuracy benchmark (`scripts/cross-check.py`) runnable against
  committed inputs without a manual extraction step.
- Refresh documentation and metadata: update the stale `openspec/project.md`,
  fix the README surname-count inconsistency, and correct the docs/ReadTheDocs
  situation.
- Prune or relocate committed legacy artifacts (MongoDB BSON dump, `*.zst`
  exports, `norm.py`, `scripts/cross-check.zip`).

## Impact
- Affected specs: `name-parsing`, `packaging`, `data-pipeline`
- Affected code:
  - `russiannames/parser.py` (gender fix, explicit imports, type hints)
  - `russiannames/consts.py` (remove duplicate/dead rules)
  - `russiannames/__init__.py` (re-export `NamesParser`), new `russiannames/py.typed`
  - `pyproject.toml` (dev extras, `py.typed` package data), remove duplicate `flake8`/`setup.cfg` lint config
  - `scripts/cross-check.py` (read committed inputs)
  - `openspec/project.md`, `README.md`, `docs/`
  - New: `.github/workflows/ci.yml`
  - Data: de-duplicate `russiannames/data/` vs `data/parquet/`, prune legacy artifacts
- Tests: add coverage for gender preservation, single-token / 4-part formats,
  CLI invocation, and package-root import.
