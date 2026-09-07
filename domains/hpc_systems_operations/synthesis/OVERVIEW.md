# OVERVIEW.md — hpc_systems_operations synthesis

Routing document only. Restates the corpus's own `corpus/aiops-survey/synthesis/README_INDEX.md` reading order in canonical-layer terms, pointing to which topic(s) each document feeds. It does not duplicate or re-derive the synthesis documents' content.

| Order | Document | What it does | Feeds topics |
|---:|---|---|---|
| 1 | `00_SCOPE_AND_METHOD.md` | Defines scope, taxonomy (venue/discipline/practice tiers), evidence rules, method limits | All (foundational) |
| 2 | `01_VENUE_MAP.md` | Maps SC/Tier-A/workshop/CUG venue structure | `system_building`, all research-evidence sections |
| 3 | `02_PAPER_CENSUS.md` | Full paper census across covered venues (largest single document) | `workload_operations`, `scheduling_resource_management` |
| 4 | `03_SC_REGULAR_PRECEDENTS.md` | Precedent analysis for SC-regular/technical-paper acceptance | `system_building` |
| 5 | `04_WORKSHOP_AND_CUG_CASES.md` | Workshop and CUG operational case studies | `telemetry_observability`, `fabric_operations`, `power_cooling` |
| 6 | `05_RESEARCH_PRACTICE_GAPS.md` | Research-practice gap table | `automated_remediation`, cross-cutting (see `research/RESEARCH_GAPS_AND_CANDIDATES.md`) |
| 7 | `06_INITIAL_SC_RESEARCH_CANDIDATES.md` | Initial 10-candidate research list | `research/RESEARCH_GAPS_AND_CANDIDATES.md` |
| 8 | `07_ANSWERS_TO_KEY_QUESTIONS.md` | Direct answers to the project's originally posed key questions | Cross-cutting |
| 9 | `08_RESEARCH_PRESERVATION_REQUIREMENTS.md` | Telemetry/provenance preservation requirements | `implementation/PRESERVATION_AND_EXPERIMENTS.md` |
| 10 | `09_ADVERSARIAL_NOVELTY_AUDIT.md` | Adversarial falsification audit of claims in `00`–`07` | `operational_llm_agents`, `evidence/EVIDENCE_LINEAGE.md` |
| 11 | `10_SC_CANDIDATE_RANKING.md` | First candidate ranking (10 → 4 + 1 workshop-level item) | `research/RESEARCH_GAPS_AND_CANDIDATES.md` (superseded by `13`) |
| 12 | `11_INITIAL_EXPERIMENT_DESIGNS.md` | First-experiment designs with falsification criteria | `implementation/PRESERVATION_AND_EXPERIMENTS.md` |
| 13 | `12_UNRESOLVED_EVIDENCE_AND_WATCHLIST.md` | Watchlist of unresolved/unverified literature items | `OPEN_QUESTIONS.md` |
| 14 | `13_VERIFICATION_ROUND2.md` | Second verification round — corrections and revised ranking | `evidence/EVIDENCE_LINEAGE.md`, `research/RESEARCH_GAPS_AND_CANDIDATES.md` (current authority) |

**Reading order matters less than lineage.** A reader who only needs one specific claim should go through `TOPIC_MAP.md` → the relevant topic file → the specific document named there, then check `evidence/EVIDENCE_LINEAGE.md` for whether a later document revises it — not read `00`–`13` in sequence.
