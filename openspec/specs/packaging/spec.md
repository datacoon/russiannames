# packaging Specification

## Purpose
TBD - created by archiving change refactor-storage-to-duckdb. Update Purpose after archive.
## Requirements
### Requirement: Modern Dependency Set
The package SHALL declare `duckdb` as a runtime dependency and SHALL NOT declare
`pymongo`. Declared dependencies SHALL be limited to those actually imported by
the package.

#### Scenario: DuckDB replaces MongoDB
- **WHEN** the package metadata is inspected
- **THEN** `duckdb` is present in the runtime dependencies
- **AND** `pymongo` is absent

#### Scenario: No unused declared dependencies
- **WHEN** the declared runtime dependencies are compared against imports
- **THEN** every declared dependency is imported somewhere in the package

### Requirement: PEP 621 Packaging With Bundled Datasets
The package SHALL be built from a PEP 621 `pyproject.toml` and SHALL include the
Parquet reference datasets as package data so they are available after a normal
install.

#### Scenario: Datasets available after install
- **WHEN** the package is installed into a clean environment
- **THEN** `NamesParser()` can load its datasets without any additional download or restore step

#### Scenario: Declared Python support matches reality
- **WHEN** the package metadata declares supported Python versions
- **THEN** it targets Python 3.9+ and does not advertise unsupported versions (e.g. 2.x, 3.3–3.6)

### Requirement: Command-Line Interface
The package SHALL provide a working command-line entry point that parses a single
full-name argument and prints the parse result.

#### Scenario: CLI parses a name
- **WHEN** the CLI is invoked with a full-name string argument
- **THEN** it prints the parsed result dictionary for that name and exits successfully

### Requirement: Automated Test Suite
The project SHALL include an automated `pytest` test suite covering the documented
parse formats, gender values, and classification examples.

#### Scenario: Tests pass on supported Python
- **WHEN** the test suite is run on a supported Python 3 version
- **THEN** all tests pass

#### Scenario: Documented examples are covered
- **WHEN** the test suite runs
- **THEN** it asserts the README `parse` and `classify` example outputs

### Requirement: Continuous Integration On Supported Python Versions
The project SHALL provide a continuous-integration workflow that runs the
automated test suite and a lint check on every push and pull request, across all
supported Python versions (3.9 through 3.13). A failing test or lint check SHALL
mark the workflow as failed.

#### Scenario: Pull request runs the test matrix
- **WHEN** a pull request is opened or updated
- **THEN** CI runs `pytest` on Python 3.9, 3.10, 3.11, 3.12 and 3.13 and a lint job

#### Scenario: Failing tests block the workflow
- **WHEN** any test fails in CI
- **THEN** the workflow reports a failing status

### Requirement: Distributed Type Information
The package SHALL ship inline type hints for its public API (`NamesParser.parse`,
`NamesParser.classify`, and construction) and include a `py.typed` marker so that
downstream type checkers consume the annotations.

#### Scenario: Type marker is packaged
- **WHEN** the built wheel is inspected
- **THEN** it contains `russiannames/py.typed`

#### Scenario: Public API is annotated
- **WHEN** a type checker analyzes code calling `NamesParser().parse("...")`
- **THEN** the parameter and return types resolve from the package's own annotations

### Requirement: Single Linter Configuration
The project SHALL declare its lint configuration in exactly one location, with no
duplicated or conflicting linter config files.

#### Scenario: No duplicate lint config
- **WHEN** the repository lint configuration is inspected
- **THEN** there is a single authoritative configuration and no redundant duplicate

### Requirement: Accurate Documentation And Project Metadata
User-facing documentation and OpenSpec project context SHALL describe the current
DuckDB/Parquet architecture, and published dataset statistics SHALL be internally
consistent.

#### Scenario: Project context reflects current state
- **WHEN** `openspec/project.md` is read
- **THEN** it does not describe MongoDB/`pymongo`, transitional Py2/Py3 code, or an absence of automated tests as the current state

#### Scenario: README statistics are consistent
- **WHEN** the README surname counts in the feature list and the statistics table are compared
- **THEN** the two figures agree

#### Scenario: Documentation build references are valid
- **WHEN** the documentation configuration and links are inspected
- **THEN** either the docs build succeeds against present sources or the removed/unbuildable docs targets and dead links are removed

