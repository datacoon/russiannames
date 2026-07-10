## ADDED Requirements

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
