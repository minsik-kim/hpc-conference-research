# OPEN_QUESTIONS.md — hpc_systems_operations

**Status: IMPORTED.** These are the corpus's own self-reported open items, routed here — none were invented or newly assessed for this import. Status vocabulary follows `governance/RESEARCH_GAP_RULES.md` where the corpus's own verdicts map onto it directly; where the corpus uses its own finer-grained vocabulary (evidence-depth tags, novelty verdicts), that is preserved and noted alongside.

## Unresolved evidence items (from `corpus/aiops-survey/synthesis/12_UNRESOLVED_EVIDENCE_AND_WATCHLIST.md` and `13_VERIFICATION_ROUND2.md` §5)

| Item | Status | Evidence depth | Source |
|---|---|---|---|
| SC26 program content — ORNL paper abstract/full text | `UNKNOWN` | `TITLE-ONLY` / `RECORD-METADATA` (partial) | `raw/V2_sc26_ornl.md` |
| ICDE 2015–2026 literature sweep | `UNKNOWN` (not performed) | `NOT FOUND` | `synthesis/12_UNRESOLVED_EVIDENCE_AND_WATCHLIST.md` |
| ModelX (HPDC 2025) | `UNDER_VERIFICATION` | `TITLE-ONLY` | `synthesis/12_UNRESOLVED_EVIDENCE_AND_WATCHLIST.md` |
| LDMSCON 2023–2025 (grey literature) | `UNDER_VERIFICATION` | `INDIRECT` / `NOT FOUND` (varies by year) | `raw/V8_grey_isc.md` |
| Beacon+ full text | `UNDER_VERIFICATION` | `ABSTRACT` (partial) | `raw/V8_grey_isc.md` |
| HPE Slingshot admin-guide counters (exact metric names) | `UNDER_VERIFICATION` | `INDIRECT` | `raw/V8_grey_isc.md` |
| KISTI internal technical reports (TRKO) | `UNKNOWN` (not yet searched) | `NOT FOUND` | `synthesis/13_VERIFICATION_ROUND2.md` §5 |

**None of these are resolved by this import.** Resolving any of them would require new literature search, which was explicitly out of scope for this canonical-import pass.

## Research-candidate open questions

The corpus's own candidate-ranking and novelty-audit pipeline (`06` → `10` → `09` → `13`) produced verdicts using its own vocabulary (`DROP` / `KEEP-WATCHING` / `WORKSHOP-LEVEL` / `SC-STRETCH` / `SC-PLAUSIBLE` / `TOP-CANDIDATE` for ranking; `CLOSED` / `PARTIALLY_ADDRESSED` / `STILL_OPEN` / `TOO_SITE_SPECIFIC` / `ENGINEERING_ONLY` / `INSUFFICIENT_EVIDENCE` for novelty). These verdicts are **not restated here** to avoid a second, driftable copy of a ranking that already lives in `13_VERIFICATION_ROUND2.md`. See `research/RESEARCH_GAPS_AND_CANDIDATES.md` for routing and `evidence/EVIDENCE_LINEAGE.md` for which document's verdict currently governs each candidate.

## Do not do in routine maintenance of this domain

- Do not perform new external search to close any item above — that is a distinct, explicitly-scoped future task, not a side effect of editing this domain's canonical layer.
- Do not upgrade a `TITLE-ONLY`/`ABSTRACT`/`INDIRECT` evidence-depth item to `FULL-TEXT` without an actual new verification pass recorded in a new `raw/V*` document.
- Do not mark an item here `CLOSED` based on a topic file or this file alone — closure must trace to a corpus document that actually performed the check.
