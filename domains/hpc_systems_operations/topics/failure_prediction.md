# failure_prediction.md

## Scope

Predictive maintenance and failure-forecasting research/practice for HPC hardware and jobs — the maturity stage above anomaly detection (predicting failure before it manifests as an anomaly). 16/31 corpus files reference failure prediction specifically.

## Operational problem

Forecasting node/component/job failure far enough in advance to act (drain, migrate, service) without an unacceptable false-positive rate that would drain healthy resources.

## Research evidence currently in corpus

- `corpus/aiops-survey/raw/F_axes_ABC.md`, `raw/G_axes_DEFG.md` [internal audit over external literature] — cover failure-prediction research axes as part of the broader adversarial census.
- `corpus/aiops-survey/raw/V3_pika_tuncer.md` [verification] — specifically re-verifies claims about **PIKA (IEEE Cluster 2020)** and **Tuncer et al. (TPDS 2019)**, two named failure-prediction-adjacent systems/papers first characterized in the initial census. Read `V3` directly for the corpus's current, verified characterization of these two works — this topic file does not restate it, to avoid a second copy that can drift from `V3`'s actual finding.

## Production/practitioner evidence currently in corpus

Center-level self-reports of predictive-maintenance deployment (as opposed to research systems) are covered, where present, within `raw/H_centers.md` [PRACTITIONER] alongside the other operational-maturity data for each center; this corpus does not treat a center's use of vendor-supplied hardware-health prediction (e.g., disk/GPU health scoring) as equivalent to a peer-reviewed failure-prediction research result.

## Known methods (generic domain background)

Survival-analysis and sequence/time-series ML approaches to component failure forecasting are the common method families in this space generally; whether and how the corpus's own census characterizes PIKA/Tuncer specifically along these lines should be read from `V3` directly.

## Research-practice gap

`synthesis/05_RESEARCH_PRACTICE_GAPS.md` and the adversarial/verification chain (`09` → `13`) address whether failure-prediction research directions remain open, are partially addressed, or are closed against this corpus's census — see `research/RESEARCH_GAPS_AND_CANDIDATES.md`.

## Evidence limitations

`V3`'s re-verification of PIKA/Tuncer is the corpus's current authority for those two items specifically (per `evidence/EVIDENCE_LINEAGE.md`); the broader initial census in `F`/`G` for other failure-prediction items has not necessarily been independently re-verified beyond what `V3` covers.

## Canonical deeper sources

`raw/F_axes_ABC.md`, `raw/G_axes_DEFG.md`, `raw/V3_pika_tuncer.md`, `synthesis/05`, `synthesis/09`, `synthesis/13`.
