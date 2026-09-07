# automated_remediation.md

## Scope

Automated remediation — the highest maturity stage in this domain's model (collection → visualization → alerting → anomaly detection → prediction → diagnosis/RCA → recommendation → **automated remediation**), covering automatic drain/repair/recovery actions triggered by detected or predicted problems. 24/31 corpus files reference this topic.

## Operational problem

Acting automatically on a detected or predicted problem (draining a node, restarting a service, rerouting traffic) with high enough confidence to avoid unnecessary disruption, and with enough auditability/rollback to be trusted in production.

## Research evidence currently in corpus

Automated-remediation research is treated primarily as a research-practice gap area rather than as a well-populated independent research topic in this corpus — see `corpus/aiops-survey/synthesis/05_RESEARCH_PRACTICE_GAPS.md`, which explicitly addresses the gap between remediation *research* and remediation *practice*.

## Production/practitioner evidence currently in corpus

`corpus/aiops-survey/raw/H_centers.md` [PRACTITIONER] — reports, where available, on centers' actual automated-remediation practice (e.g., automatic node drain on threshold breach), which the corpus's own gap analysis (`05`) characterizes as generally simpler/more rule-based than what research literature proposes.

## Known methods (generic domain background)

Rule/threshold-triggered drain-and-repair automation is the most common practitioner-reported pattern in this space generally; ML-driven remediation-policy research (e.g., reinforcement-learning-based remediation) is a research-side direction whose maturity in this corpus's census should be checked directly rather than assumed present.

## Research-practice gap

This is one of the topics where the corpus's explicit research-practice gap framing (4/31 files) most directly applies — `synthesis/05_RESEARCH_PRACTICE_GAPS.md` is the primary document; see `research/RESEARCH_GAPS_AND_CANDIDATES.md` for how this feeds the candidate-ranking pipeline.

## Evidence limitations

Practitioner evidence (`H_centers.md`) here should not be described as "automated-remediation research" — per `DOMAIN_CONTEXT.md`'s explicit warning against upgrading practitioner deployment to research-grade claims.

## Canonical deeper sources

`synthesis/05_RESEARCH_PRACTICE_GAPS.md`, `raw/H_centers.md`.
