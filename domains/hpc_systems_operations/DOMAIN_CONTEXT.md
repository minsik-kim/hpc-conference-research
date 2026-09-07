# DOMAIN_CONTEXT.md — hpc_systems_operations

**Status: IMPORTED.** This domain now contains a real corpus. This file is the GPT/reader entry point for this domain — read it before `TOPIC_MAP.md`, before any `topics/*.md` file, and before answering any question routed here from `GLOBAL_CONTEXT.md`.

## Scope

HPC system building, production deployment, and operations; telemetry, monitoring, and observability; AIOps — anomaly detection, failure prediction, predictive maintenance, log intelligence, root-cause analysis; performance diagnosis and workload intelligence; scheduling and resource management; network/fabric operations; storage/I/O operations; GPU/AI-cluster operations; power/cooling/facility operations; automated remediation; operational LLM/agent use.

## What this domain's corpus actually is

The corpus (`corpus/aiops-survey/`) is **not** a set of externally authored conference papers. It is a **31-file internally authored research-survey project** (produced in a prior Claude Cowork session, imported here byte-identically) that surveys and audits the external literature and practitioner record on HPC AIOps/operations. It has two document roles, preserved as separate directories:

- `corpus/aiops-survey/synthesis/` (15 files, originally `out/00`–`13` + `README_INDEX.md`) — synthesis and deliverable documents: scope/taxonomy definitions, venue maps, paper census, precedent analyses, gap analyses, candidate lists, adversarial audits, rankings, experiment designs, a preservation-requirements document, an unresolved-evidence watchlist, and a second verification round.
- `corpus/aiops-survey/raw/` (16 files, `A`–`H` + `V1`–`V8`) — raw evidence documents. `A`–`H` is an initial literature/practitioner census; `V1`–`V8` is an independent **second-round verification** pass that re-checked and, in several places, corrected findings first reported in `A`–`H`.

This means the corpus is itself a layered research artifact — raw evidence → synthesis → adversarial audit → verification — not a flat literature collection. That layering is load-bearing for correctness and must not be flattened when answering questions (see "Evidence precedence" below).

