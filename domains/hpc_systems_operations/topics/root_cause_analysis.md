# root_cause_analysis.md

## Scope

Root-cause analysis (RCA) and performance-diagnosis research/practice — the maturity stage that turns a detected anomaly or predicted failure into an actionable explanation. 28/31 corpus files reference RCA. Log analytics/log intelligence (11/31 files) is included here as a diagnosis *technique* (as opposed to `topics/telemetry_observability.md`, which covers log collection as a data source).

## Operational problem

Explaining *why* an anomaly or failure occurred (which component, which interaction, which upstream cause) quickly enough to act, across systems with many interacting subsystems (compute, fabric, storage, power/cooling) where causal attribution is genuinely hard.

## Research evidence currently in corpus

- `corpus/aiops-survey/raw/F_axes_ABC.md`, `raw/G_axes_DEFG.md` [internal audit over external literature] — RCA-relevant research axes within the broader census.
- `corpus/aiops-survey/raw/V4_hindsight_suffbench.md` [verification] — re-verifies claims about **Hindsight (NSDI'23)**, **TelemetrySuffBench**, and causal-discovery-under-subsampling literature specifically relevant to RCA.
- `corpus/aiops-survey/raw/V5_fdi_sensor_placement.md` [verification] — re-verifies fault-detection/isolation (FDI) sensor-placement literature, a control-theory-adjacent RCA approach.

## Production/practitioner evidence currently in corpus

`raw/H_centers.md` [PRACTITIONER] covers, where reported, how specific centers actually perform incident diagnosis today (manual log correlation vs. tooling-assisted); this is practice evidence about specific sites and is not conflated with the research systems named above.

## Known methods (generic domain background)

Causal-graph/causal-discovery methods, log-correlation and log-template mining, and control-theory-style fault detection/isolation (sensor placement, diagnosability) are the common method families discussed in this space generally. The corpus's specific verified characterization of any one of them (Hindsight, TelemetrySuffBench, the FDI sensor-placement literature) is in `V4`/`V5`, not restated here.

## Research-practice gap

See `synthesis/05_RESEARCH_PRACTICE_GAPS.md` and `synthesis/09`/`13` for whether a specific RCA research direction is open/closed against this corpus's census — route through `research/RESEARCH_GAPS_AND_CANDIDATES.md`.

## Evidence limitations

`V4` and `V5` are the current authority for the specific systems/literature they name (per `evidence/EVIDENCE_LINEAGE.md`); other RCA-adjacent items in `F`/`G` not covered by a `V` document remain unverified initial census.

## Canonical deeper sources

`raw/F_axes_ABC.md`, `raw/G_axes_DEFG.md`, `raw/V4_hindsight_suffbench.md`, `raw/V5_fdi_sensor_placement.md`, `synthesis/05`, `synthesis/09`, `synthesis/13`.
