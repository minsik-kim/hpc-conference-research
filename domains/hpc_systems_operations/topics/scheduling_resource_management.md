# scheduling_resource_management.md

## Scope

Job scheduling and resource-management research and practice for HPC systems. 29/31 corpus files reference scheduling — the second-highest-coverage topic in the corpus after telemetry.

## Operational problem

Allocating heterogeneous, contended compute/fabric/storage resources to a mixed job workload to meet throughput, fairness, and (increasingly) energy/power constraints, while incorporating operational signals (health, predicted failure) into scheduling decisions.

## Research evidence currently in corpus

- `corpus/aiops-survey/synthesis/02_PAPER_CENSUS.md` [internal census] — scheduling-relevant papers within the full venue census.
- `corpus/aiops-survey/raw/A_SC_main.md` [internal census] and `raw/B_hpdc_ipdps_cluster_isc_acsos.md` [internal census] — SC main-track and HPDC/IPDPS/Cluster/ISC/ACSOS coverage, the primary venues for scheduling research per the corpus's own venue map (`synthesis/01_VENUE_MAP.md`).

## Production/practitioner evidence currently in corpus

`raw/H_centers.md` [PRACTITIONER] reports, where available, each center's actual scheduler (e.g., Slurm-family deployments) and any operational customizations, as self-reported center practice rather than a research contribution.

## Known methods (generic domain background)

Backfill/fairshare scheduling, power-aware and topology-aware placement, and health/failure-signal-informed scheduling are common method families in this space generally; the corpus's specific coverage is in `02`, `A`, `B` — read those directly for which of these families this census actually documents.

## Research-practice gap

`synthesis/05_RESEARCH_PRACTICE_GAPS.md` addresses whether scheduling research (e.g., health-aware scheduling) is reflected in what centers in `H_centers.md` actually deploy; see `research/RESEARCH_GAPS_AND_CANDIDATES.md`.

## Evidence limitations

Broad coverage (29/31) reflects that "scheduling" appears widely as a keyword, not that every mention is a dedicated scheduling-research finding — check the specific document (`A`, `B`, `02`) for the depth of treatment on any specific claim.

## Canonical deeper sources

`synthesis/02_PAPER_CENSUS.md`, `raw/A_SC_main.md`, `raw/B_hpdc_ipdps_cluster_isc_acsos.md`, `synthesis/01_VENUE_MAP.md`.
