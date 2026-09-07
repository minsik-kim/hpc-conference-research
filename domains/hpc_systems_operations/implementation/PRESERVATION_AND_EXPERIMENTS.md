# PRESERVATION_AND_EXPERIMENTS.md — hpc_systems_operations

Routing document only.

## Preservation requirements

`corpus/aiops-survey/synthesis/08_RESEARCH_PRESERVATION_REQUIREMENTS.md` sets out telemetry/provenance preservation requirements that the corpus identifies as necessary for any future system-building or research work in this space (e.g., what data must be retained, at what granularity, for how long, to support later diagnosis/RCA/research). This is an operational-decision document, not a peer-reviewed result — read it directly for the actual requirements; this file only points to it.

## Experiment designs

`corpus/aiops-survey/synthesis/11_INITIAL_EXPERIMENT_DESIGNS.md` contains first-experiment designs, including explicit falsification criteria, for the research candidates that survived the ranking/audit pipeline (see `research/RESEARCH_GAPS_AND_CANDIDATES.md` and `evidence/EVIDENCE_LINEAGE.md` for which candidates currently stand per `13_VERIFICATION_ROUND2.md`). These are proposed designs, not executed experiments — the corpus does not report results from running them.

## Relationship

The preservation requirements in `08` are a precondition for being able to run the experiments in `11` with adequate telemetry — read `08` before `11` if evaluating experiment feasibility on a real system.
