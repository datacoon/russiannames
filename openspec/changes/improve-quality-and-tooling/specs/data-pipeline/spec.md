## ADDED Requirements

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
