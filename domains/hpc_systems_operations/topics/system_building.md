# system_building.md

## Scope

System-building and production-deployment work framed as a potential research contribution (e.g., "we built and deployed X at scale" as a paper's core claim) — 9/31 corpus files use this explicit framing. This topic exists specifically to make system-building research retrievable while preserving the corpus's own qualifications about when scale/deployment alone is or is not SC-regular-worthy.

## Operational problem

Whether building and deploying an operational system at large scale is, by itself, a sufficient research contribution for a top venue (SC regular/technical track), versus requiring an additional generalizable/novel technical contribution beyond engineering effort.

## Research evidence currently in corpus

- `corpus/aiops-survey/synthesis/03_SC_REGULAR_PRECEDENTS.md` [internal precedent analysis] — analyzes actual SC-regular acceptance precedents for system-building-framed submissions.
- `corpus/aiops-survey/synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` and `synthesis/13_VERIFICATION_ROUND2.md` [internal adversarial audit/verification] — apply novelty-falsification discipline specifically to system-building claims, using verdicts including `ENGINEERING_ONLY` (a system-building claim judged to be engineering effort without a separable research contribution) and `TOO_SITE_SPECIFIC`.

## Production/practitioner evidence currently in corpus

`raw/H_centers.md` [PRACTITIONER] documents many deployed operational systems at production centers; **this corpus's own discipline is that a system being deployed does not by itself make it "SC regular worthy"** — that judgment is made only by `03`/`09`/`13` against actual precedent, and this topic file does not promote a deployment to research-contribution status on its own.

## Known methods (generic domain background)

"Systems paper" framing (deployment at scale + operational lessons) is a recognized but contested category at top HPC venues generally; the corpus's own precedent analysis (`03`) is the specific evidence for what has and hasn't been accepted under this framing historically.

## Research-practice gap

See `research/RESEARCH_GAPS_AND_CANDIDATES.md` — several candidates in the ranking pipeline were evaluated specifically against this "engineering vs. research contribution" line.

## Evidence limitations

Precedent analysis (`03`) is itself synthesis over the corpus's own venue/paper census (`01`, `02`) — treat its precedent claims as grounded in that census, not as an independent legal/editorial ruling.

## Canonical deeper sources

`synthesis/03_SC_REGULAR_PRECEDENTS.md`, `synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md`, `synthesis/13_VERIFICATION_ROUND2.md`.
