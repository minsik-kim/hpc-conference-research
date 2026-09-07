# RESEARCH_GAPS_AND_CANDIDATES.md — hpc_systems_operations

Routing document only — current candidate/gap status lives in the corpus documents themselves, not here, to avoid a second copy that can drift out of sync.

## Research-practice gap analysis

`corpus/aiops-survey/synthesis/05_RESEARCH_PRACTICE_GAPS.md` — the gap table between what the research literature addresses and what production centers actually do/need (per `raw/H_centers.md` and the workshop/CUG evidence in `raw/D`, `raw/E`). Explicit "research-practice gap" framing appears in 4/31 corpus files; the broader theme runs through `09` and `13` as well.

## Candidate pipeline (read in this order; later documents supersede earlier ones per `evidence/EVIDENCE_LINEAGE.md`)

1. `corpus/aiops-survey/synthesis/06_INITIAL_SC_RESEARCH_CANDIDATES.md` — initial list of 10 candidates.
2. `corpus/aiops-survey/synthesis/10_SC_CANDIDATE_RANKING.md` — first ranking (10 candidates → 4 + 1 workshop-level item), using verdicts `DROP` / `KEEP-WATCHING` / `WORKSHOP-LEVEL` / `SC-STRETCH` / `SC-PLAUSIBLE` / `TOP-CANDIDATE`.
3. `corpus/aiops-survey/synthesis/09_ADVERSARIAL_NOVELTY_AUDIT.md` — adversarial falsification pass, using novelty verdicts `CLOSED` / `PARTIALLY_ADDRESSED` / `STILL_OPEN` / `TOO_SITE_SPECIFIC` / `ENGINEERING_ONLY` / `INSUFFICIENT_EVIDENCE`.
4. `corpus/aiops-survey/synthesis/13_VERIFICATION_ROUND2.md` — **current authority.** Revises specific items from `09` and updates the ranking from `10`.

## Unresolved evidence feeding the pipeline

`corpus/aiops-survey/synthesis/12_UNRESOLVED_EVIDENCE_AND_WATCHLIST.md` — items whose unresolved status directly bears on candidate novelty verdicts above (e.g., a candidate cannot be marked `CLOSED` on novelty grounds while a directly relevant watchlist item is still `UNKNOWN`/`TITLE-ONLY`). See `OPEN_QUESTIONS.md` for the routed list.

## How to answer a "what should we research here" question

Read `13_VERIFICATION_ROUND2.md` for the current ranking, cross-check any candidate whose novelty claim depends on an item in `OPEN_QUESTIONS.md`, and report the verdict with its actual corpus label (do not paraphrase `SC-PLAUSIBLE` as "recommended" or `KEEP-WATCHING` as "rejected" — use the corpus's own vocabulary).
