# DOMAIN_INDEX.md — hpc_systems_operations

**Status: IMPORTED.** Structural index of everything in this domain. Read `DOMAIN_CONTEXT.md` first for how to use these pieces together.

**Path shorthand used throughout this domain's canonical-layer documents (`DOMAIN_CONTEXT.md`, `TOPIC_MAP.md`, `topics/*.md`, `evidence/*.md`, `synthesis/*.md`, `implementation/*.md`, `research/*.md`):** a bare `synthesis/NN_NAME.md` reference is shorthand for `corpus/aiops-survey/synthesis/NN_NAME.md`, and a bare `raw/X_name.md` (or bare `V1`–`V8`, `A`–`H`) reference is shorthand for `corpus/aiops-survey/raw/X_name.md`. This shorthand is used for readability once a document has already been introduced with its full path; it is not a separate, second copy of these files anywhere else in the domain. The only files that exist at these full paths are under `corpus/aiops-survey/`.

## 1. Topics (`topics/`)

14 topic files, each grounded in grep-verified corpus evidence (see `TOPIC_MAP.md` for per-topic coverage and source routing):

`telemetry_observability.md`, `anomaly_detection.md`, `failure_prediction.md`, `root_cause_analysis.md`, `workload_operations.md`, `scheduling_resource_management.md`, `fabric_operations.md`, `storage_io_operations.md`, `gpu_operations.md`, `power_cooling.md`, `automated_remediation.md`, `operational_llm_agents.md`, `system_building.md`, `center_operations.md`.

## 2. Synthesis (`synthesis/`)

Cross-topic routing/overview documents that index the corpus's own synthesis without duplicating it:

- `synthesis/OVERVIEW.md` — reading-order overview of `corpus/aiops-survey/synthesis/00`–`13`, restating the corpus's own `README_INDEX.md` reading order in canonical-layer terms and pointing to which topic each synthesis document feeds.

The actual synthesis content lives in `corpus/aiops-survey/synthesis/00_SCOPE_AND_METHOD.md` through `13_VERIFICATION_ROUND2.md` plus `README_INDEX.md` — this section indexes it, it does not re-derive it.

## 3. Evidence audits (`evidence/`)

- `evidence/EVIDENCE_LINEAGE.md` — the raw-evidence and synthesis correction chains (`A`–`H` → `V1`–`V8`; `00`–`07` → `09` → `13`), with explicit "later verification supersedes earlier synthesis" routing per claim area.
- `evidence/SOURCE_TYPE_MAPPING.md` — mapping table between the corpus's in-place publication-type taxonomy and this repository's `governance/SOURCE_EVIDENCE_RULES.md` taxonomy.

The actual audit content lives in `corpus/aiops-survey/synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` and `corpus/aiops-survey/synthesis/13_VERIFICATION_ROUND2.md`, and in `corpus/aiops-survey/raw/V1`–`V8`.

## 4. Implementation resources (`implementation/`)

- `implementation/PRESERVATION_AND_EXPERIMENTS.md` — routes to `corpus/aiops-survey/synthesis/08_RESEARCH_PRESERVATION_REQUIREMENTS.md` (telemetry/provenance preservation requirements for any future system-building work) and `corpus/aiops-survey/synthesis/11_INITIAL_EXPERIMENT_DESIGNS.md` (first-experiment designs with falsification criteria for the surviving research candidates).

## 5. Research-gap documents (`research/`)

- `research/RESEARCH_GAPS_AND_CANDIDATES.md` — routes to `corpus/aiops-survey/synthesis/05_RESEARCH_PRACTICE_GAPS.md` (gap table), `06_INITIAL_SC_RESEARCH_CANDIDATES.md` (initial 10-candidate list), `10_SC_CANDIDATE_RANKING.md` (first ranking), `13_VERIFICATION_ROUND2.md` (revised ranking — current authority), and `12_UNRESOLVED_EVIDENCE_AND_WATCHLIST.md` (unresolved items). Current open-question status lives in `OPEN_QUESTIONS.md`; this file routes to the source documents behind that status.

## 6. Corpus coverage (`corpus/`)

`corpus/aiops-survey/` — the full 31-file imported corpus, byte-identical to source:

- `corpus/aiops-survey/synthesis/` — 15 files (`00_SCOPE_AND_METHOD.md` … `13_VERIFICATION_ROUND2.md`, `README_INDEX.md`), originally staged as `out/`.
- `corpus/aiops-survey/raw/` — 16 files (`A_SC_main.md` … `H_centers.md`, `V1_db_retention_sweep.md` … `V8_grey_isc.md`), originally staged as `raw/`.

The original filenames are treated as the stable identifiers for these 31 documents (see `governance/ID_NAMING_RULES.md` — the `<VENUE><YY>-<NN>` per-paper ID scheme does not apply here, since these are internally authored survey/evidence documents, not individually cataloged external papers). No per-citation catalog (`sources.yaml`) was built in this import; hundreds of individual external citations remain embedded in these 31 files with their in-place tags, un-extracted. Extracting them into a structured catalog is a separate, future task, not performed here.
