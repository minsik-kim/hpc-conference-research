# DOMAIN_INDEX — HPC & Quantum

Status: **PARTIAL** — one source project imported (`quantum-hpc-survey`);
domain scope is broader than current coverage (see `TOPIC_MAP.md`).

| Section | Path | Status |
|---|---|---|
| Topics | `topics/` | 7 topic files created; scope items with no source coverage were left without a file (see `TOPIC_MAP.md` §3) |
| Synthesis | `synthesis/` | routing index only — the actual synthesis documents remain in their canonical location under `corpus/quantum-hpc-survey/corpus/` (see `synthesis/README.md`) |
| Evidence audits | `evidence/` | routing index of evidence-grading conventions and known limitations carried from the source (`evidence/README.md`) |
| Implementation resources | `implementation/` | third-party artifact/code registry only — this domain's source project contains no implementation of its own (`implementation/ARTIFACT_REGISTRY.md`) |
| Research-gap documents | `research/` | source-reported `VENUE_GAP`/`POSSIBLE_CROSSOVER`/`OPEN_QUESTION` candidates, indexed with pointers, not re-falsified (`research/CANDIDATE_QUESTIONS.md`) |
| Corpus coverage | `corpus/` | one source project: `corpus/quantum-hpc-survey/` — 39 files preserved byte-identically from staging |

## Imported source projects

| Project | Path | Files | Scope |
|---|---|---|---|
| `quantum-hpc-survey` | `corpus/quantum-hpc-survey/` | 39 (11 corpus + 28 working-evidence) | SC 2024–2025 + ASPLOS 2024–2026 regular-paper censuses, 21-venue landscape map, QEC/simulation/compilation lineage synthesis |

## Catalog note

No per-paper entry has been added to the repository-wide `catalog/`
(`catalog/papers.yaml` does not exist yet for any domain — see
`catalog/README.md`). Per the governance instruction to avoid forcing a
large machine-readable citation catalog where the source does not already
have one, this domain's paper-level registry lives instead in
`corpus/quantum-hpc-survey/corpus/data/asplos/CORPUS.md` (the 36-paper
ASPLOS table) and the SC census's own master tables (§3.0, §4.0) — both
preserved from source. No new stable IDs (`governance/ID_NAMING_RULES.md`)
were assigned during this import; existing DOIs/titles in those tables
serve as identifiers for now. A future decision to build
`catalog/papers.yaml` for this domain should treat this as a starting
point, not redo it.
