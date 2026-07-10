## ADDED Requirements

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
