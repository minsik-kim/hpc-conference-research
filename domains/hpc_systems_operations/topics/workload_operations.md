# workload_operations.md

## Scope

Workload forecasting and characterization — understanding job/application behavior at the system level to inform scheduling, capacity planning, and anomaly baselines. 9/31 corpus files reference this explicitly (a narrower topic than scheduling itself).

## Operational problem

Characterizing and forecasting workload mix and demand (job arrival patterns, resource-usage profiles, application classes) accurately enough to inform scheduling policy and capacity decisions, without access to proprietary user code.

## Research evidence currently in corpus

- `corpus/aiops-survey/synthesis/02_PAPER_CENSUS.md` [internal census over external literature] — the largest single corpus document; includes workload-characterization papers within its broader SC/HPDC/IPDPS/Cluster/ISC/ACSOS/DSN/ISSRE census.
- `corpus/aiops-survey/raw/B_hpdc_ipdps_cluster_isc_acsos.md` [internal census] — the specific census slice covering HPDC/IPDPS/Cluster/ISC/ACSOS, the venues where workload-characterization work most often appears per the corpus's venue map.

## Production/practitioner evidence currently in corpus

Workload-characterization practice (as opposed to published research) is not separately profiled per-center in this corpus beyond what `raw/H_centers.md` [PRACTITIONER] reports incidentally as part of each center's operational description; there is no dedicated practitioner document for this topic.

## Known methods (generic domain background)

Trace-based workload characterization and time-series demand forecasting are the common method families in this space generally; the corpus's specific coverage of this literature is in `02` and `B`, not elaborated further here.

## Research-practice gap

Not given dedicated explicit framing in the corpus beyond the general treatment in `synthesis/05_RESEARCH_PRACTICE_GAPS.md`; see `research/RESEARCH_GAPS_AND_CANDIDATES.md`.

## Evidence limitations

This topic has the corpus's lowest explicit-framing hit count among the covered topics (9/31) — treat coverage here as narrower than `scheduling_resource_management` or `telemetry_observability`, and check `synthesis/02_PAPER_CENSUS.md` directly for depth before assuming broad coverage.

## Canonical deeper sources

`synthesis/02_PAPER_CENSUS.md`, `raw/B_hpdc_ipdps_cluster_isc_acsos.md`.
