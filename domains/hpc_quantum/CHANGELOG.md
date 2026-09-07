# CHANGELOG — HPC & Quantum

## 2026-09-07 — Domain scaffold created

Added: `DOMAIN_CONTEXT.md`, `DOMAIN_INDEX.md`, `TOPIC_MAP.md`,
`RESEARCH_STATUS.md`, `OPEN_QUESTIONS.md`, this file. No content imported.
Status: `STRUCTURE_ONLY — CONTENT NOT YET IMPORTED`. Domain scoped to the
HPC × quantum-computing interface (not quantum computing generally); VQE
recorded as a topic within this domain rather than a top-level domain.

## 2026-09-07 — `quantum-hpc-survey` source project imported

Added:
- `corpus/quantum-hpc-survey/` — 39 files (11 curated corpus documents + 28
  raw working-evidence extracts) imported byte-identically from a
  previously staged copy (`~/Documents/hpc-conference-research-import/hpc_quantum/`).
  Preserved: `SOURCE_MANIFEST.md`, `SOURCE_INVENTORY.md`,
  `STAGING_CHECKSUMS.sha256` from the staging step.
- `synthesis/README.md` — routing index to the five synthesis documents
  that already exist inside the imported corpus (venue map, research
  queue, architecture lineages, SC census, ASPLOS census); no synthesis
  content was rewritten or duplicated.
- `evidence/README.md` — routing index to the corpus's own evidence-tag
  conventions, verification-pass appendices (ASPLOS census Appendix A, SC
  census Appendix D), and known evidence limitations.
- `implementation/ARTIFACT_REGISTRY.md` — provenance record (remote URL +
  HEAD commit) for nine third-party upstream repositories the source
  project's authors cloned for artifact verification; the repositories
  themselves (~800 MB) were **not** copied into this repository.
- `research/CANDIDATE_QUESTIONS.md` — an index, with exact file/line
  pointers, of the source's own inline `VENUE_GAP` (10),
  `POSSIBLE_CROSSOVER` (5), and `OPEN_QUESTION` (3) observations. All
  entries are `CANDIDATE` status; none was independently re-falsified
  through the `governance/RESEARCH_GAP_RULES.md` pipeline during this
  import.
- `topics/qec_decoding.md` (STRONG), `topics/quantum_simulation_distributed_gpu.md`
  (STRONG), `topics/compilation_and_classical_cost.md` (STRONG),
  `topics/benchmarking_and_artifacts.md` (STRONG),
  `topics/qpu_scheduling_and_orchestration.md` (MODERATE),
  `topics/modular_multi_qpu_architecture.md` (MODERATE),
  `topics/variational_algorithms_and_nisq.md` (PARTIAL, with an explicit
  non-comprehensive-VQE-coverage disclaimer). No topic file was created
  for a domain scope item with no coverage in this source (classical
  optimizer studies, initialization/warm-start, barren plateaus/
  trainability, gradient estimation, excited-state methods — all
  `NOT_COVERED`, see `TOPIC_MAP.md`).

Changed:
- `DOMAIN_CONTEXT.md`, `DOMAIN_INDEX.md`, `TOPIC_MAP.md`,
  `RESEARCH_STATUS.md`, `OPEN_QUESTIONS.md` — rewritten from
  `STRUCTURE_ONLY` scaffolding to reflect this domain's one imported
  source project. Status changed `STRUCTURE_ONLY` → `PARTIAL`.

Closed questions: n/a — no research-gap pipeline was run during this
import.

New questions: n/a — see `research/CANDIDATE_QUESTIONS.md` for the
source's own pre-existing candidates, now indexed but not newly generated.

Revalidated: The imported corpus's own SC and ASPLOS censuses were each
already independently verified by a separate adversarial pass *before*
this import (see `evidence/README.md`); this import performed no new
verification of their factual claims, only integrity verification of the
file transfer itself (byte-identical diff against the staged copy;
SHA-256 checksum match — see the domain's local commit for the exact
verification commands run).

Notes:
- This import step is a retrieval-layer construction, not new literature
  research. No web search or paper lookup was performed.
- The user's own `hpc-quantum-warmstart-paper` research project was not
  read, referenced, or merged into this domain.
- No per-paper stable IDs (`governance/ID_NAMING_RULES.md`) were assigned
  in this import; see `DOMAIN_INDEX.md` "Catalog note".
- No GitHub push was performed as part of this import.
