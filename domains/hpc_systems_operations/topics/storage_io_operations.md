# storage_io_operations.md

**Note:** this topic file was added beyond the initially sketched topic list because the corpus has substantial, grep-verified evidence for it (storage/I/O — predominantly Lustre — appears in 21/31 files) — see `DOMAIN_CONTEXT.md` and `TOPIC_MAP.md` for why topic grouping in this domain follows filesystem evidence rather than a fixed template.

## Scope

Parallel-filesystem (predominantly Lustre) storage and I/O operations — monitoring, contention diagnosis, and capacity/performance management.

## Operational problem

Diagnosing and managing I/O contention and performance variability on shared parallel filesystems, where a single misbehaving job can degrade throughput for many concurrent users, and where root-causing a slow-I/O incident to a specific client/OST/network path is genuinely hard.

## Research evidence currently in corpus

Storage/I/O research appears within the broader venue census (`corpus/aiops-survey/synthesis/02_PAPER_CENSUS.md`) rather than as a dedicated storage-specific research document in this corpus.

## Production/practitioner evidence currently in corpus

`corpus/aiops-survey/raw/H_centers.md` [PRACTITIONER] — center-level reports of Lustre (or equivalent parallel-filesystem) deployment and operational monitoring, where reported, as self-reported practice.

## Known methods (generic domain background)

Lustre-specific monitoring tools (e.g., LMT-family, vendor dashboards) and I/O-contention attribution techniques are common concerns in this space generally; this corpus's specific coverage should be checked directly in `H_centers.md` and `02_PAPER_CENSUS.md` rather than assumed.

## Research-practice gap

Not given a dedicated gap-analysis document in this corpus; general treatment via `synthesis/05_RESEARCH_PRACTICE_GAPS.md`.

## Evidence limitations

This topic's evidence is comparatively thin and practitioner-weighted (mostly `H_centers.md`) relative to topics with a dedicated research-audit document (e.g., anomaly detection, RCA); do not present storage/I/O claims here as having the same verification depth as those topics.

## Canonical deeper sources

`raw/H_centers.md`, `synthesis/02_PAPER_CENSUS.md`.
