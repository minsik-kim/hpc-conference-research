# telemetry_observability.md

## Scope

Data collection, transport, storage/retention, and visualization of HPC system telemetry (node/job/fabric/storage/power metrics, logs, events) — the foundational data layer that anomaly detection, failure prediction, and RCA are built on. Includes log analytics/log intelligence as a telemetry data-source concern (11/31 corpus files reference log analytics/mining specifically; see `topics/root_cause_analysis.md` for log-based diagnosis techniques built on top of it).

## Operational problem

Production HPC centers must collect, retain, and make queryable very high-volume, high-cardinality telemetry (per-node, per-job, per-second in some cases) without overwhelming storage or the systems being monitored, while keeping enough fidelity and retention depth to support later diagnosis and research. **Telemetry collection and visualization alone is not AIOps** — see `DOMAIN_CONTEXT.md`'s maturity-stage model (collection → visualization → rule-based alerting → statistical anomaly detection → prediction → diagnosis/RCA → recommendation → automated remediation); this topic covers the earlier stages specifically.

## Research evidence currently in corpus

- `corpus/aiops-survey/synthesis/08_RESEARCH_PRESERVATION_REQUIREMENTS.md` [internal synthesis] — sets out what telemetry preservation (retention granularity, duration, provenance) is required to support later research; treat as a requirements/design document, not a peer-reviewed result.
- `corpus/aiops-survey/raw/V1_db_retention_sweep.md` [verification] — a literature sweep specifically on database/retention/rollup approaches for telemetry at this scale.
- `corpus/aiops-survey/raw/V7_nonenglish_indices.md` [verification] — includes a non-English-language (Korean/Chinese/Japanese) literature sweep that touches telemetry-adjacent indexing work.

## Production/practitioner evidence currently in corpus

- `corpus/aiops-survey/raw/H_centers.md` [PRACTITIONER] — 15+ center profiles describing their actual telemetry stacks (e.g., collection agents, storage backends, retention policy, dashboarding) as self-reported by the centers/vendors involved. This is production-practice evidence about specific sites, not a generalizable research result.
- `corpus/aiops-survey/raw/E_cug_vendor.md` [CUG/VENDOR] and `corpus/aiops-survey/synthesis/04_WORKSHOP_AND_CUG_CASES.md` [WORKSHOP/CUG] — CUG (Cray/HPE User Group) and vendor material describing telemetry-stack products and deployments.

## Known methods (generic domain background, not a corpus-specific claim)

Common telemetry-stack building blocks discussed across HPC operations literature and practice include: LDMS-family collectors, Prometheus/Grafana-style time-series stacks, vendor-specific counters (e.g., DCGM for GPU, Slingshot fabric counters), and log-shipping/indexing pipelines. Whether and how a *specific* one of these appears in this corpus should be checked against the actual document (`H_centers.md`, `E_cug_vendor.md`), not assumed from this general list.

## Research-practice gap

The corpus's explicit research-practice gap analysis (`synthesis/05_RESEARCH_PRACTICE_GAPS.md`) and the broader treatment in `09`/`13` cover whether academic telemetry-architecture research addresses what centers in `H_centers.md` actually report needing. See `research/RESEARCH_GAPS_AND_CANDIDATES.md`.

## Evidence limitations

Retention/collection-architecture literature review (`V1`) and grey-literature items (Slingshot admin-guide counters, LDMSCON proceedings — `V8_grey_isc.md`) are marked unresolved/partial in-source; see `OPEN_QUESTIONS.md`.

## Canonical deeper sources

`synthesis/08`, `raw/H_centers.md`, `raw/E_cug_vendor.md`, `raw/V1_db_retention_sweep.md`, `raw/V7_nonenglish_indices.md`, `raw/V8_grey_isc.md`.
