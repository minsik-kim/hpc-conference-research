# scripts/

No validator or index-builder scripts exist yet in this repository.

Planned (not yet created):

- `validate_catalog.py` — validates `catalog/papers.yaml` /
  `catalog/sources.yaml` against `catalog/CATALOG_SCHEMA.md`
- `build_indexes.py` — rebuilds any `<!-- GENERATED — DO NOT EDIT MANUALLY -->`
  index files from the catalog

If equivalent scripts already exist in the external AI/HPC systems
workspace, they should be carried over and adapted to this repository's
path structure during the import step (see
`../governance/CONFERENCE_IMPORT_WORKFLOW.md`), preserving their existing
functionality rather than being rewritten from scratch.
