## ADDED Requirements

### Requirement: Embedded DuckDB Storage Engine
The library SHALL use an embedded DuckDB engine as its storage and query backend
and SHALL NOT require any external database server or restore step to operate.

#### Scenario: No server required
- **WHEN** a caller constructs the datastore with default settings
- **THEN** it opens an in-process DuckDB connection
- **AND** it does not attempt any network connection to a database server

#### Scenario: MongoDB is not used
- **WHEN** any runtime code path executes name lookups
- **THEN** no `pymongo`/MongoDB client is imported or invoked

### Requirement: Parquet-Backed Datasets
The datastore SHALL load its three reference datasets (`names`, `surnames`,
`midnames`) from Parquet files into DuckDB.

#### Scenario: Datasets loaded from Parquet
- **WHEN** the datastore initializes the `names`, `surnames`, and `midnames` datasets
- **THEN** each dataset is populated from its corresponding Parquet file
- **AND** the loaded row counts match the source Parquet files

#### Scenario: List-typed ethnic column preserved
- **WHEN** a row with an `ethnic` value is read
- **THEN** the `ethnic` value is returned as a list of ethnic keys

### Requirement: Exact-Match Lookup By Text
The datastore SHALL provide an exact-match lookup that returns a single record
for a given `text` key, or a null/None result when no record exists.

#### Scenario: Existing key returns a record
- **WHEN** `find_one('names', 'Николай')` is called
- **THEN** a record is returned exposing at least `text`, `count`, `gender`, and `ethnic`

#### Scenario: Missing key returns nothing
- **WHEN** a lookup is performed for a `text` value not present in the dataset
- **THEN** a null/None result is returned

#### Scenario: Lookups are safe against special characters
- **WHEN** a lookup value contains quote or SQL-significant characters
- **THEN** the query is parameterized so no SQL injection or query error occurs

### Requirement: Configurable Dataset Location
The datastore SHALL resolve the dataset location from an explicit argument, then
an environment variable, then bundled package data, in that order of precedence.

#### Scenario: Default bundled datasets
- **WHEN** the datastore is created with no location argument and no environment override
- **THEN** it loads the Parquet datasets bundled with the installed package

#### Scenario: Explicit override
- **WHEN** the datastore is created with an explicit dataset directory
- **THEN** it loads the Parquet datasets from that directory instead of the bundled ones
