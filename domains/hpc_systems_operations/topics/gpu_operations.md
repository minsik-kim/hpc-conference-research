# gpu_operations.md

## Scope

GPU/AI-cluster operations, with particular corpus emphasis on NVIDIA DCGM-based monitoring. 19/31 corpus files reference GPU-cluster operations/DCGM.

## Operational problem

Monitoring and managing GPU health, utilization, and failure modes (ECC errors, thermal throttling, Xid errors) at cluster scale, and integrating GPU-specific telemetry into broader system operations (scheduling, RCA) alongside CPU/fabric/storage signals.

## Research evidence currently in corpus

GPU-operations research appears within the broader venue census (`corpus/aiops-survey/synthesis/02_PAPER_CENSUS.md`); no dedicated GPU-operations research-audit document exists in this corpus distinct from the general census.

## Production/practitioner evidence currently in corpus

- `corpus/aiops-survey/raw/H_centers.md` [PRACTITIONER] — center-level reports of GPU-cluster monitoring stacks (where GPU-heavy centers are profiled).
- `corpus/aiops-survey/raw/E_cug_vendor.md` [VENDOR] — vendor material on DCGM and related GPU-monitoring tooling.

## Known methods (generic domain background)

DCGM-based health/utilization monitoring and GPU-specific anomaly signatures (ECC/Xid errors, thermal events) are common concerns in this space generally; this corpus's specific coverage is predominantly vendor/practitioner, not independent peer-reviewed research on GPU-operations specifically — apply the source-type caution in `DOMAIN_CONTEXT.md`.

## Research-practice gap

Not given a dedicated gap-analysis document; general treatment via `synthesis/05_RESEARCH_PRACTICE_GAPS.md`.

## Evidence limitations

Predominantly vendor/practitioner evidence (DCGM, center reports) with limited independent research-audit depth in this corpus specifically for GPU operations as distinct from general anomaly detection/RCA (see those topic files for the research side of GPU-cluster-relevant methods).

## Canonical deeper sources

`raw/H_centers.md`, `raw/E_cug_vendor.md`, `synthesis/02_PAPER_CENSUS.md`.
