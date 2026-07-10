## ADDED Requirements

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
