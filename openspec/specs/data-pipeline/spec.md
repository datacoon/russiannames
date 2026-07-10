# data-pipeline Specification

## Purpose
TBD - created by archiving change refactor-storage-to-duckdb. Update Purpose after archive.
## Requirements
### Requirement: MongoDB-Free Dataset Build
The dataset build/ETL tooling SHALL produce the `names`, `surnames`, and
`midnames` datasets as Parquet files without using MongoDB or `pymongo`.

#### Scenario: Rebuild produces Parquet
- **WHEN** the dataset build tooling is run against raw source inputs
- **THEN** it writes `names`, `surnames`, and `midnames` Parquet files
- **AND** it performs no MongoDB operations

#### Scenario: Rebuilt datasets are consumable
- **WHEN** the datastore is pointed at freshly rebuilt Parquet files
- **THEN** `NamesParser` loads and queries them successfully

### Requirement: Python 3 Compatible Tooling
All ETL and helper tooling (`processor.py`, `reader.py`, and scripts) SHALL run
under supported Python 3 versions without Python 2 idioms or removed APIs.

#### Scenario: No Python 2 byte/str idioms
- **WHEN** tooling reads or writes text files
- **THEN** it uses text-mode I/O with explicit UTF-8 encoding and does not call `str.decode`/`str.encode` on `str` objects

#### Scenario: No removed database APIs or dead references
- **WHEN** the tooling modules are imported and executed
- **THEN** they do not call removed pymongo methods (`save`, `remove`, `find().count()`) and contain no references to non-existent methods

### Requirement: Single Source Of Truth For Bundled Datasets
The bundled package datasets under `russiannames/data/` SHALL be derived from the
canonical dataset directory (`data/parquet/`) rather than maintained as an
independent, manually-copied duplicate, so that the runtime datasets and the
build inputs cannot silently diverge.

#### Scenario: Bundled datasets are regenerated from canonical source
- **WHEN** the datasets are rebuilt or synced
- **THEN** `russiannames/data/*.parquet` is produced from `data/parquet/*.parquet` by a documented, repeatable step

#### Scenario: No undocumented divergence
- **WHEN** the canonical datasets change
- **THEN** the bundled package datasets are updated by the same step rather than by an independent manual edit

### Requirement: Runnable Accuracy Benchmark
The accuracy benchmark script SHALL run against inputs committed to the
repository without requiring a manual, undocumented extraction step, and SHALL
report gender-classification accuracy.

#### Scenario: Benchmark runs from repository inputs
- **WHEN** the accuracy benchmark is executed on a fresh checkout
- **THEN** it reads its labelled input from committed data (or extracts it automatically) and completes without a `FileNotFoundError`

