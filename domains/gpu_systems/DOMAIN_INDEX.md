# DOMAIN_INDEX — GPU Systems

Status: **PARTIAL** — 30 venue-years censused, 85 full-paper deep analyses;
coverage bounded by public full-text access, not by the screen.

| Section | Path | Status |
|---|---|---|
| Census | `census/` | 30 venue-year files (21 `COMPLETE_CENSUS`, 9 `PARTIAL_CENSUS`) + template. Population, source class, broad screen, seed reconciliation |
| Corpus | `corpus/` | 85 deep analyses + 11 cluster verdict ledgers + 2 templates. One analysis per paper that passed the full-paper gate |
| Topics | `topics/` | 12 topic files, one per taxonomy area (A/B, C/D, E, F, G, H/I, J/K, L/M, N, O, P, Q) |
| Synthesis | `synthesis/` | Master index, 5 lineage documents, cross-venue map, overlap registry, watchlist, methodology notes, integration answers |
| Evidence | `evidence/` | Evidence-tag conventions, uncertainty-marker inventory, access-limitation record (`evidence/README.md`) |
| Implementation | `implementation/` | Third-party artifact registry: 25 repositories pinned by commit hash (`implementation/ARTIFACT_REGISTRY.md`) |
| Research | `research/` | `CANDIDATE`-status observations with per-item pointers; none promoted to a research gap (`research/CANDIDATE_QUESTIONS.md`) |

## Build

One construction pass, 2026-09-18 → 2026-09-19, from public sources only. No
prior corpus was imported into this domain; nothing here was reconstructed from
a model's recollection of the literature. The eleven adjudication clusters ran
in parallel over disjoint stable-ID bands so that no ID could be reused.

## Catalog note

No per-paper entry was added to the repository-wide `catalog/`:
`catalog/papers.yaml` does not exist for any domain yet, and
`scripts/validate_catalog.py` / `scripts/build_indexes.py`, which
`governance/CONFERENCE_IMPORT_WORKFLOW.md` steps 5–7 call for, are not present
either (`scripts/README.md` is a placeholder). Those steps are recorded as
outstanding in `RESEARCH_STATUS.md` rather than skipped silently. This domain's
paper-level registry is `synthesis/GPU_MASTER_INDEX.md`, and its stable IDs
follow the domain-prefixed scheme that `governance/ID_NAMING_RULES.md` reserves
for new sources.
