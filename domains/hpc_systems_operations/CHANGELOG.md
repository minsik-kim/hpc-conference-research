# CHANGELOG.md — hpc_systems_operations

## 2026-09-07 — Canonical import of AIOps survey corpus

**Added:**
- `corpus/aiops-survey/synthesis/` — 15 files, byte-identical import of the prior session's `out/00`–`13` + `README_INDEX.md`.
- `corpus/aiops-survey/raw/` — 16 files, byte-identical import of the prior session's `raw/A`–`H` + `V1`–`V8`.
- `DOMAIN_CONTEXT.md`, `DOMAIN_INDEX.md`, `TOPIC_MAP.md`, `RESEARCH_STATUS.md`, `OPEN_QUESTIONS.md` — replaced the `STRUCTURE_ONLY` placeholder content with a real canonical retrieval layer over the imported corpus.
- 14 topic files under `topics/`: `telemetry_observability.md`, `anomaly_detection.md`, `failure_prediction.md`, `root_cause_analysis.md`, `workload_operations.md`, `scheduling_resource_management.md`, `fabric_operations.md`, `storage_io_operations.md`, `gpu_operations.md`, `power_cooling.md`, `automated_remediation.md`, `operational_llm_agents.md`, `system_building.md`, `center_operations.md`.
- Routing documents: `synthesis/OVERVIEW.md`, `evidence/EVIDENCE_LINEAGE.md`, `evidence/SOURCE_TYPE_MAPPING.md`, `implementation/PRESERVATION_AND_EXPERIMENTS.md`, `research/RESEARCH_GAPS_AND_CANDIDATES.md`.

**Changed:**
- Domain status: `STRUCTURE_ONLY` → `IMPORTED` (this domain now has real corpus content; `ai_hpc_systems` and `hpc_quantum` were not touched and retain their own independent status).

**Closed questions:**
- None. This import performed no new literature search and resolved no item on the corpus's own unresolved-evidence watchlist.

**New questions:**
- None invented. All open items in `OPEN_QUESTIONS.md` are routed from the corpus's own self-reported watchlist (`synthesis/12_UNRESOLVED_EVIDENCE_AND_WATCHLIST.md`, `synthesis/13_VERIFICATION_ROUND2.md` §5).

**Revalidated:**
- Byte-identity of all 31 corpus files was verified against the staged copies (`~/Documents/hpc-conference-research-import/hpc_systems_operations/`) by SHA-256 diff — 0 mismatches. See the import task's final report for the full verification record.

**Provenance:**
- Source: Claude Cowork cloud-container session `/home/claude/aiops-survey`, staged via `~/Documents/hpc-conference-research-import/hpc_systems_operations/` (staging performed 2026-09-07, corpus authored 2026-09-06 per original file mtimes), imported into this canonical repository 2026-09-07.

`knowledge_as_of: 2026-09-06` (the corpus's own content date — nothing in the corpus reflects events or literature after this date; the canonical-layer documents added on top of it are dated 2026-09-07 but add no new findings).
