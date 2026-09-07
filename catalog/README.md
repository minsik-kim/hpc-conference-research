# catalog/

Machine-readable, cross-domain source metadata lives here.

Current state: **empty**. No `papers.yaml` exists yet in this repository —
none has been imported. When the AI/HPC systems corpus is imported from its
external workspace, its existing `papers.yaml` (if present there) should be
preserved as-is and become the canonical AI/HPC-systems paper metadata
source, per `CATALOG_SCHEMA.md` and `../governance/ID_NAMING_RULES.md`
(existing stable IDs must not be renumbered).

Planned files (not yet created):

- `papers.yaml` — canonical AI/HPC systems paper metadata (pending import)
- `sources.yaml` — cross-domain source metadata, once more than one domain
  has real content
- `CATALOG_SCHEMA.md` — schema definition (this directory)
- `MASTER_BIBLIOGRAPHY.md` — human-readable bibliography roll-up
- `references.bib` — BibTeX export
