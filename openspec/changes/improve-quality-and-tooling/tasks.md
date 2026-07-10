# Tasks

## 1. Correctness and tests
- [x] 1.1 Add regression tests for gender preservation: `Оглы` → `m`, `Кызы` → `f`, and the README `sfm` example (`tests/test_parser.py`)
- [x] 1.2 Fix the gender guard in `russiannames/parser.py`: add explicit parentheses and skip the `result['gender'] = '-'` reset when a definitive `m`/`f` was already set; re-derive only when gender is absent or `u`
- [x] 1.3 Add tests for single-token formats (`f`, `s`) and CLI invocation (`rusnames`)
- [x] 1.4 Add a test for `from russiannames import NamesParser`
- [x] 1.5 Confirm the full suite passes (`pytest`)

## 2. Code quality
- [x] 2.1 Remove the duplicate `MIDDLENAME_POSTRULES` definition in `russiannames/consts.py`; remove dead `NAME_POSTRULES` (kept `NAME_POSTFIXES`, used by `processor.py`)
- [x] 2.2 Replace `from .consts import *` in `parser.py` with explicit imports
- [x] 2.3 Clean up `u''` prefixes / other Py2 residue in `consts.py`
- [x] 2.4 Add type hints to the public API (`NamesParser.__init__`, `parse`, `classify`) and to `datastore.find_one`
- [x] 2.5 Add `russiannames/py.typed` and register it as package data in `pyproject.toml`
- [x] 2.6 Re-export `NamesParser` (and `__version__`) from `russiannames/__init__.py`

## 3. CI and tooling
- [x] 3.1 Add `.github/workflows/ci.yml`: test matrix py3.9–3.13 running `pytest`, plus a lint job
- [x] 3.2 Consolidate lint config on `ruff` in `pyproject.toml`; remove the duplicate bare `flake8` file and `setup.cfg` (flake8-only)
- [x] 3.3 Add a `dev` optional-dependencies group (`ruff`, `coverage`, `build`, `twine`) in `pyproject.toml`
- [x] 3.4 Update `Makefile` `lint`/`test` targets to match; remove the broken `docs` target

## 4. Data hygiene and benchmark
- [x] 4.1 Establish single source of truth: add `make sync-data` that regenerates `russiannames/data/*.parquet` from `data/parquet/*.parquet`; `dist` depends on it
- [x] 4.2 Make `scripts/cross-check.py` read its labelled input directly from `data/raw/data-distinct.zip` (no manual extraction) and report accuracy
- [x] 4.3 Remove/relocate legacy artifacts: removed tracked `data/bson/*.zip`; added untracked `*.zst`, `norm.py`, `scripts/cross-check.zip` to `.gitignore` (avoid irrecoverable deletion of untracked data)

## 5. Documentation and metadata
- [x] 5.1 Update `openspec/project.md` to reflect the completed DuckDB migration (remove MongoDB/`pymongo`/`click`, "no tests", Py2 references)
- [x] 5.2 Fix README surname-count inconsistency (`375449` verified) and recompute the whole stats table so rows sum to totals
- [x] 5.3 Resolve the docs situation: dropped `docs/` Sphinx setup + ReadTheDocs link, rely on README
- [x] 5.4 Reconcile documented ethnic keys (`jew`, `polsk`, `tur`, `slav`) with `consts.py` (added `ETNOS_JEW`, `ETNOS_POL`, `ETNOS_TUR`)

## 6. Validation
- [x] 6.1 `openspec validate improve-quality-and-tooling --strict` passes
- [x] 6.2 Tests green (24 passed); ruff clean; `python -m build` produces a wheel containing `py.typed` and the Parquet datasets
