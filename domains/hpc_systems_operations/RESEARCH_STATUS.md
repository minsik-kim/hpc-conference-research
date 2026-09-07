# RESEARCH_STATUS.md — hpc_systems_operations

**Status: IMPORTED.** A 31-file research-survey corpus (`corpus/aiops-survey/`) has been imported byte-identically from a prior Cowork research session. This replaces the earlier "no corpus identified" placeholder.

## What exists now

- A completed literature/practitioner census across SC, HPDC, IPDPS, Cluster, ISC, ACSOS, DSN, ISSRE, workshops, and CUG (`corpus/aiops-survey/raw/A`–`H`).
- An independent second-round verification pass over specific claims from that census (`corpus/aiops-survey/raw/V1`–`V8`).
- Synthesis covering venue structure, SC-regular precedents, research-practice gaps, an initial research-candidate list, an adversarial novelty audit, a candidate ranking, first-experiment designs, a preservation-requirements document, an unresolved-evidence watchlist, and a second verification round that revises the ranking (`corpus/aiops-survey/synthesis/00`–`13`, `README_INDEX.md`).
- A canonical retrieval layer over that corpus: `DOMAIN_CONTEXT.md`, `DOMAIN_INDEX.md`, `TOPIC_MAP.md`, 14 `topics/*.md` files, and routing documents in `synthesis/`, `evidence/`, `implementation/`, `research/`.

## What was *not* done in this import

- **No new literature search.** Every claim, citation, and evidence-depth tag in the corpus is exactly as it was when staged; this import added indexing and routing documents, not new findings.
- **No per-citation catalog extraction** (`sources.yaml` or equivalent) — the hundreds of individual external citations embedded in the 31 files remain un-extracted; see `DOMAIN_INDEX.md` §6.
- **No resolution of any item on the corpus's own unresolved-evidence watchlist** — see `OPEN_QUESTIONS.md`.

## Current research-candidate status (as of the corpus's own latest verification round)

Per `corpus/aiops-survey/synthesis/13_VERIFICATION_ROUND2.md` (the current authority — see `evidence/EVIDENCE_LINEAGE.md`), the original 10-candidate list in `06_INITIAL_SC_RESEARCH_CANDIDATES.md` was narrowed by `10_SC_CANDIDATE_RANKING.md` and then revised again by `13`. This domain's canonical layer does not restate the specific candidate verdicts here (doing so would duplicate content that changes as the corpus is revisited) — read `research/RESEARCH_GAPS_AND_CANDIDATES.md` for routing to the actual ranking documents, and treat `13` as superseding `10` wherever the two differ.

## Known incomplete areas (unresolved in-source; not addressed by this import)

See `OPEN_QUESTIONS.md` for the full list and status. In brief: SC26 ORNL paper content, ICDE 2015–2026 sweep, ModelX (HPDC 2025) full text, several grey-literature items, and KISTI TRKO reports are all unresolved as the corpus itself reports.

## Last updated

`last_updated: 2026-09-07` — canonical import performed; no corpus content changed since staging (2026-09-06 per corpus file mtimes).
