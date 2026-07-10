## Context
The library shipped a clean DuckDB/Parquet runtime in v2.0.0. This change is a
hardening pass: no new runtime capabilities, but correctness, CI, typing,
documentation accuracy, and repository hygiene. The base capabilities are still
described inside the pending `refactor-storage-to-duckdb` change (the
`openspec/specs/` tree is empty), so this proposal adds new, orthogonal
guarantees rather than modifying archived requirements.

## Goals / Non-Goals
- Goals: fix the gender-clobbering bug; add CI; ship type info; make docs and
  metadata accurate; stop dataset duplication; make the benchmark runnable;
  remove dead code and legacy artifacts.
- Non-Goals: changing the parsing algorithm's format detection, adding new name
  formats or ethnic keys, retraining/expanding datasets, or altering the public
  method signatures beyond adding type hints and a convenience import.

## Decisions

### Gender preservation (`parser.py:132`)
- Decision: Guard the re-derivation block with explicit parentheses and only run
  it when gender is unresolved. Concretely, treat a gender already set to `m`/`f`
  by an earlier branch as authoritative and skip the `result['gender'] = '-'`
  reset for those cases; re-derive only when gender is absent or `u`.
- Rationale: The current expression
  `if result and 'gender' not in result or (...)` binds `and` before `or`, so a
  branch that set `gender='m'` (e.g. `Оглы`) enters the block and is reset to
  `-`. Regression tests for `Оглы`/`Кызы` and the README example are added
  before the logic is touched.
- Alternatives considered: full rewrite of `parse()` into per-token helpers —
  deferred to a later refactor to keep this change low-risk and test-gated.

### Linting: consolidate on ruff
- Decision: Replace the duplicated flake8 config (bare `flake8` file + section in
  `setup.cfg`) with a single `ruff` configuration in `pyproject.toml`; run
  `ruff check` in CI. `black`-compatible formatting via `ruff format`.
- Rationale: One fast tool, one config location, satisfies the "single linter
  configuration" requirement. Existing `max-line-length = 100` is preserved.
- Alternative: keep flake8 but delete the duplicate file. Rejected: ruff is
  faster and folds in the pyupgrade/`u''` cleanup.

### Dataset single source of truth
- Decision: Keep `data/parquet/` as canonical source and generate
  `russiannames/data/*.parquet` via a `make sync-data` target (copy/symlink is
  not portable in wheels, so a copy step invoked by the build/`make dist`).
- Rationale: Prevents silent divergence while keeping the wheel self-contained
  (package data must be real files inside the package).
- Alternative: keep only one directory and have the ETL write straight into
  `russiannames/data/`. Viable; chosen approach preserves the existing
  `data/parquet/` archival location with an explicit sync step.

### Benchmark inputs
- Decision: Have `scripts/cross-check.py` read directly from
  `data/raw/data-distinct.zip` (open the CSV member in-memory) instead of
  requiring a pre-extracted CSV.
- Rationale: Avoids committing a second large uncompressed copy and removes the
  `FileNotFoundError` on a fresh checkout.

### CI matrix
- Decision: GitHub Actions, `.github/workflows/ci.yml`, matrix over py3.9–3.13,
  steps: install `.[test]`, run `pytest`; separate lint job runs `ruff check`.

### Legacy artifact handling
- Decision: Remove `data/bson/*.zip`, `data/jsonl/*.zst`, `data/jsonl/norm.py`,
  and `scripts/cross-check.zip` from the tree (history retains them). If any are
  still needed for reproducibility, document their provenance in the ETL README
  instead of committing binaries.

## Risks / Trade-offs
- Removing legacy binaries loses convenient in-tree access → mitigation: they
  remain in git history and can be re-added via release assets/LFS if needed.
- ruff adoption may surface many lint warnings → mitigation: fix or scope the
  initial ruleset conservatively (start with pyflakes + pyupgrade).
- Gender-logic change could alter outputs for edge cases → mitigation: add
  regression tests capturing current correct outputs before editing.

## Migration Plan
1. Land correctness + tests + CI (no packaging-visible break).
2. Land typing, package-root export, ruff consolidation.
3. Land docs/metadata refresh and data de-duplication/pruning.
No consumer API breakage; version can bump to 2.0.1 (or fold into the 2.0.0
release if unreleased).

## Open Questions
- Should legacy artifacts move to Git LFS / release assets rather than be
  deleted outright?
- Docs: restore Sphinx RST sources, or drop `docs/` + `make docs` and rely on
  the README?
