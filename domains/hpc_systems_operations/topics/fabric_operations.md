# fabric_operations.md

## Scope

Network/interconnect-fabric operations, with particular corpus emphasis on HPE Slingshot (the dominant fabric in the corpus's covered centers/vendors). 24/31 corpus files reference fabric/Slingshot operations.

## Operational problem

Monitoring, diagnosing, and managing high-radix HPC interconnect fabrics (congestion, link errors, routing) at a scale where per-link telemetry volume and topology complexity make manual management infeasible.

## Research evidence currently in corpus

Fabric-operations research is covered as part of the broader census rather than in a dedicated fabric-specific research document; see `corpus/aiops-survey/synthesis/02_PAPER_CENSUS.md` for any fabric-specific papers captured there.

## Production/practitioner evidence currently in corpus

- `corpus/aiops-survey/raw/H_centers.md` [PRACTITIONER] — center-level reports of fabric operations as actually run.
- `corpus/aiops-survey/raw/E_cug_vendor.md` [CUG/VENDOR] — CUG and vendor material on Slingshot specifically, including product/operational claims.
- `corpus/aiops-survey/raw/V8_grey_isc.md` [verification] — re-checks grey-literature items including **HPE Slingshot admin-guide counters** (marked unresolved/`INDIRECT` in-source — see `OPEN_QUESTIONS.md`) and an ISC 2024–2026 recount relevant to fabric-operations coverage.

## Known methods (generic domain background)

Congestion-control monitoring, adaptive routing, and link-health telemetry are common fabric-operations concerns generally; the corpus's actual evidence here is predominantly vendor/practitioner (Slingshot-specific), not independent peer-reviewed research — see the source-type warning in `DOMAIN_CONTEXT.md` before treating a vendor claim as a verified result.

## Research-practice gap

Not given a dedicated gap-analysis document; general treatment via `synthesis/05_RESEARCH_PRACTICE_GAPS.md`.

## Evidence limitations

The Slingshot admin-guide counter claim in `V8_grey_isc.md` remains `INDIRECT`/unresolved — do not present exact metric names as confirmed without checking `V8` directly.

## Canonical deeper sources

`raw/H_centers.md`, `raw/E_cug_vendor.md`, `raw/V8_grey_isc.md`.
