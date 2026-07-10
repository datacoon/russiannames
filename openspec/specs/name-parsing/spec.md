# name-parsing Specification

## Purpose
TBD - created by archiving change refactor-storage-to-duckdb. Update Purpose after archive.
## Requirements
### Requirement: Full Name Parsing On DuckDB Backend
`NamesParser.parse(text)` SHALL parse a Russian full-name string into its
components using the DuckDB-backed datastore, preserving the existing result
contract. The returned dictionary SHALL always include `text` and `parsed`, and,
when a format is recognized, a `format` field plus the relevant component fields
(`sn`, `fn`, `mn`, and initial variants `sn_s`, `fn_s`, `mn_s`).

#### Scenario: Full surname-first-name-middlename
- **WHEN** `parse('Нигматуллин Ринат Ахметович')` is called
- **THEN** the result is `{'format': 'sfm', 'sn': 'Нигматуллин', 'fn': 'Ринат', 'mn': 'Ахметович', 'gender': 'm', 'text': 'Нигматуллин Ринат Ахметович', 'parsed': True}`

#### Scenario: Surname with initials
- **WHEN** `parse('Петрова C.Я.')` is called
- **THEN** the result has `format` `sFM`, `sn` `Петрова`, `fn_s` `C`, `mn_s` `Я`, `gender` `f`, and `parsed` True

#### Scenario: Unrecognized input
- **WHEN** `parse` is called with a string that matches no known format
- **THEN** the result includes `parsed: False` and echoes the original `text`

### Requirement: Public API And Zero-Config Construction Preserved
`NamesParser` SHALL remain constructible with no arguments and SHALL keep the
`parse` and `classify` methods as its public interface. Constructing the parser
SHALL NOT require any running database server.

#### Scenario: Default construction
- **WHEN** `NamesParser()` is instantiated with no arguments
- **THEN** it initializes successfully using the bundled datasets without contacting any server

#### Scenario: Optional dataset override
- **WHEN** `NamesParser` is constructed with an explicit dataset directory
- **THEN** parsing uses datasets from that directory

### Requirement: Gender Resolution Preserved
`parse` SHALL resolve `gender` using dataset records and the existing rule tables,
producing one of `m`, `f`, `u`, or `-`.

#### Scenario: Gender from datasets and rules
- **WHEN** a name is parsed whose components have gender information in the datasets or match gender rules
- **THEN** the resolved `gender` matches the value produced by the pre-migration behavior for the same input

### Requirement: Explicitly Determined Gender Is Preserved
`NamesParser.parse` SHALL preserve a definitive gender that an earlier parse
branch already established, and SHALL NOT reset it to the unresolved value.
Gender re-derivation logic SHALL only run when no definitive gender has been
established (gender is absent or unknown). The guarding condition SHALL be
written with explicit operator precedence so its intent is unambiguous. This
applies to genders established by the four-part honorific branch (Oghlu/Kyzy),
by a dataset match, or by a gender rule.

#### Scenario: Turkic male honorific preserved
- **WHEN** `parse('Алиев Гейдар Ага Оглы')` (a four-part name ending in `Оглы`) is called
- **THEN** the result has `format` `sfm` and `gender` `m`

#### Scenario: Turkic female honorific preserved
- **WHEN** `parse` is called with a four-part name ending in `Кызы`
- **THEN** the result has `format` `sfm` and `gender` `f`

#### Scenario: Dataset gender not regressed
- **WHEN** `parse('Нигматуллин Ринат Ахметович')` is called
- **THEN** the result still reports `gender` `m` as before the fix

### Requirement: NamesParser Importable From Package Root
The package SHALL expose `NamesParser` from the top-level `russiannames`
namespace so that `from russiannames import NamesParser` works, in addition to
the existing `from russiannames.parser import NamesParser`.

#### Scenario: Import from package root
- **WHEN** a user runs `from russiannames import NamesParser`
- **THEN** the import succeeds and returns the same class as `russiannames.parser.NamesParser`

