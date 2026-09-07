# power_cooling.md

## Scope

Power, cooling, and facility operations for HPC systems (power budgeting/capping, CDU/liquid-cooling management, facility-level telemetry). 24/31 corpus files reference this topic.

## Operational problem

Managing power draw and thermal load within facility constraints (power caps, cooling-plant capacity) while maintaining performance, and integrating facility-level signals (CDU status, power telemetry) into broader operational monitoring alongside compute/fabric/storage.

## Research evidence currently in corpus

Power/cooling research appears within the broader venue census (`corpus/aiops-survey/synthesis/02_PAPER_CENSUS.md`); no dedicated power/cooling research-audit document exists distinct from the general census in this corpus.

## Production/practitioner evidence currently in corpus

- `corpus/aiops-survey/raw/H_centers.md` [PRACTITIONER] — center-level reports of power/cooling infrastructure and monitoring (CDU deployments, power telemetry), where reported.
- `corpus/aiops-survey/raw/E_cug_vendor.md` [VENDOR] — vendor material relevant to power/cooling infrastructure products.

## Known methods (generic domain background)

Power capping/budgeting and liquid-cooling (CDU) telemetry integration are common concerns in this space generally; this corpus's specific coverage is predominantly practitioner/vendor (center facility reports), not independent peer-reviewed research specific to power/cooling operations.

## Research-practice gap

Not given a dedicated gap-analysis document; general treatment via `synthesis/05_RESEARCH_PRACTICE_GAPS.md`.

## Evidence limitations

Predominantly practitioner/vendor evidence; treat any specific power/cooling numeric claim as site-specific practitioner-reported data (from `H_centers.md`) unless a research document independently confirms it.

## Canonical deeper sources

`raw/H_centers.md`, `raw/E_cug_vendor.md`, `synthesis/02_PAPER_CENSUS.md`.