The corpus is external/public-literature research only. **No internal KISTI operational data, non-public configuration, or site-specific material is present in this domain** — confirmed at staging time by an explicit filesystem check (see the staging phase's `SOURCE_INVENTORY.md` §"Internal/project-specific material"); this should not be added to the domain in a routine synthesis pass. The corpus does cite KISTI's own **externally published** domestic-conference/journal work as literature (discussed in `corpus/aiops-survey/synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` §9 and `synthesis/13_VERIFICATION_ROUND2.md` §2.8) — those are public citations, not internal design material, and are staged as ordinary corpus literature.

## Research-vs-practice-vs-vendor evidence model

**Source type matters in this domain. A practitioner deployment, a vendor presentation, a BoF statement, and an archival peer-reviewed result are not interchangeable evidence.** The corpus itself tags individual cited works with a publication-type taxonomy (`SC-TECHNICAL-PAPER`, `STATE-OF-PRACTICE`, `ARCHIVAL-PEER-REVIEWED`, `WORKSHOP-PEER-REVIEWED`, `POSTER`, `BOF`, `PANEL`, `TUTORIAL`, `PRACTITIONER`, `VENDOR`, `TECH-REPORT`) — these tags live **inside** the original 31 files, attached to hundreds of individual external citations, and were preserved verbatim, not re-tagged. See `evidence/SOURCE_TYPE_MAPPING.md` for how this in-corpus taxonomy relates to this repository's governance taxonomy (`governance/SOURCE_EVIDENCE_RULES.md`) — that file is a mapping/translation layer only; it does not change or re-tag anything inside the original documents.

When writing new canonical summaries in this domain (topic files, this file, etc.) that characterize a specific external source, use bracketed shorthand consistent with governance — `[ARCHIVAL]`, `[WORKSHOP]`, `[PRACTITIONER]`, `[VENDOR]`, `[BOF]`, `[POSTER]`, `[PANEL]`, `[TUTORIAL]`, `[TECH-REPORT]` — and never collapse these into an undifferentiated "paper." A center's own operational description of its telemetry stack (`raw/H_centers.md`) is production/practitioner evidence about what one site does, not a peer-reviewed research result about what works in general; a vendor's claim about a product is not an independently verified result until the corpus's own verification documents (`V1`–`V8`, `13`) say so.

**Telemetry ≠ AIOps.** The corpus and this domain distinguish operational maturity stages: data collection → visualization → rule-based alerting → statistical anomaly detection → prediction → diagnosis/RCA → recommendation → automated remediation. A center that collects and visualizes telemetry has not thereby done AIOps research, and a monitoring deployment is not described as "AIOps" or "ML-based" in this domain's canonical layer unless the corpus's own evidence supports that specific stage.

## Major topics (topics/)

Topic files exist only where the corpus has real, grep-verifiable evidence (see `TOPIC_MAP.md` for per-topic file-count evidence and `evidence/SOURCE_TYPE_MAPPING.md`/`SOURCE_INVENTORY`-style grounding). Currently:

`telemetry_observability`, `anomaly_detection`, `failure_prediction`, `root_cause_analysis`, `workload_operations`, `scheduling_resource_management`, `fabric_operations`, `storage_io_operations`, `gpu_operations`, `power_cooling`, `automated_remediation`, `operational_llm_agents`, `system_building`, `center_operations`.

`storage_io_operations` and `center_operations` were added beyond the initially sketched topic list because the imported corpus has substantial, grep-verified evidence for both (storage/I/O — Lustre — appears in 21/31 files; `raw/H_centers.md` alone is a 743-line, 15-center operational-profile document) — topic grouping follows filesystem evidence, not a fixed template.

## Important source classes inside the corpus

- **Venue/precedent analysis:** `synthesis/01_VENUE_MAP.md`, `synthesis/03_SC_REGULAR_PRECEDENTS.md` — SC/Tier-A/workshop/CUG structure and precedent for what gets accepted where.
- **Census (initial):** `raw/A_SC_main.md` through `raw/H_centers.md` — SC/HPDC/IPDPS/Cluster/ISC/ACSOS/DSN/ISSRE/workshop/CUG/vendor/center coverage.
- **Verification (second round):** `raw/V1`–`V8` — independently re-checked and in several cases corrected specific claims from `A`–`H` (e.g., a work's venue classification, a system's actual characterization).
- **Gap and candidate analysis:** `synthesis/05_RESEARCH_PRACTICE_GAPS.md`, `synthesis/06_INITIAL_SC_RESEARCH_CANDIDATES.md`, `synthesis/10_SC_CANDIDATE_RANKING.md`.
- **Adversarial audit:** `synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` — falsification-style audit of claims made in `00`–`07`.
- **Second verification round:** `synthesis/13_VERIFICATION_ROUND2.md` — corrects items first raised in `09`, and revises the candidate ranking.
- **Preservation requirements:** `synthesis/08_RESEARCH_PRESERVATION_REQUIREMENTS.md` — telemetry/provenance requirements for any future system-building work in this space.
- **Experiment designs:** `synthesis/11_INITIAL_EXPERIMENT_DESIGNS.md` — first-experiment designs with falsification criteria for the surviving candidates.
- **Unresolved-evidence watchlist:** `synthesis/12_UNRESOLVED_EVIDENCE_AND_WATCHLIST.md` — items the corpus itself flags as not yet resolved.

## Evidence precedence — later verification supersedes earlier synthesis

The corpus contains two real, in-source correction chains. **Neither chain was resolved by deleting or editing the earlier documents** — supersession is expressed as routing metadata only, per `governance/KNOWLEDGE_BASE_RULES.md` ("historical decisions are marked with status, never deleted").

1. **Synthesis chain:** `synthesis/00_SCOPE_AND_METHOD.md` through `synthesis/07_ANSWERS_TO_KEY_QUESTIONS.md` (initial synthesis) → `synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` (adversarial audit of `00`–`07`) → `synthesis/13_VERIFICATION_ROUND2.md` (corrects items first raised in `09`, revises the ranking from `10`). **`13` is the current authority; where `13` conflicts with `09`, and `09` conflicts with `00`–`07`, the later document wins.**
2. **Raw-evidence chain:** `raw/A`–`H` (initial census) → `raw/V1`–`V8` (independent second-round verification, which revises specific claims first made in `A`–`H`, e.g. PIKA's venue classification, CENTILE's characterization). **`V1`–`V8` is the current authority for the items each one addresses; `A`–`H` remains authoritative for everything the `V` documents did not re-examine.**

Full routing detail (which specific claims were revised, and by which document) is in `evidence/EVIDENCE_LINEAGE.md` — read that before treating any single claim from `00`–`09` or `A`–`H` as final if a `13` or `V1`–`V8` document also touches it.

## Known evidence gaps (unresolved — not to be closed by new search in this domain's routine maintenance)

- SC26 program content (ORNL paper full text/abstract) — `UNKNOWN` in-source (`raw/V2_sc26_ornl.md`).
- ICDE 2015–2026 literature sweep — not performed in-source.
- ModelX (HPDC 2025) — `TITLE-ONLY` evidence depth in-source.
- Several grey-literature items (LDMSCON 2023–2025 full text, Beacon+ full text, HPE Slingshot admin-guide counters) — unresolved in-source.
- KISTI internal technical reports (TRKO) — explicitly not yet searched, per the corpus's own statement.

See `RESEARCH_STATUS.md` and `OPEN_QUESTIONS.md` for the full routing of these. **Do not mark any of these resolved without an explicit new literature-search pass — this import performed none.**

## Retrieval instructions

Follow the chain: `GLOBAL_CONTEXT.md` → this file → `TOPIC_MAP.md` → the relevant `topics/<topic>.md` → the synthesis document(s) it cites in `corpus/aiops-survey/synthesis/` → the raw evidence/verification document(s) in `corpus/aiops-survey/raw/` it in turn cites. For any claim that is quantitative, contentious, about novelty ("no prior work does X"), or about a specific external paper's content, do not stop at a topic file or this file — follow the citation down to the deepest corpus document that actually makes the claim, and check `evidence/EVIDENCE_LINEAGE.md` for whether a later verification document revises it. If the deepest available corpus document itself marks a claim `UNKNOWN`, `TITLE-ONLY`, `SPECULATIVE`, or unresolved, report it that way — do not round it up to a settled fact.
