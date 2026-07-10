## ADDED Requirements

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
