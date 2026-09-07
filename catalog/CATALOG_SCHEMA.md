# CATALOG_SCHEMA

Schema notes for `catalog/papers.yaml` / `catalog/sources.yaml`, prepared
ahead of any actual import so that an import step has a schema to target.
No entries exist yet — this file defines shape, not content.

## Per-source fields (minimum)

- `id` — stable source ID (see `../governance/ID_NAMING_RULES.md`); never
  reused or renumbered once assigned
- `domain` — one of `ai_hpc_systems`, `hpc_systems_operations`,
  `hpc_quantum`
- `venue`, `year`
- `publication_type` — one of the values in
  `../governance/SOURCE_EVIDENCE_RULES.md`
- `title`, `authors`
- `analysis_file` — relative path to the corresponding `corpus/` analysis
- `topics` — list of topic slugs this source is referenced from

## Multi-domain extension

`sources.yaml` (not yet created) is reserved for cross-domain metadata once
more than one domain has real content, so that a single schema does not
have to be stretched to cover unrelated domains' fields. Its exact shape
is deferred until there is real multi-domain data to design it against —
do not pre-populate it with guessed fields.
