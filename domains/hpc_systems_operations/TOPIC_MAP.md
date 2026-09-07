# TOPIC_MAP.md — hpc_systems_operations

**Status: IMPORTED.** Read `DOMAIN_CONTEXT.md` first. This file routes each topic to its canonical topic file and the corpus documents that actually support it. Coverage figures are grep-verified hit counts out of the corpus's 31 files (from the staging-phase `SOURCE_INVENTORY.md`), reproduced here as a coverage indicator only — not a claim of research depth or completeness.

| Topic | Coverage (files / 31) | Canonical topic file | Key source documents | Primary evidence types present |
|---|---:|---|---|---|
| Telemetry / monitoring / observability | 30 | `topics/telemetry_observability.md` | `synthesis/04_WORKSHOP_AND_CUG_CASES.md`, `synthesis/08_RESEARCH_PRESERVATION_REQUIREMENTS.md`, `raw/E_cug_vendor.md`, `raw/H_centers.md` | Practitioner (center stacks), vendor, workshop, some archival |
| Anomaly detection | 25 | `topics/anomaly_detection.md` | `synthesis/05_RESEARCH_PRACTICE_GAPS.md`, `raw/F_axes_ABC.md`, `raw/G_axes_DEFG.md`, `raw/V1`, `raw/V6` | Archival, workshop; verification revisions in `V1`/`V6` |
| Failure prediction | 16 | `topics/failure_prediction.md` | `raw/F_axes_ABC.md`, `raw/G_axes_DEFG.md`, `raw/V3_pika_tuncer.md` | Archival (PIKA, Tuncer) with `V3` correcting venue/characterization |
| Root cause analysis (RCA) | 28 | `topics/root_cause_analysis.md` | `raw/F_axes_ABC.md`, `raw/G_axes_DEFG.md`, `raw/V4_hindsight_suffbench.md`, `raw/V5_fdi_sensor_placement.md` | Archival, with `V4`/`V5` verification |
| Workload forecasting / characterization | 9 | `topics/workload_operations.md` | `synthesis/02_PAPER_CENSUS.md`, `raw/B_hpdc_ipdps_cluster_isc_acsos.md` | Archival (HPDC/IPDPS/Cluster/ISC) |
| Scheduling / resource management | 29 | `topics/scheduling_resource_management.md` | `synthesis/02_PAPER_CENSUS.md`, `raw/A_SC_main.md`, `raw/B_hpdc_ipdps_cluster_isc_acsos.md` | Archival, practitioner |
| Network / fabric operations (Slingshot) | 24 | `topics/fabric_operations.md` | `raw/E_cug_vendor.md`, `raw/H_centers.md`, `raw/V8_grey_isc.md` | Vendor, practitioner, CUG grey literature |
| Storage / I/O operations (Lustre) | 21 | `topics/storage_io_operations.md` | `raw/H_centers.md`, `synthesis/02_PAPER_CENSUS.md` | Practitioner, archival |
| GPU / AI-cluster operations (DCGM) | 19 | `topics/gpu_operations.md` | `raw/H_centers.md`, `raw/E_cug_vendor.md` | Vendor, practitioner |
| Power / cooling / facility operations | 24 | `topics/power_cooling.md` | `raw/H_centers.md`, `raw/E_cug_vendor.md` | Practitioner, vendor |
| Automated remediation | 24 | `topics/automated_remediation.md` | `synthesis/05_RESEARCH_PRACTICE_GAPS.md`, `raw/H_centers.md` | Practitioner, with archival gap analysis |
| Operational LLM / agent-assisted operations | 20 | `topics/operational_llm_agents.md` | `synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md`, `synthesis/13_VERIFICATION_ROUND2.md` | Mixed; heavily audited for novelty overclaim |
| System-building / production-deployment framing | 9 | `topics/system_building.md` | `synthesis/03_SC_REGULAR_PRECEDENTS.md`, `synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` | Precedent analysis, adversarial audit |
| Center operational profiles | n/a (single dedicated source) | `topics/center_operations.md` | `raw/H_centers.md` (15+ centers) | Practitioner (self-reported center architecture) |

Two areas were identified in the corpus but do not have a dedicated topic file, per "do not create empty files for weak evidence — but also do not duplicate a cross-cutting concern as if it were a topic":

- **Log analytics / log intelligence** (11/31 files) — folded into `topics/telemetry_observability.md` (a data-source/maturity-stage concern) and cross-referenced from `topics/root_cause_analysis.md` (a diagnosis-technique concern), rather than given its own file.
- **Research–practice gap framing** (explicit framing in 4/31 files; broader treatment throughout `09`/`13`) and **SC-regular-paper precedent framing** (17/31 files) — these are cross-cutting analytical lenses applied *across* the topics above, not a topic of their own. They are routed through `research/RESEARCH_GAPS_AND_CANDIDATES.md` and `synthesis/OVERVIEW.md` respectively.

For the evidence-precedence relationships referenced in each topic file (which synthesis document is superseded by which verification document), see `evidence/EVIDENCE_LINEAGE.md`.
