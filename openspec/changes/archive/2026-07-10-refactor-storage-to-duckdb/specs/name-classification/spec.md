## ADDED Requirements

### Requirement: Gender And Ethnic Classification On DuckDB Backend
`NamesParser.classify(sn, fn, mn)` SHALL infer a person's gender and ethnic
affiliations from the surname, first name, and patronymic using the DuckDB-backed
datastore and the existing rule tables, returning a dictionary with an `ethnics`
list and, when determinable, a `gender` value.

#### Scenario: Turkic male full name
- **WHEN** `classify('Нигматуллин', 'Ринат', 'Ахметович')` is called
- **THEN** the result is `{'ethnics': ['tur'], 'gender': 'm'}`

#### Scenario: Slavic female full name
- **WHEN** `classify('Алексеева', 'Ольга', 'Ивановна')` is called
- **THEN** the result is `{'ethnics': ['slav'], 'gender': 'f'}`

### Requirement: Ethnic Aggregation From List Column
`classify` SHALL aggregate ethnic keys from the `ethnic` list values of matched
records without duplicates, preserving first-seen order.

#### Scenario: Deduplicated ethnic aggregation
- **WHEN** multiple matched records contribute overlapping ethnic keys
- **THEN** the returned `ethnics` list contains each key once, in first-seen order

#### Scenario: Gender falls back past unknown
- **WHEN** the most frequent gender vote is `u` and another gender vote exists
- **THEN** the returned `gender` is the next most frequent non-`u` value
