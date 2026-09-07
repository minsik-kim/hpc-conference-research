# anomaly_detection.md

## Scope

Statistical and ML-based detection of anomalous system/job/component behavior from telemetry, as a maturity stage above rule-based alerting and below failure prediction/RCA (see `DOMAIN_CONTEXT.md`'s maturity-stage model). 25/31 corpus files reference anomaly detection.

## Operational problem

Distinguishing genuine operational anomalies (impending failure, misconfiguration, contention, security event) from normal variance in very high-dimensional, non-stationary HPC telemetry, at a scale and rate that rules out manual review.

## Research evidence currently in corpus

- `corpus/aiops-survey/raw/F_axes_ABC.md` and `raw/G_axes_DEFG.md` [internal adversarial-audit documents over external literature] — census and adversarial audit of anomaly-detection research axes.
- `corpus/aiops-survey/raw/V1_db_retention_sweep.md` [verification] and `raw/V6_lcopt_centile_setdiff.md` [verification] — re-checked specific claims about anomaly-detection-adjacent systems (LC-Opt, CENTILE, SeT-Diff) first raised in the initial census.
- `corpus/aiops-survey/synthesis/05_RESEARCH_PRACTICE_GAPS.md` — where academic anomaly-detection work is compared against what centers actually deploy.

## Production/practitioner evidence currently in corpus

- `corpus/aiops-survey/raw/H_centers.md` [PRACTITIONER] — where centers report using threshold- or rule-based alerting rather than statistical/ML anomaly detection, that distinction is preserved as-is; do not describe a center's rule-based alerting as "anomaly detection research."

## Known methods (generic domain background)

Statistical (control-chart, outlier-score) and ML-based (clustering, autoencoder, sequence-model) approaches are the common families discussed in this literature space generally. Which specific method families the corpus's own census (`F`, `G`) actually covers, and with what evidence-confidence tag, should be read directly rather than assumed.

## Research-practice gap

See `synthesis/05_RESEARCH_PRACTICE_GAPS.md` and the adversarial audit in `synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` (revised by `13_VERIFICATION_ROUND2.md`) for whether a specific anomaly-detection research direction is `STILL_OPEN`, `PARTIALLY_ADDRESSED`, or `CLOSED` against this corpus's census — route through `research/RESEARCH_GAPS_AND_CANDIDATES.md`.

## Evidence limitations

`V6_lcopt_centile_setdiff.md` revises characterizations first made in `F`/`G` — per `evidence/EVIDENCE_LINEAGE.md`, treat `V6` as authoritative for LC-Opt/CENTILE/SeT-Diff specifically, and `F`/`G` as the initial (unverified for these items) census otherwise.

## Canonical deeper sources

`raw/F_axes_ABC.md`, `raw/G_axes_DEFG.md`, `raw/V1_db_retention_sweep.md`, `raw/V6_lcopt_centile_setdiff.md`, `synthesis/05`, `synthesis/09`, `synthesis/13`.
